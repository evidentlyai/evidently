import re
import warnings
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Iterator
from typing import NamedTuple
from typing import Optional
from typing import Union

import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently.core.datasets import FeatureDescriptor
from evidently.core.datasets import LLMClassification
from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.legacy.features.llm_judge import LLMJudge
from evidently.legacy.features.llm_judge import MulticlassClassificationPromptTemplate
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.base import LLMMessage
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.optimization.optimizer import BaseOptimizer
from evidently.llm.optimization.optimizer import InitContextMixin
from evidently.llm.optimization.optimizer import Inputs
from evidently.llm.optimization.optimizer import LogID
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerContext
from evidently.llm.optimization.optimizer import OptimizerLog
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.arg_type_registry import BaseArgTypeRegistry


class PromptOptimizationLog(OptimizerLog):
    input_prompt: str
    optimizer_prompt: str
    new_prompt: str
    input_tokens: int
    output_tokens: str
    stop: bool

    def message(self) -> str:
        return f"Prompt '{self.input_prompt[:40]}...' optimized to '{self.new_prompt[:40]}...'"


class PromptOptimizerStrategy(BaseArgTypeRegistry, AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "prompt_optimizer_strategy"

    @abstractmethod
    async def run(self, prompt: str, state: OptimizerContext) -> PromptOptimizationLog:
        raise NotImplementedError()


class PromptOptimizerConfig(OptimizerConfig):
    strategy: PromptOptimizerStrategy


class PromptEvaluationLog(OptimizerLog):
    prompt: str
    data: Dict[str, Optional[pd.Series]]

    def __init__(
        self,
        prompt: str,
        prediction: Optional[pd.Series] = None,
        prediction_reasoning: Optional[pd.Series] = None,
        prediction_scores: Optional[pd.Series] = None,
        data: Optional[Dict[str, Optional[pd.Series]]] = None,
        **kwargs: Any,
    ) -> None:
        data = data or {}
        data.setdefault(Inputs.Pred, prediction)
        data.setdefault(Inputs.PredScores, prediction_scores)
        data.setdefault(Inputs.PredReasoning, prediction_reasoning)
        super().__init__(prompt=prompt, data=data, **kwargs)

    def message(self) -> str:
        lens = " ".join(f"{k}({len(v)})" for k, v in self.data.items() if v is not None)
        return f"Evaluated prompt '{self.prompt[:40]}...', got {lens}"

    def get_data(self, name: str) -> pd.Series:
        val = self.data.get(name, None)
        if val is None:
            raise KeyError(f"Evaluation data does not contain {name}")
        return val

    def has_data(self, name: str) -> bool:
        return self.data.get(name, None) is not None


def get_classification_dataset(context: OptimizerContext) -> Dataset:
    clf = context.get_input(Inputs.LLMClassification, LLMClassification, "Missing LLMClassification input")
    return Dataset.from_pandas(
        pd.DataFrame(
            {
                clf.values: list(context.get_input(Inputs.Values, pd.Series)),
                clf.target: list(context.get_input(Inputs.Target, pd.Series)),
            }
        )
    )


class PromptEvaluator(AutoAliasMixin, EvidentlyBaseModel, InitContextMixin, ABC):
    __alias_type__: ClassVar = "prompt_evaluator"

    def evaluate(self, prompt: str, context: OptimizerContext) -> PromptEvaluationLog:
        dataset = get_classification_dataset(context)
        return self._evaluate(prompt, dataset, context.options)

    @abstractmethod
    def _evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        raise NotImplementedError()

    @abstractmethod
    def get_base_prompt(self) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_task(self) -> str:
        raise NotImplementedError()

    def get_optimizer_instructions(self) -> Optional[str]:
        return None

    def init(self, context: OptimizerContext):
        context.set_input(Inputs.Task, self.get_task())
        instructions = self.get_optimizer_instructions()
        if instructions is not None:
            context.set_input(Inputs.OptimizerPromptInstructions, instructions)


AnyJudgeTemplateTuple = (BinaryClassificationPromptTemplate, MulticlassClassificationPromptTemplate)
AnyJudgeTemplate = Union[AnyJudgeTemplateTuple]


class LLMJudgePromptEvaluator(PromptEvaluator):
    judge: LLMJudge

    def _evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        template = self.template
        judge = self.judge.update(template=template.update(criteria=prompt))
        generated = judge.generate_features_renamed(
            dataset.as_dataframe(), data_definition=dataset.data_definition, options=options
        )
        cols = judge.list_columns()
        category = generated[[c.name for c in cols if "category" in c.name][0]] if template.include_category else None
        score = generated[[c.name for c in cols if "score" in c.name][0]] if template.include_score else None
        reasoning = (
            generated[[c.name for c in cols if "reasoning" in c.name][0]] if template.include_reasoning else None
        )
        return PromptEvaluationLog(
            prompt=prompt,
            data={
                Inputs.Pred: category,
                Inputs.PredReasoning: reasoning,
                Inputs.PredScores: score,
            },
        )

    @property
    def template(self) -> AnyJudgeTemplate:
        t = self.judge.template
        assert isinstance(t, AnyJudgeTemplateTuple)
        return t

    def get_base_prompt(self) -> str:
        return self.template.criteria

    def get_task(self) -> str:
        return "classify texts"

    def get_optimizer_instructions(self) -> Optional[str]:
        return "Do not add new classes."


CustomEvaluatorCallable = Callable[[str], PromptEvaluationLog]


class CallablePromptEvaluator(PromptEvaluator):
    func: str
    _func: Optional[CustomEvaluatorCallable] = PrivateAttr(None)
    task: Optional[str] = None

    def __init__(
        self,
        func: Union[str, CustomEvaluatorCallable],
    ):
        if callable(func):
            self._func = func
            func = f"{func.__module__}.{func.__name__}"
        else:
            self._func = None
        self.func = func
        super().__init__()

    def evaluate(self, prompt: str, context: OptimizerContext) -> PromptEvaluationLog:
        return self._func(prompt)

    def _evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        raise NotImplementedError()

    def get_base_prompt(self) -> Optional[str]:
        return None

    def get_task(self) -> str:
        if self.task is not None:
            return self.task
        doc = self._func.__doc__
        if doc is None:
            warnings.warn(f"Please add docstring to {self.func} describing task you are trying to optimize.")
        return doc


AnyPromptEvaluator = Union[PromptEvaluator, LLMJudge, CustomEvaluatorCallable]


def get_prompt_evaluator(value: AnyPromptEvaluator) -> PromptEvaluator:
    if isinstance(value, PromptEvaluator):
        return value
    if isinstance(value, LLMJudge) and isinstance(value.template, AnyJudgeTemplateTuple):
        return LLMJudgePromptEvaluator(judge=value)
    if callable(value):
        # todo: check signature
        return CallablePromptEvaluator(value)
    raise NotImplementedError(f"Not implemented for {value.__class__.__name__}")


class PromptScoringLog(OptimizerLog):
    evaluation_log_id: LogID
    scores: Dict[str, float]

    def message(self) -> str:
        return "Prompt scored: " + ", ".join(f"{k}: {v}" for k, v in self.scores.items())


class OptimizationScorer(BaseArgTypeRegistry, AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "optimizer_scorer"

    def get_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        raise NotImplementedError()

    def score(self, context: OptimizerContext, evaluation: PromptEvaluationLog) -> Optional[float]:
        target = context.get_input(Inputs.Target, missing_error_message=f"{self.get_name()} requires target input")
        predictions = evaluation.get_data(Inputs.Pred)
        if not isinstance(target, pd.Series):
            target = pd.Series([target for _ in range(len(predictions))])
        return self._score(predictions, target, context.options)


StrOptimizationScorer = Union[str, OptimizationScorer, Any]


def get_scorer(scorer: StrOptimizationScorer) -> OptimizationScorer:
    if isinstance(scorer, str):
        return OptimizationScorer.registry_lookup(scorer)
    if isinstance(scorer, OptimizationScorer):
        return scorer
    if isinstance(scorer, LLMJudge) and isinstance(scorer.template, BinaryClassificationPromptTemplate):
        return BinaryJudgeScorer(judge=scorer)
    if isinstance(scorer, FeatureDescriptor) and isinstance(scorer.feature, LLMJudge):
        return BinaryJudgeScorer(judge=scorer.feature)
    raise NotImplementedError(f"Not implemented for {scorer.__class__.__name__}")


class BinaryJudgeScorer(OptimizationScorer):
    judge: LLMJudge
    scorer: Optional[OptimizationScorer] = None

    def score(self, context: OptimizerContext, evaluation: PromptEvaluationLog) -> Optional[float]:
        predictions = evaluation.get_data(Inputs.Pred)

        judge = self.judge
        template = judge.template
        if not isinstance(template, BinaryClassificationPromptTemplate):
            raise ValueError("Judge scorer only supports binary classification")
        judge.update(template=template.update(include_category=True, include_reasoning=True, include_score=False))
        input_columns = judge.get_input_columns()
        if len(input_columns) > 1:
            raise NotImplementedError("Judge scorer only supports one input column")
        input_column = next(iter(input_columns))
        generated = judge.generate_features_renamed(
            pd.DataFrame({input_column: predictions}),
            data_definition=DataDefinition(text_columns=input_column),
            options=context.options,
        )
        cols = judge.list_columns()
        category = generated[[c.name for c in cols if "category" in c.name][0]] if template.include_category else None
        reasoning = (
            generated[[c.name for c in cols if "reasoning" in c.name][0]] if template.include_reasoning else None
        )
        assert category is not None
        scorer = self.scorer or AccuracyScorer()
        target = pd.Series([template.target_category] * len(predictions))
        evaluation.data[Inputs.Target] = target
        evaluation.data[Inputs.PredReasoning] = reasoning
        return scorer._score(category, target=target, options=context.options)

    def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        raise NotImplementedError()


class AccuracyScorer(OptimizationScorer):
    __registry_alias__: ClassVar = "accuracy"

    def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return (predictions == target).mean()


class EarlyStopConfig(BaseModel):
    bigger_score_better: bool = True
    max_iterations: int = 5
    min_score_gain: float = 0.01
    target_score: float = 1.0

    @property
    def score_sign(self):
        return 1 if self.bigger_score_better else -1

    def should_stop(self, context: OptimizerContext) -> Optional[float]:
        if len(context.get_logs(PromptOptimizationLog)) > self.max_iterations:
            return True
        scores = context.get_logs(PromptScoringLog)
        score_name = context.get_input(Inputs.Scorer, OptimizationScorer).get_name()
        if len(scores) > 0:
            last_score = scores[-1]
            if last_score.scores[score_name] == self.target_score:
                return True
        if len(scores) > 1:
            prev_score, last_score = scores[-2:]
            if (last_score.scores[score_name] - prev_score.scores[score_name]) * self.score_sign < self.min_score_gain:
                return True
        return False


class PromptOptimizer(BaseOptimizer[PromptOptimizerConfig]):
    def __init__(self, name: str, strategy: Union[str, PromptOptimizerStrategy], checkpoint_path: Optional[str] = None):
        strategy = PromptOptimizerStrategy.registry_lookup(strategy)
        super().__init__(name, PromptOptimizerConfig(strategy=strategy), checkpoint_path=checkpoint_path)

    def run_sync(
        self,
        evaluator: AnyPromptEvaluator,
        scorer: Optional[StrOptimizationScorer],
        options: AnyOptions = None,
    ) -> Optional[PromptOptimizationLog]:
        return async_to_sync(self.run(evaluator, scorer, options))

    async def run(
        self,
        evaluator: AnyPromptEvaluator,
        scorer: Optional[StrOptimizationScorer],
        options: AnyOptions = None,
        early_stop: Optional[EarlyStopConfig] = None,
    ) -> Optional[PromptOptimizationLog]:
        evaluator = get_prompt_evaluator(evaluator)
        self.set_input(Inputs.Evaluator, evaluator)
        self.set_input(Inputs.Options, Options.from_any_options(options))
        if scorer is None:
            scorer = AccuracyScorer()
        self.set_input(Inputs.Scorer, get_scorer(scorer))
        self.set_input(Inputs.EarlyStop, early_stop or EarlyStopConfig())

        self._lock()

        await self.resume()

    def _get_prompt(self) -> str:
        log = self.context.get_last_log(PromptOptimizationLog)
        if log is not None:
            return log.new_prompt
        evaluator = self.get_input(Inputs.Evaluator, PromptEvaluator)
        prompt = evaluator.get_base_prompt()
        if prompt is not None:
            return prompt
        return self.get_input(
            Inputs.BasePrompt, str, f"'{Inputs.BasePrompt}' input is required for {evaluator.__class__.__name__}"
        )

    async def resume(self):
        evaluator = self.get_input(Inputs.Evaluator, PromptEvaluator)
        scorer = self.get_input(Inputs.Scorer, OptimizationScorer)
        early_stop = self.get_input(Inputs.EarlyStop, EarlyStopConfig)
        prompt = self._get_prompt()

        stop = False
        self._eval_score(prompt, evaluator, scorer)
        while not stop:
            opt_log = await self.config.strategy.run(prompt, self.context)
            self.context.add_log(opt_log)
            prompt = opt_log.new_prompt
            self._eval_score(prompt, evaluator, scorer)
            stop = opt_log.stop or early_stop.should_stop(self.context)

    def _eval_score(self, prompt: str, evaluator: PromptEvaluator, scorer: OptimizationScorer):
        eval_log = evaluator.evaluate(prompt, self.context)
        self.context.add_log(eval_log)
        score = scorer.score(self.context, eval_log)
        score_log = PromptScoringLog(evaluation_log_id=eval_log.id, scores={scorer.get_name(): score})
        self.context.add_log(score_log)

    @property
    def config(self) -> PromptOptimizerConfig:
        return self.context.config

    def set_input_dataset(self, dataset: Dataset):
        dd = dataset.data_definition
        clf = dd.llm
        assert isinstance(clf, LLMClassification)
        self.set_input(Inputs.Values, dataset.column(clf.values).data)
        self.set_input(Inputs.Target, dataset.column(clf.target).data)
        self.set_input(Inputs.LLMClassification, clf)
        if clf.reasoning is not None:
            self.set_input(Inputs.Reasoning, dataset.column(clf.reasoning).data)
        if clf.predictions is not None:
            self.set_input(Inputs.Pred, dataset.column(clf.predictions).data)
        if clf.prediction_reasoning is not None:
            self.set_input(Inputs.PredReasoning, dataset.column(clf.prediction_reasoning).data)

    def best_prompt(self):
        score_name = self.get_input(Inputs.Scorer, OptimizationScorer).get_name()
        scores = self.context.get_logs(PromptScoringLog)
        early_stop = self.get_input(Inputs.EarlyStop, EarlyStopConfig)
        best_score = max(scores, key=lambda s: s.scores[score_name] * early_stop.score_sign)
        evaluation_log = self.context.get_log(best_score.evaluation_log_id)
        assert isinstance(evaluation_log, PromptEvaluationLog)
        return evaluation_log.prompt


def get_tag(value, tag_name):
    match = re.search(rf"<{tag_name}>(.*?)</{tag_name}>", value, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


class SimplePromptOptimizer(PromptOptimizerStrategy):
    __registry_alias__: ClassVar = "simple"

    optimizer_prompt: str = (
        "I'm using llm to do {task}. Here is my prompt <prompt>{prompt}</prompt>. "
        "Please make it better so I can have better results. "
        "{instructions} "
        # "Do not add new classes. "
        "Return new version inside <new_prompt> tag"
    )
    return_tag: str = "new_prompt"

    async def run(self, prompt: str, context: OptimizerContext) -> PromptOptimizationLog:
        task = context.get_input(Inputs.Task) or "task"
        instructions = context.get_input(Inputs.OptimizerPromptInstructions) or ""
        optimizer_prompt = self.optimizer_prompt.format(prompt=prompt, task=task, instructions=instructions)
        response = await context.llm_wrapper.complete([LLMMessage.user(optimizer_prompt)])
        new_prompt = get_tag(response.result, self.return_tag)
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=optimizer_prompt,
            new_prompt=new_prompt,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            stop=True,
        )


class _Row(NamedTuple):
    value: Optional[Any]
    target: Optional[Any]
    reasoning: Optional[Any]
    prediction: Optional[Any]
    prediction_reasoning: Optional[Any]


def iter_mistakes(context: OptimizerContext) -> Iterator[_Row]:
    last_eval = context.get_last_log(PromptEvaluationLog)
    if last_eval is None:
        raise ValueError("Prompt was not evaluated")
    try:
        target = last_eval.get_data(Inputs.Target)
    except KeyError:
        target = context.get_input(Inputs.Target, missing_error_message="Need target input to filter failed rows")

    preds = last_eval.get_data(Inputs.Pred)
    df = pd.DataFrame({Inputs.Pred: preds})
    df[Inputs.Target] = target
    df[Inputs.Values] = context.get_input(Inputs.Values)
    df[Inputs.Reasoning] = context.get_input(Inputs.Reasoning)
    df[Inputs.PredReasoning] = (
        last_eval.get_data(Inputs.PredReasoning) if last_eval.has_data(Inputs.PredReasoning) else ""
    )
    for _, row in df[preds != target].iterrows():
        yield _Row(
            row[Inputs.Values],
            row[Inputs.Target],
            row[Inputs.Reasoning],
            row[Inputs.Pred],
            row[Inputs.PredReasoning],
        )


class FeedbackStrategy(PromptOptimizerStrategy):
    __registry_alias__: ClassVar = "feedback"

    add_feedback_prompt = (
        "I ran LLM for some inputs to do {task} and it made some mistakes. "
        "Here is my original prompt <prompt>{prompt}</prompt>. "
        "And here are rows where LLM made mistakes: <rows>{rows}</rows>. "
        "Please update my prompt to improve LLM quality. "
        "Generalize examples to not overfit on them. "
        "{instructions} "
        "Return new prompt inside <new_prompt> tag"
    )
    row_template = """<input>{input}</input>
    <true_label>{true_label}</true_label>
    <llm_judge_label>{llm_judge_label}</llm_judge_label>
    <human_reasoning>{human_reasoning}</human_reasoning>
    <llm_judge_reasoning>{llm_judge_reasoning}</llm_judge_reasoning>
    """

    async def run(self, prompt: str, context: OptimizerContext) -> PromptOptimizationLog:
        rows = "\n".join(
            self.row_template.format(
                input=row.value,
                true_label=row.target,
                llm_judge_label=row.prediction,
                human_reasoning=row.reasoning,
                llm_judge_reasoning=row.prediction_reasoning,
            )
            for row in iter_mistakes(context)
        )
        optimizer_prompt = self.add_feedback_prompt.format(
            prompt="{prompt}", task="{task}", instructions="{instructions}", rows=rows
        )
        log = await SimplePromptOptimizer(optimizer_prompt=optimizer_prompt).run(prompt, context)
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=optimizer_prompt,
            new_prompt=log.new_prompt,
            input_tokens=log.input_tokens,
            output_tokens=log.output_tokens,
            stop=False,
        )

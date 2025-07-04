import re
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import Dataset
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently.core.datasets import LLMClassification
from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate
from evidently.legacy.features.llm_judge import LLMJudge
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.base import LLMMessage
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.optimization.optimizer import BaseOptimizer
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
        return f"Prompt '{self.input_prompt[:40]}' optimized to '{self.new_prompt[:40]}'"


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
        data[Inputs.Pred] = prediction
        data[Inputs.PredReasoning] = prediction_reasoning
        data[Inputs.PredScores] = prediction_scores
        super().__init__(prompt=prompt, data=data, **kwargs)

    def message(self) -> str:
        lens = " ".join(f"{k}({len(v)})" for k, v in self.data.items() if v is not None)
        return f"Evaluated prompt '{self.prompt[:40]}...', got {lens}"


class PromptEvaluator(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "prompt_evaluator"

    @abstractmethod
    def evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        raise NotImplementedError()

    @abstractmethod
    def get_base_prompt(self) -> Optional[str]:
        raise NotImplementedError()


class BinaryLLMJudgePromptEvaluator(PromptEvaluator):
    judge: LLMJudge

    def evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
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
    def template(self) -> BinaryClassificationPromptTemplate:
        t = self.judge.template
        assert isinstance(t, BinaryClassificationPromptTemplate)
        return t

    def get_base_prompt(self) -> str:
        return self.template.criteria


CustomEvaluatorCallable = Callable[[str], PromptEvaluationLog]


class CallablePromptEvaluator(PromptEvaluator):
    func: str
    _func: Optional[CustomEvaluatorCallable] = PrivateAttr(None)

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

    def evaluate(self, prompt: str, dataset: Dataset, options: Options) -> PromptEvaluationLog:
        return self._func(prompt)

    def get_base_prompt(self) -> Optional[str]:
        return None


AnyPromptEvaluator = Union[PromptEvaluator, LLMJudge, CustomEvaluatorCallable]


def get_prompt_evaluator(value: AnyPromptEvaluator) -> PromptEvaluator:
    if isinstance(value, PromptEvaluator):
        return value
    if isinstance(value, LLMJudge) and isinstance(value.template, BinaryClassificationPromptTemplate):
        return BinaryLLMJudgePromptEvaluator(judge=value)
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

    @abstractmethod
    def score(self, context: OptimizerContext, evaluation: PromptEvaluationLog) -> Optional[float]:
        raise NotImplementedError()


StrOptimizationScorer = Union[str, OptimizationScorer]


class AccuracyScorer(OptimizationScorer):
    __registry_alias__: ClassVar = "accuracy"

    def score(self, context: OptimizerContext, evaluation: PromptEvaluationLog) -> Optional[float]:
        if Inputs.Target not in context.inputs or Inputs.Pred not in evaluation.data:
            # todo: error?
            return None
        target = context.inputs[Inputs.Target]
        result = evaluation.data[Inputs.Pred]
        return (result == target).mean()


class EarlyStopConfig(BaseModel):
    bigger_score_better: bool = True
    max_iterations: int = 5
    min_score_gain: float = 0.01
    main_score_name: Optional[str] = None

    @property
    def _score_sign(self):
        return 1 if self.bigger_score_better else -1

    def should_stop(self, logs: List[OptimizerLog]) -> Optional[float]:
        if sum(1 for _ in logs if isinstance(_, PromptOptimizationLog)) > self.max_iterations:
            return True
        scores = list(log for log in logs if isinstance(log, PromptScoringLog))
        if len(scores) > 1:
            prev_score, last_score = scores[-2:]
            score_name = self.main_score_name or next(iter(prev_score.scores))
            if (last_score.scores[score_name] - prev_score.scores[score_name]) * self._score_sign < self.min_score_gain:
                return True
        return False


class PromptOptimizer(BaseOptimizer[PromptOptimizerConfig]):
    def __init__(self, name: str, strategy: Union[str, PromptOptimizerStrategy], checkpoint_path: Optional[str] = None):
        strategy = PromptOptimizerStrategy.registry_lookup(strategy)
        super().__init__(name, PromptOptimizerConfig(strategy=strategy), checkpoint_path=checkpoint_path)

    def run_sync(
        self,
        dataset: Dataset,
        evaluator: AnyPromptEvaluator,
        scorer: Optional[StrOptimizationScorer],
        options: AnyOptions = None,
    ) -> Optional[PromptOptimizationLog]:
        return async_to_sync(self.run(dataset, evaluator, scorer, options))

    async def run(
        self,
        dataset: Dataset,
        evaluator: AnyPromptEvaluator,
        scorer: Optional[StrOptimizationScorer],
        options: AnyOptions = None,
        early_stop: Optional[EarlyStopConfig] = None,
    ) -> Optional[PromptOptimizationLog]:
        self.set_input_dataset(dataset)
        evaluator = get_prompt_evaluator(evaluator)
        self.set_input(Inputs.Evaluator, evaluator)
        self.set_input(Inputs.Options, Options.from_any_options(options))
        if scorer is None:
            scorer = AccuracyScorer()
        self.set_input(Inputs.Scorer, OptimizationScorer.registry_lookup(scorer))
        self.set_input(Inputs.EarlyStop, early_stop or EarlyStopConfig())

        await self.resume()

    async def resume(self):
        evaluator = self.get_input(Inputs.Evaluator, PromptEvaluator)
        scorer = self.get_input(Inputs.Scorer, OptimizationScorer)

        prompt = evaluator.get_base_prompt()
        if prompt is None:
            prompt = self.get_input(
                Inputs.BasePrompt, str, f"'{Inputs.BasePrompt}' input is required for {evaluator.__class__.__name__}"
            )
        early_stop = self.get_input(Inputs.EarlyStop, EarlyStopConfig)

        stop = False
        self._eval_score(prompt, evaluator, scorer)
        while not stop:
            opt_log = await self.config.strategy.run(prompt, self.context)
            self.context.add_log(opt_log)
            prompt = opt_log.new_prompt
            self._eval_score(prompt, evaluator, scorer)
            stop = opt_log.stop or early_stop.should_stop(self.context.logs)

    def _eval_score(self, prompt: str, evaluator: PromptEvaluator, scorer: OptimizationScorer):
        eval_log = evaluator.evaluate(prompt, self.dataset, self.context.options)
        self.context.add_log(eval_log)
        score = scorer.score(self.context, eval_log)
        score_log = PromptScoringLog(evaluation_log_id=eval_log.id, scores={scorer.__class__.__name__: score})
        self.context.add_log(score_log)

    @property
    def config(self) -> PromptOptimizerConfig:
        return self.context.config

    @property
    def dataset(self) -> Dataset:
        clf = self.get_input(Inputs.LLMClassification, LLMClassification)
        return Dataset.from_pandas(
            pd.DataFrame(
                {
                    clf.values: list(self.get_input(Inputs.Values, pd.Series)),
                    clf.target: list(self.get_input(Inputs.Target, pd.Series)),
                }
            )
        )

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


def get_tag(value, tag_name):
    match = re.search(rf"<{tag_name}>(.*?)</{tag_name}>", value, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


class SimplePromptOptimizer(PromptOptimizerStrategy):
    __registry_alias__: ClassVar = "simple"

    optimizer_prompt: str = (
        "I'm using llm to classify texts. Here is my prompt <prompt>{prompt}</prompt>. "
        "Please make it better so I can have better classification quality. "
        "Do not add new classes. "
        "Return new version inside <new_prompt> tag"
    )
    return_tag: str = "new_prompt"

    async def run(self, prompt: str, state: OptimizerContext) -> PromptOptimizationLog:
        response = await state.llm_wrapper.complete([LLMMessage.user(self.optimizer_prompt.format(prompt=prompt))])
        new_prompt = get_tag(response.result, self.return_tag)
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=self.optimizer_prompt,
            new_prompt=new_prompt,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            stop=True,
        )


class FeedbackStrategy(PromptOptimizerStrategy):
    __registry_alias__: ClassVar = "feedback"

    add_feedback_prompt = (
        "I ran LLM judge for some inputs and it made some mistakes. "
        "Here is my original prompt <prompt>{prompt}</prompt>. "
        "And here are rows where LLM made mistakes: <rows>{rows}</rows>. "
        "Please update my prompt to improve LLM judge quality. "
        "Generalize examples to not overfit on them. "
        "Return new prompt inside <new_prompt> tag"
    )
    row_template = """<input>{input}</input>
    <true_label>{true_label}</true_label>
    <llm_judge_label>{llm_judge_label}</llm_judge_label>
    <human_reasoning>{human_reasoning}</human_reasoning>
    <llm_judge_reasoning>{llm_judge_reasoning}</llm_judge_reasoning>
    """

    async def run(self, prompt: str, state: OptimizerContext) -> PromptOptimizationLog:
        mistakes = state.mistakes
        rows = "\n".join(
            self.row_template.format(
                input=val,
                true_label=gt,
                llm_judge_label=pred,
                human_reasoning=gt_reason,
                llm_judge_reasoning=pred_reason,
            )
            for val, gt, pred, gt_reason, pred_reason in zip(
                mistakes.values, mistakes.target, mistakes.preds, mistakes.reasoning, mistakes.preds_reasoning
            )
        )
        optimizer_prompt = self.add_feedback_prompt.format(prompt="{prompt}", rows=rows)
        log = await SimplePromptOptimizer(optimizer_prompt=optimizer_prompt).run(prompt, state)
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=optimizer_prompt,
            new_prompt=log.new_prompt,
            input_tokens=log.input_tokens,
            output_tokens=log.output_tokens,
            stop=False,
        )

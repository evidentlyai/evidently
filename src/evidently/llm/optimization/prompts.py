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

from evidently import ColumnType
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
from evidently.legacy.utils.data_preprocessing import ColumnDefinition
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.legacy.utils.llm.base import LLMMessage
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.optimization.errors import OptimizationConfigurationError
from evidently.llm.optimization.errors import OptimizationError
from evidently.llm.optimization.errors import OptimizationRuntimeError
from evidently.llm.optimization.optimizer import BaseOptimizer
from evidently.llm.optimization.optimizer import InitContextMixin
from evidently.llm.optimization.optimizer import LogID
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerContext
from evidently.llm.optimization.optimizer import OptimizerLog
from evidently.llm.optimization.optimizer import Params
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.arg_type_registry import BaseArgTypeRegistry


class PromptOptimizationLog(OptimizerLog):
    """Log entry for a single prompt optimization step."""

    input_prompt: str
    optimizer_prompt: str
    new_prompt: str
    input_tokens: int
    output_tokens: str
    stop: bool

    def message(self) -> str:
        return f"Prompt '{self.input_prompt[:40]}...' optimized to '{self.new_prompt[:40]}...'"


class PromptOptimizerStrategy(BaseArgTypeRegistry, AutoAliasMixin, EvidentlyBaseModel, ABC):
    """Abstract base class for prompt optimization strategies."""

    __alias_type__: ClassVar = "prompt_optimizer_strategy"

    class Config:
        is_base_type = True

    @abstractmethod
    async def run(self, prompt: str, context: OptimizerContext) -> PromptOptimizationLog:
        """Run the optimization strategy for a given prompt and context."""
        raise NotImplementedError()


class PromptOptimizerConfig(OptimizerConfig):
    """Configuration for prompt optimizers, including the strategy."""

    strategy: PromptOptimizerStrategy


class PromptExecutionLog(OptimizerLog):
    """Log entry for prompt execution results."""

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
        data.setdefault(Params.Pred, prediction)
        data.setdefault(Params.PredScores, prediction_scores)
        data.setdefault(Params.PredReasoning, prediction_reasoning)
        super().__init__(prompt=prompt, data=data, **kwargs)

    def message(self) -> str:
        lens = " ".join(f"{k}({len(v)})" for k, v in self.data.items() if v is not None)
        return f"Executed prompt '{self.prompt[:40]}...', got {lens}"

    def get_data(self, name: str) -> pd.Series:
        val = self.data.get(name, None)
        if val is None:
            raise KeyError(f"Execution result data does not contain {name}")
        return val

    def has_data(self, name: str) -> bool:
        return self.data.get(name, None) is not None


def get_classification_dataset(context: OptimizerContext) -> Dataset:
    clf = context.get_param(Params.LLMClassification, LLMClassification, "Missing LLMClassification param")
    return Dataset.from_pandas(
        pd.DataFrame(
            {
                clf.input: list(context.get_param(Params.InputValues, pd.Series)),
                clf.target: list(context.get_param(Params.Target, pd.Series)),
            }
        )
    )


class PromptExecutor(AutoAliasMixin, EvidentlyBaseModel, InitContextMixin, ABC):
    """Abstract base class for prompt executors."""

    __alias_type__: ClassVar = "prompt_executor"

    class Config:
        is_base_type = True

    @abstractmethod
    def execute(self, prompt: str, context: OptimizerContext) -> PromptExecutionLog:
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
        context.set_param(Params.Task, self.get_task())
        instructions = self.get_optimizer_instructions()
        if instructions is not None:
            context.set_param(Params.OptimizerPromptInstructions, instructions)


AnyJudgeTemplate = Union[BinaryClassificationPromptTemplate, MulticlassClassificationPromptTemplate]


class LLMJudgePromptExecutor(PromptExecutor):
    """Prompt executor that runs an LLMJudge."""

    judge: LLMJudge

    def execute(self, prompt: str, context: OptimizerContext) -> PromptExecutionLog:
        dataset = get_classification_dataset(context)
        options = context.options
        try:
            template = self.template
            judge = self.judge.update(template=template.update(criteria=prompt))
            dd = dataset.data_definition
            generated = judge.generate_features_renamed(
                dataset.as_dataframe(),
                data_definition=DataDefinition(
                    columns={
                        col: ColumnDefinition(col, dd.get_column_type(col)) for col in dd.get_columns(list(ColumnType))
                    },
                    target=None,
                    prediction_columns=None,
                    id_column=None,
                    datetime_column=None,
                    embeddings=None,
                    user_id=None,
                    item_id=None,
                    task=None,
                    classification_labels=None,
                    reference_present=False,
                    recommendations_type=None,
                ),
                options=options,
            )
            cols = judge.list_columns()
            category = (
                generated[[c.name for c in cols if "category" in c.name][0]] if template.include_category else None
            )
            score = generated[[c.name for c in cols if "score" in c.name][0]] if template.include_score else None
            reasoning = (
                generated[[c.name for c in cols if "reasoning" in c.name][0]] if template.include_reasoning else None
            )
            return PromptExecutionLog(
                prompt=prompt,
                data={
                    Params.Pred: category,
                    Params.PredReasoning: reasoning,
                    Params.PredScores: score,
                },
            )
        except Exception as e:
            raise OptimizationRuntimeError(f"LLMJudgePromptEexecutor failed: {e}")

    @property
    def template(self) -> AnyJudgeTemplate:
        t = self.judge.template
        assert isinstance(t, (BinaryClassificationPromptTemplate, MulticlassClassificationPromptTemplate))
        return t

    def get_base_prompt(self) -> str:
        return self.template.criteria

    def get_task(self) -> str:
        return "classify texts"

    def get_optimizer_instructions(self) -> Optional[str]:
        return "Do not add new classes."


CustomExecutorCallable = Callable[[str, OptimizerContext], PromptExecutionLog]


class CallablePromptExecutor(PromptExecutor):
    """Prompt executor that wraps a callable function."""

    func: str
    _func: Optional[CustomExecutorCallable] = PrivateAttr(None)
    task: Optional[str] = None

    def __init__(
        self,
        func: Union[str, CustomExecutorCallable],
    ):
        if callable(func):
            self._func = func
            func = f"{func.__module__}.{func.__name__}"
        else:
            self._func = None
        self.func = func
        super().__init__()

    def execute(self, prompt: str, context: OptimizerContext) -> PromptExecutionLog:
        if self._func is None:
            raise OptimizationConfigurationError(f"No function set for CallablePromptExecutor: {self.func}")
        return self._func(prompt, context)

    def get_base_prompt(self) -> Optional[str]:
        return None

    def get_task(self) -> str:
        if self.task is not None:
            return self.task
        doc = self._func.__doc__
        if doc is None:
            warnings.warn(f"Please add docstring to {self.func} describing task you are trying to optimize.")
        return doc or ""


AnyPromptExecutor = Union[PromptExecutor, LLMJudge, CustomExecutorCallable]


def get_prompt_executor(value: AnyPromptExecutor) -> PromptExecutor:
    """Convert a value to a PromptExecutor, if possible."""
    if isinstance(value, PromptExecutor):
        return value
    if isinstance(value, LLMJudge) and isinstance(
        value.template, (BinaryClassificationPromptTemplate, MulticlassClassificationPromptTemplate)
    ):
        return LLMJudgePromptExecutor(judge=value)
    if (
        isinstance(value, FeatureDescriptor)
        and isinstance(value.feature, LLMJudge)
        and isinstance(
            value.feature.template, (BinaryClassificationPromptTemplate, MulticlassClassificationPromptTemplate)
        )
    ):
        return LLMJudgePromptExecutor(judge=value.feature)
    if callable(value):
        # todo: check signature
        return CallablePromptExecutor(value)
    raise NotImplementedError(f"Not implemented for {value.__class__.__name__}")


class PromptScoringLog(OptimizerLog):
    """Log entry for prompt scoring results."""

    execution_log_id: LogID
    scores: Dict[str, float]

    def message(self) -> str:
        return "Prompt scored: " + ", ".join(f"{k}: {v}" for k, v in self.scores.items())


class OptimizationScorer(BaseArgTypeRegistry, AutoAliasMixin, EvidentlyBaseModel, ABC):
    """Abstract base class for optimization scorers."""

    __alias_type__: ClassVar = "optimizer_scorer"

    class Config:
        is_base_type = True

    def get_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        raise NotImplementedError()

    async def score(self, context: OptimizerContext, execution_log: PromptExecutionLog) -> Optional[float]:
        target: Any = context.get_param(Params.Target, missing_error_message=f"{self.get_name()} requires target input")
        predictions = execution_log.get_data(Params.Pred)
        if not isinstance(target, pd.Series):
            target = pd.Series([target for _ in range(len(predictions))])
        return await self._score(predictions, target, context.options)


AnyOptimizationScorer = Union[str, OptimizationScorer, Any]


def get_scorer(scorer: AnyOptimizationScorer) -> OptimizationScorer:
    """Convert a value to an OptimizationScorer, if possible."""
    if isinstance(scorer, str):
        return OptimizationScorer.registry_lookup(scorer)
    if isinstance(scorer, OptimizationScorer):
        return scorer
    if isinstance(scorer, LLMJudge) and isinstance(scorer.template, BinaryClassificationPromptTemplate):
        return BinaryJudgeScorer(judge=scorer)
    if (
        isinstance(scorer, FeatureDescriptor)
        and isinstance(scorer.feature, LLMJudge)
        and isinstance(scorer.feature.template, BinaryClassificationPromptTemplate)
    ):
        return BinaryJudgeScorer(judge=scorer.feature)
    raise NotImplementedError(f"Not implemented for {scorer.__class__.__name__}")


class BinaryJudgeScorer(OptimizationScorer):
    """Scorer that uses a binary LLMJudge for scoring."""

    judge: LLMJudge
    scorer: Optional[OptimizationScorer] = None

    async def score(self, context: OptimizerContext, execution_log: PromptExecutionLog) -> Optional[float]:
        try:
            predictions = execution_log.get_data(Params.Pred)
            judge = self.judge
            template = judge.template
            if not isinstance(template, BinaryClassificationPromptTemplate):
                raise OptimizationConfigurationError("Judge scorer only supports binary classification")
            judge.update(template=template.update(include_category=True, include_reasoning=True, include_score=False))
            input_columns = judge.get_input_columns()
            if len(input_columns) > 1:
                raise OptimizationConfigurationError("Judge scorer only supports one input column")
            input_column = next(iter(input_columns))
            generated = judge.generate_features_renamed(
                pd.DataFrame({input_column: predictions}),
                data_definition=DataDefinition(
                    columns={input_column: ColumnDefinition(input_column, ColumnType.Text)},
                    target=None,
                    prediction_columns=None,
                    id_column=None,
                    datetime_column=None,
                    embeddings=None,
                    user_id=None,
                    item_id=None,
                    task=None,
                    classification_labels=None,
                    reference_present=False,
                    recommendations_type=None,
                ),
                options=context.options,
            )
            cols = judge.list_columns()
            category = (
                generated[[c.name for c in cols if "category" in c.name][0]] if template.include_category else None
            )
            reasoning = (
                generated[[c.name for c in cols if "reasoning" in c.name][0]] if template.include_reasoning else None
            )
            assert category is not None
            scorer = self.scorer or AccuracyScorer()
            target = pd.Series([template.target_category] * len(predictions))
            execution_log.data[Params.Target] = target
            execution_log.data[Params.PredReasoning] = reasoning
            return await scorer._score(category, target=target, options=context.options)
        except Exception as e:
            raise OptimizationRuntimeError(f"BinaryJudgeScorer failed: {e}") from e

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        raise NotImplementedError()


class AccuracyScorer(OptimizationScorer):
    """Scorer that computes accuracy of predictions."""

    __registry_alias__: ClassVar = "accuracy"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return (predictions == target).mean()


class EarlyStopConfig(BaseModel):
    """Configuration for early stopping during optimization."""

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
        score_name = context.get_param(Params.Scorer, OptimizationScorer).get_name()
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
    """Main class for running prompt optimization using a given strategy."""

    def __init__(self, name: str, strategy: Union[str, PromptOptimizerStrategy], checkpoint_path: Optional[str] = None):
        strategy = PromptOptimizerStrategy.registry_lookup(strategy)
        super().__init__(name, PromptOptimizerConfig(strategy=strategy), checkpoint_path=checkpoint_path)

    def run(
        self,
        executor: AnyPromptExecutor,
        scorer: Optional[AnyOptimizationScorer],
        options: AnyOptions = None,
    ):
        async_to_sync(self.arun(executor, scorer, options))

    async def arun(
        self,
        executor: AnyPromptExecutor,
        scorer: Optional[AnyOptimizationScorer],
        options: AnyOptions = None,
        early_stop: Optional[EarlyStopConfig] = None,
    ):
        """Run the optimizer"""
        executor = get_prompt_executor(executor)
        self.set_param(Params.Executor, executor)
        self.set_param(Params.Options, Options.from_any_options(options))
        if scorer is None:
            scorer = AccuracyScorer()
        self.set_param(Params.Scorer, get_scorer(scorer))
        self.set_param(Params.EarlyStop, early_stop or EarlyStopConfig())
        self._lock()
        await self.resume()

    def _get_prompt(self) -> str:
        """Get the current prompt for optimization, using logs or executor base prompt."""
        log = self.context.get_last_log(PromptOptimizationLog)
        if log is not None:
            return log.new_prompt
        executor = self.get_param(Params.Executor, PromptExecutor)
        prompt = executor.get_base_prompt()
        if prompt is not None:
            return prompt
        return self.get_param(
            Params.BasePrompt, str, f"'{Params.BasePrompt}' input is required for {executor.__class__.__name__}"
        )

    async def resume(self):
        """Resume optimization from the current state."""
        executor = self.get_param(Params.Executor, PromptExecutor)
        scorer = self.get_param(Params.Scorer, OptimizationScorer)
        early_stop = self.get_param(Params.EarlyStop, EarlyStopConfig)
        prompt = self._get_prompt()
        stop = False
        await self._evaluate_prompt(prompt, executor, scorer)
        while not stop:
            try:
                opt_log = await self.config.strategy.run(prompt, self.context)
                self.context.add_log(opt_log)
                prompt = opt_log.new_prompt
                await self._evaluate_prompt(prompt, executor, scorer)
                stop = opt_log.stop or early_stop.should_stop(self.context)
            except OptimizationError:
                raise
            except Exception as e:
                raise OptimizationRuntimeError(f"Error during optimization step: {e}")

    async def _evaluate_prompt(self, prompt: str, executor: PromptExecutor, scorer: OptimizationScorer):
        eval_log = executor.execute(prompt, self.context)
        self.context.add_log(eval_log)
        score = await scorer.score(self.context, eval_log)
        score_log = PromptScoringLog(execution_log_id=eval_log.id, scores={scorer.get_name(): score})
        self.context.add_log(score_log)

    @property
    def config(self) -> PromptOptimizerConfig:
        config = self.context.config
        if not isinstance(config, PromptOptimizerConfig):
            raise OptimizationConfigurationError(
                f"Wrong config type {config.__class__.__name__}, expected {PromptOptimizerConfig.__name__}"
            )
        return config

    def set_input_dataset(self, dataset: Dataset):
        dd = dataset.data_definition
        clf = dd.llm
        assert isinstance(clf, LLMClassification)
        self.set_param(Params.InputValues, dataset.column(clf.input).data)
        self.set_param(Params.Target, dataset.column(clf.target).data)
        self.set_param(Params.LLMClassification, clf)
        if clf.reasoning is not None:
            self.set_param(Params.Reasoning, dataset.column(clf.reasoning).data)
        if clf.predictions is not None:
            self.set_param(Params.Pred, dataset.column(clf.predictions).data)
        if clf.prediction_reasoning is not None:
            self.set_param(Params.PredReasoning, dataset.column(clf.prediction_reasoning).data)

    def best_prompt(self):
        """Return the best prompt found during optimization based on the scoring metric."""
        score_name = self.get_param(Params.Scorer, OptimizationScorer).get_name()
        scores = self.context.get_logs(PromptScoringLog)
        early_stop = self.get_param(Params.EarlyStop, EarlyStopConfig)
        best_score = max(scores, key=lambda s: s.scores[score_name] * early_stop.score_sign)
        execution_log = self.context.get_log(best_score.execution_log_id)
        assert isinstance(execution_log, PromptExecutionLog)
        return execution_log.prompt


def get_tag(value, tag_name):
    """Extract the content of a tag from a string value."""
    match = re.search(rf"<{tag_name}>(.*?)</{tag_name}>", value, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


class SimplePromptOptimizer(PromptOptimizerStrategy):
    """A simple prompt optimization strategy that asks the LLM to improve the prompt."""

    __registry_alias__: ClassVar = "simple"

    optimizer_prompt: str = (
        "I'm using llm to do {task}. Here is my prompt <prompt>{prompt}</prompt>. "
        "Please make it better so I can have better results. "
        "{instructions} "
        "Return new version inside <new_prompt> tag"
    )
    return_tag: str = "new_prompt"

    async def run(self, prompt: str, context: OptimizerContext) -> PromptOptimizationLog:
        task: str = context.get_param(Params.Task) or "task"
        instructions: str = context.get_param(Params.OptimizerPromptInstructions) or ""
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
    input: Optional[Any]
    target: Optional[Any]
    reasoning: Optional[Any]
    prediction: Optional[Any]
    prediction_reasoning: Optional[Any]


def iter_mistakes(context: OptimizerContext) -> Iterator[_Row]:
    last_eval = context.get_last_log(PromptExecutionLog)
    if last_eval is None:
        raise OptimizationRuntimeError("Prompt was not executed.")
    try:
        target = last_eval.get_data(Params.Target)
    except KeyError:
        target = context.get_param(
            Params.Target, missing_error_message=f"Need '{Params.Target}' param to filter failed rows"
        )

    preds = last_eval.get_data(Params.Pred)
    df = pd.DataFrame({Params.Pred: preds})
    df[Params.Target] = target
    df[Params.InputValues] = context.get_param(Params.InputValues)
    df[Params.Reasoning] = context.get_param(Params.Reasoning)
    df[Params.PredReasoning] = (
        last_eval.get_data(Params.PredReasoning) if last_eval.has_data(Params.PredReasoning) else ""
    )
    for _, row in df[preds != target].iterrows():
        yield _Row(
            row[Params.InputValues],
            row[Params.Target],
            row[Params.Reasoning],
            row[Params.Pred],
            row[Params.PredReasoning],
        )


class FeedbackStrategy(PromptOptimizerStrategy):
    """A feedback-based prompt optimization strategy that uses mistakes to improve prompts."""

    __registry_alias__: ClassVar = "feedback"

    add_feedback_prompt = (
        "I ran LLM for some inputs to do {task} and it made some mistakes. "
        "Here is my original prompt <prompt>\n{prompt}\n</prompt>\n"
        "And here are rows where LLM made mistakes:\n"
        "<rows>\n{rows}\n</rows>. "
        "Please update my prompt to improve LLM quality. "
        "Generalize examples to not overfit on them. "
        "{instructions} "
        "Return new prompt inside <new_prompt> tag"
    )
    row_template = """<input>{input}</input>
<target>{target}</target>
<llm_response>{llm_response}</llm_response>
<human_reasoning>{human_reasoning}</human_reasoning>
<llm_reasoning>{llm_reasoning}</llm_reasoning>
"""

    async def run(self, prompt: str, context: OptimizerContext) -> PromptOptimizationLog:
        """Run the feedback optimization strategy for a given prompt and context."""
        rows = "\n".join(
            self.row_template.format(
                input=row.input,
                target=row.target,
                llm_response=row.prediction,
                human_reasoning=row.reasoning,
                llm_reasoning=row.prediction_reasoning,
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

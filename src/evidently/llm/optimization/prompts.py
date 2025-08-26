import asyncio
import logging
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
from typing import Sequence
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
from evidently.llm.optimization.optimizer import LLMCallOptimizerLog
from evidently.llm.optimization.optimizer import LLMDataset
from evidently.llm.optimization.optimizer import LLMDatasetColumns
from evidently.llm.optimization.optimizer import LLMDatasetSplit
from evidently.llm.optimization.optimizer import LLMResultDataset
from evidently.llm.optimization.optimizer import LogID
from evidently.llm.optimization.optimizer import OptimizerConfig
from evidently.llm.optimization.optimizer import OptimizerContext
from evidently.llm.optimization.optimizer import OptimizerLog
from evidently.llm.optimization.optimizer import OptimizerRun
from evidently.llm.optimization.optimizer import Params
from evidently.llm.optimization.scorers import AccuracyScorer
from evidently.llm.optimization.scorers import OptimizationScorer
from evidently.llm.templates import Uncertainty
from evidently.llm.utils.parsing import get_tag
from evidently.llm.utils.wrapper import LLMResult
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.arg_type_registry import BaseArgTypeRegistry

logger = logging.getLogger(__name__)


class PromptOptimizationLog(LLMCallOptimizerLog):
    """Log entry for a single prompt optimization step."""

    __is_step__: ClassVar[bool] = True

    input_prompt: str
    optimizer_prompt: str
    new_prompt: str
    stop: bool

    def message(self) -> str:
        return f"Prompt '{trunc(self.input_prompt)}' optimized to '{trunc(self.new_prompt)}'"


DatasetSplitShares = Dict[str, Optional[float]]


class PromptOptimizerStrategy(BaseArgTypeRegistry, AutoAliasMixin, EvidentlyBaseModel, ABC):
    """Abstract base class for prompt optimization strategies."""

    __alias_type__: ClassVar = "prompt_optimizer_strategy"

    class Config:
        is_base_type = True

    @abstractmethod
    def get_default_scorer(self) -> "OptimizationScorer":
        raise NotImplementedError()

    def get_default_data_split_shares(self) -> DatasetSplitShares:
        """Shares of train, val and test splits. None means same as train"""
        return {}

    @abstractmethod
    async def run(self, prompt: str, run: OptimizerRun) -> PromptOptimizationLog:
        """Run the optimization strategy for a given prompt and context."""
        raise NotImplementedError()


class PromptOptimizerConfig(OptimizerConfig):
    """Configuration for prompt optimizers, including the strategy."""

    strategy: PromptOptimizerStrategy
    data_split_shares: Optional[DatasetSplitShares] = None


def trunc(msg: str, max_len: int = 40):
    if len(msg) > max_len:
        return msg[:max_len] + "..."
    return msg


class PromptExecutionLog(OptimizerLog):
    """Log entry for prompt execution results."""

    prompt: str
    result: LLMResultDataset

    def __init__(
        self,
        prompt: str,
        result: LLMResultDataset,
        **kwargs: Any,
    ) -> None:
        super().__init__(prompt=prompt, result=result, **kwargs)

    def message(self) -> str:
        lens = " ".join(f"{k}({len(v)})" for k, v in self.result.items() if v is not None)
        return f"Executed prompt '{trunc(self.prompt)}', got {lens}"

    def full_message(self):
        return f"Executed prompt '{self.prompt}'"


def get_classification_dataset(context: OptimizerContext) -> Dataset:
    clf = context.get_param(Params.LLMClassification, LLMClassification, "Missing LLMClassification param")
    dataset = context.get_param(Params.Dataset, LLMDataset, "Missing LLMDataset param")
    values = dataset.input_values
    target = dataset.target
    if target is None:
        raise OptimizationConfigurationError("Target is required for judge executor")
    return Dataset.from_pandas(
        pd.DataFrame(
            {
                clf.input: list(values),
                clf.target: list(target),
            }
        )
    )


class PromptExecutor(AutoAliasMixin, EvidentlyBaseModel, InitContextMixin, ABC):
    """Abstract base class for prompt executors."""

    __alias_type__: ClassVar = "prompt_executor"

    class Config:
        is_base_type = True

    @abstractmethod
    def execute(self, prompt: str, run: OptimizerRun) -> PromptExecutionLog:
        raise NotImplementedError()

    @abstractmethod
    def get_base_prompt(self) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_task(self) -> str:
        raise NotImplementedError()

    def get_optimizer_instructions(self) -> Optional[str]:
        return None

    def on_param_set(self, context: OptimizerContext):
        context.set_param(Params.Task, self.get_task())
        instructions = self.get_optimizer_instructions()
        if instructions is not None:
            context.set_param(Params.OptimizerPromptInstructions, instructions)

    async def start(self, run: OptimizerRun):
        pass

    @abstractmethod
    def get_best_result(self, prompt: str, context: OptimizerContext):
        raise NotImplementedError()


AnyJudgeTemplate = Union[BinaryClassificationPromptTemplate, MulticlassClassificationPromptTemplate]


class LLMJudgePromptExecutor(PromptExecutor):
    """Prompt executor that runs an LLMJudge."""

    judge: LLMJudge

    def _make_judge(self, prompt: str) -> LLMJudge:
        judge = self.judge.update(template=self.template.update(criteria=prompt))
        return judge

    def execute(self, prompt: str, run: OptimizerRun) -> PromptExecutionLog:
        dataset = get_classification_dataset(run.context)
        options = run.context.options
        try:
            template = self.template
            judge = self._make_judge(prompt)
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
                result=LLMResultDataset(
                    predictions=category,
                    reasoning=reasoning,
                    scores=score,
                ),
            )
        except Exception as e:
            raise OptimizationRuntimeError(f"LLMJudgePromptExecutor failed: {e}")

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

    def get_best_result(self, prompt: str, context: OptimizerContext):
        return self._make_judge(prompt)


CustomExecutorCallable = Callable[[str, OptimizerContext], Union[PromptExecutionLog, Sequence[Any], pd.Series]]


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

    def execute(self, prompt: str, run: OptimizerRun) -> PromptExecutionLog:
        if self._func is None:
            raise OptimizationConfigurationError(f"No function set for CallablePromptExecutor: {self.func}")
        result = self._func(prompt, run.context)
        if not isinstance(result, PromptExecutionLog):
            result = PromptExecutionLog(
                prompt=prompt,
                result=LLMResultDataset(
                    predictions=pd.Series(result),
                ),
            )
        return result

    def get_base_prompt(self) -> Optional[str]:
        return None

    def get_task(self) -> str:
        if self.task is not None:
            return self.task
        doc = self._func.__doc__
        if doc is None:
            warnings.warn(f"Please add docstring to {self.func} describing task you are trying to optimize.")
        return doc or ""

    def get_best_result(self, prompt: str, context: OptimizerContext):
        def best_result():
            return self._func(prompt, context)

        return best_result


class NoopPromptExecutor(PromptExecutor):
    """Prompt executor that does nothing."""

    def get_base_prompt(self) -> Optional[str]:
        return None

    def get_task(self) -> str:
        return ""

    def execute(self, prompt: str, run: OptimizerRun) -> PromptExecutionLog:
        return PromptExecutionLog(
            prompt=prompt,
            result=LLMResultDataset(
                predictions=None,
                reasoning=None,
                scores=None,
            ),
        )

    def get_best_result(self, prompt: str, context: OptimizerContext):
        return None


class InitGenerationLog(LLMCallOptimizerLog):
    kind: str
    value: str

    def message(self) -> str:
        return f"Generated initial {self.kind}: `{self.value}`"


class BlankLLMJudge(PromptExecutor):
    kind: str = ""

    def execute(self, prompt: str, run: OptimizerRun) -> PromptExecutionLog:
        if prompt == "":
            prompt = self.sub_executor.get_base_prompt()
        result = self.sub_executor.execute(prompt, run)
        return result.update(prompt=prompt)

    def get_base_prompt(self) -> Optional[str]:
        return ""

    def get_task(self) -> str:
        return ""

    def get_best_result(self, prompt: str, context: OptimizerContext):
        return self.sub_executor.get_best_result(prompt, context)

    _sub_executor: LLMJudgePromptExecutor = PrivateAttr(None)

    @property
    def sub_executor(self) -> LLMJudgePromptExecutor:
        if self._sub_executor is None:
            raise OptimizationRuntimeError("Sub executor is not set for BlankLLMJudge")
        return self._sub_executor

    async def start(self, run: OptimizerRun):
        await self._ensure_sub_executor(run)

    async def _ensure_sub_executor(self, run: OptimizerRun):
        if self._sub_executor is None:
            judge = await self._build_judge(run)
            self._sub_executor = LLMJudgePromptExecutor(judge=judge)

    async def _build_judge(self, run: OptimizerRun) -> LLMJudge:
        context = run.context
        dataset = context.get_param(Params.Dataset, LLMDataset)
        target = dataset.target
        if target is None:
            raise OptimizationConfigurationError("Target is required for BlankLLMJudge executor")
        inputs = dataset.input_values
        labels = target.unique()
        model = context.config.model
        provider = context.config.provider
        if len(labels) < 2:
            raise OptimizationConfigurationError(f"Cannot create judge, target column has {len(labels)} labels")
        if len(labels) == 2:
            target_category, non_target_category = list(labels)
            criteria = await self._generate_binary_criteria(target_category, non_target_category, run)
            template = BinaryClassificationPromptTemplate(
                criteria=criteria,
                target_category=target_category,
                non_target_category=non_target_category,
                uncertainty=Uncertainty.UNKNOWN,
                include_category=True,
                include_reasoning=dataset.reasoning is not None,
                include_score=False,
                pre_messages=[LLMMessage.system(await self._generate_binary_system_message(criteria, run))],
            )
        else:
            raise NotImplementedError("BlankLLMJudge do not support multiclass yet")
            # template = MulticlassClassificationPromptTemplate()
        return LLMJudge(model=model, provider=provider, template=template, input_column=inputs.name)

    async def _generate_binary_criteria(self, target: str, non_target_category: str, run: OptimizerRun) -> str:
        tag = "criteria"
        binary_prompt = (
            f"I am creating binary LLM judge to classify texts. "
            f"Here is come context: {self.kind}"
            f"between two categories: '{target}' and '{non_target_category}'\n"
            f"Write a very short simple criteria for prompt for this judge. "
            f"Do not add any placeholders or specify response format in it. Return criteria inside <{tag}></{tag}> tag"
        )
        result: LLMResult[str] = await run.context.llm_wrapper.complete(
            messages=[LLMMessage.user(binary_prompt)], seed=run.seed
        )
        criteria = get_tag(result.result, tag)
        if criteria is None:
            raise OptimizationRuntimeError("Could not generate binary criteria")
        run.add_log(
            InitGenerationLog(
                kind="criteria for binary judge",
                value=criteria,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
            )
        )
        return criteria

    async def _generate_binary_system_message(self, binary_prompt: str, run: OptimizerRun) -> str:
        tag = "judge_system_message"
        system_prompt = (
            f"I am creating binary LLM judge to classify texts. "
            f"Here is my prompt: <prompt>{binary_prompt}</prompt>\n"
            f"Write a system message that will go before prompt for this judge to improve judge quality. "
            f"Make it short. "
            f"Return new system message inside <{tag}></{tag}> tag"
        )
        result: LLMResult[str] = await run.context.llm_wrapper.complete(
            messages=[LLMMessage.user(system_prompt)], seed=run.seed
        )
        sysmessage = get_tag(result.result, tag)
        if sysmessage is None:
            raise OptimizationRuntimeError("Could not generate system message")
        run.add_log(
            InitGenerationLog(
                kind="system message for binary judge",
                value=sysmessage,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
            )
        )
        return sysmessage


AnyPromptExecutor = Union[PromptExecutor, LLMJudge, CustomExecutorCallable, None]


def get_prompt_executor(value: AnyPromptExecutor) -> PromptExecutor:
    """Convert a value to a PromptExecutor, if possible."""
    if value is None:
        return NoopPromptExecutor()
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
    scores: Dict[str, Dict[str, float]]

    def get_score(self, score_name: str, split: str) -> float:
        score = self.scores[score_name]
        if split in score:
            return score[split]
        return score[LLMDatasetSplit.All]

    def message(self) -> str:
        return "Prompt scored: " + ", ".join(f"{k}: {v}" for k, v in self.scores.items())


AnyOptimizationScorer = Union[str, OptimizationScorer, None, Any]


def get_scorer(scorer: AnyOptimizationScorer) -> OptimizationScorer:
    """Convert a value to an OptimizationScorer, if possible."""
    if scorer is None:
        return NoopOptimizationScorer()
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


class NoopOptimizationScorer(OptimizationScorer):
    async def score(self, context: OptimizerContext, execution_log: PromptExecutionLog) -> Optional[Dict[str, float]]:
        return {LLMDatasetSplit.Train: 0}

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        raise NotImplementedError()


class BinaryJudgeScorer(OptimizationScorer, InitContextMixin):
    """Scorer that uses a binary LLMJudge for scoring."""

    judge: LLMJudge
    scorer: Optional[OptimizationScorer] = None

    @property
    def template(self) -> BinaryClassificationPromptTemplate:
        template = self.judge.template
        if not isinstance(template, BinaryClassificationPromptTemplate):
            raise OptimizationConfigurationError("Judge scorer only supports binary classification")
        return template

    def on_param_set(self, context: OptimizerContext):
        context.set_param(Params.TargetValue, self.template.target_category)

    async def score(self, context: OptimizerContext, execution_log: PromptExecutionLog) -> Optional[Dict[str, float]]:
        try:
            predictions = execution_log.result.get_predictions()
            judge = self.judge
            template = self.template
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
            execution_log.result.reasoning = reasoning
            fake_log = PromptExecutionLog(
                execution_log.prompt, LLMResultDataset(predictions=category, reasoning=reasoning)
            )
            return await scorer.score(context, fake_log)
        except Exception as e:
            raise OptimizationRuntimeError(f"BinaryJudgeScorer failed: {e}") from e

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        raise NotImplementedError()


class EarlyStopConfig(BaseModel):
    """Configuration for early stopping during optimization."""

    bigger_score_better: bool = True
    max_iterations: int = 5
    min_score_gain: float = 0.01
    target_score: float = 1.0

    @property
    def score_sign(self):
        return 1 if self.bigger_score_better else -1

    def should_stop(self, run: OptimizerRun) -> bool:
        if len(run.get_logs(PromptOptimizationLog)) > self.max_iterations:
            return True
        scores_log = run.get_logs(PromptScoringLog)
        score_name = run.context.get_param(Params.Scorer, OptimizationScorer).get_name()
        if len(scores_log) > 0:
            last_score = scores_log[-1]
            if last_score.get_score(score_name, LLMDatasetSplit.Val) == self.target_score:
                return True
        if len(scores_log) > 1:
            prev_score, last_score = scores_log[-2:]
            if (
                last_score.get_score(score_name, LLMDatasetSplit.Val)
                - prev_score.get_score(score_name, LLMDatasetSplit.Val)
            ) * self.score_sign < self.min_score_gain:
                return True
        return False


async def _evaluate_prompt(run: OptimizerRun, prompt: str, executor: PromptExecutor, scorer: OptimizationScorer) -> str:
    eval_log = executor.execute(prompt, run)
    run.add_log(eval_log)
    score = await scorer.score(run.context, eval_log)
    score_log = PromptScoringLog(execution_log_id=eval_log.id, scores={scorer.get_name(): score})
    run.add_log(score_log)
    return eval_log.prompt


class PromptOptimizationResultLog(OptimizerLog):
    score_log_id: LogID
    best_scores: Dict[str, float]
    step_count: int
    execution_log_id: LogID
    best_prompt: str

    def message(self) -> str:
        return f"Optimization run finished in {self.step_count} steps with best scores {self.best_scores}."


class PromptOptimizer(BaseOptimizer[PromptOptimizerConfig]):
    """Main class for running prompt optimization using a given strategy."""

    def __init__(
        self,
        name: str,
        strategy: Union[str, PromptOptimizerStrategy],
        checkpoint_path: Optional[str] = None,
        verbose: bool = False,
    ):
        strategy = PromptOptimizerStrategy.registry_lookup(strategy)
        super().__init__(
            name, PromptOptimizerConfig(strategy=strategy, verbose=verbose), checkpoint_path=checkpoint_path
        )

    def run(
        self,
        executor: AnyPromptExecutor = None,
        scorer: Optional[AnyOptimizationScorer] = None,
        dataset: Optional[Dataset] = None,
        options: AnyOptions = None,
        early_stop: Optional[EarlyStopConfig] = None,
        repetitions: int = 1,
        **params,
    ):
        async_to_sync(
            self.arun(
                executor=executor,
                scorer=scorer,
                dataset=dataset,
                options=options,
                early_stop=early_stop,
                repetitions=repetitions,
                **params,
            )
        )

    async def arun(
        self,
        executor: AnyPromptExecutor = None,
        scorer: Optional[AnyOptimizationScorer] = None,
        dataset: Optional[Dataset] = None,
        options: AnyOptions = None,
        early_stop: Optional[EarlyStopConfig] = None,
        repetitions: int = 1,
        **params,
    ):
        """Run the optimizer"""
        if dataset is not None:
            self.set_input_dataset(dataset)
        executor = get_prompt_executor(executor)
        self.set_param(Params.Executor, executor)
        self.set_param(Params.Options, Options.from_any_options(options))
        if scorer is None:
            scorer = self.config.strategy.get_default_scorer()
        self.set_param(Params.Scorer, get_scorer(scorer))
        self.set_param(Params.EarlyStop, early_stop or EarlyStopConfig())
        for param, value in params.items():
            self.set_param(param, value)
        self._lock()
        runs = []
        for _ in range(repetitions):
            runs.append(self._create_run(executor))
        await asyncio.gather(*runs)

    async def _create_run(self, executor: PromptExecutor):
        run = await self.context.new_run()
        await executor.start(run)
        await self.resume(run)
        run.add_log(self._create_result_log(run))

    def _get_prompt(self, run: OptimizerRun) -> str:
        """Get the current prompt for optimization, using logs or executor base prompt."""
        log = run.get_last_log(PromptOptimizationLog)
        if log is not None:
            return log.new_prompt
        executor = self.get_param(Params.Executor, PromptExecutor)
        prompt = executor.get_base_prompt()
        if prompt is not None:
            return prompt
        return self.get_param(
            Params.BasePrompt, str, f"'{Params.BasePrompt}' input is required for {executor.__class__.__name__}"
        )

    async def resume(self, run: OptimizerRun):
        """Resume optimization from the current state."""
        executor = self.get_param(Params.Executor, PromptExecutor)
        scorer = self.get_param(Params.Scorer, OptimizationScorer)
        early_stop = self.get_param(Params.EarlyStop, EarlyStopConfig)
        prompt = self._get_prompt(run)
        stop = False
        prompt = await _evaluate_prompt(run, prompt, executor, scorer)
        while not stop:
            try:
                opt_log = await self.config.strategy.run(prompt, run)
                run.add_log(opt_log)
                prompt = opt_log.new_prompt
                await _evaluate_prompt(run, prompt, executor, scorer)
                stop = opt_log.stop or early_stop.should_stop(run)
            except OptimizationError:
                raise
            except Exception as e:
                raise OptimizationRuntimeError(f"Error during optimization step: {e}")

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

        llm_dataset = LLMDataset(
            input_values=dataset.column(clf.input).data,
            target=dataset.column(clf.target).data,
        )
        self.set_param(Params.LLMClassification, clf)
        if clf.reasoning is not None:
            llm_dataset.reasoning = dataset.column(clf.reasoning).data
        if clf.predictions is not None:
            llm_dataset.predictions = dataset.column(clf.predictions).data
        if clf.prediction_reasoning is not None:
            llm_dataset.prediction_reasoning = dataset.column(clf.prediction_reasoning).data

        data_split_shares = self.config.data_split_shares
        if data_split_shares is None:
            data_split_shares = self.config.strategy.get_default_data_split_shares()
        llm_dataset.split(data_split_shares, seed=self.config.seed)
        self.context.set_param(Params.Dataset, llm_dataset)

    def best_prompt(self):
        """Return the best prompt found during optimization based on the scoring metric."""
        return self.best_result().best_prompt

    def best_score(self):
        return self.best_result().best_scores

    def _create_result_log(self, run: OptimizerRun) -> PromptOptimizationResultLog:
        score_name = self.get_param(Params.Scorer, OptimizationScorer).get_name()
        scores = run.get_logs(PromptScoringLog)
        early_stop = self.get_param(Params.EarlyStop, EarlyStopConfig)
        best_score: PromptScoringLog = max(
            reversed(scores), key=lambda s: s.get_score(score_name, LLMDatasetSplit.Val) * early_stop.score_sign
        )
        execution_log = run.get_log(best_score.execution_log_id)
        assert isinstance(execution_log, PromptExecutionLog)
        return PromptOptimizationResultLog(
            score_log_id=best_score.id,
            best_scores=best_score.scores[score_name],
            step_count=len(scores),
            execution_log_id=best_score.execution_log_id,
            best_prompt=execution_log.prompt,
        )

    def best_result(self) -> PromptOptimizationResultLog:
        early_stop = self.get_param(Params.EarlyStop, EarlyStopConfig)
        results = [r.get_last_log(PromptOptimizationResultLog) for r in self.context.runs]
        result = max(
            reversed([log for log in results if log is not None]),
            key=lambda s: s.best_scores.get(LLMDatasetSplit.Val, s.best_scores.get(LLMDatasetSplit.All) or 0)
            * early_stop.score_sign,
        )
        if result is None:
            raise ValueError("No best result found")
        return result

    def best_executor(self):
        executor = self.get_param(Params.Executor, PromptExecutor)
        return executor.get_best_result(self.best_prompt(), self.context)

    def print_stats(self):
        print("Optimization statistics:")
        print(f"Seed: {self.config.seed}")
        if self.has_param(Params.Dataset):
            dataset = self.get_param(Params.Dataset, LLMDataset)
            sizes = ", ".join(f"{k}: {v.sum()}" for k, v in dataset.split_masks.items())
            if not sizes:
                sizes = len(dataset.input_values)
            print(f"Dataset {sizes}")
        print(f"Runs: {len(self.context.runs)}")
        all_logs = [log for run in self.context.runs for log in run.logs.values()]
        first_log = min(run.start_time for run in self.context.runs)
        last_log = max(log.timestamp for log in all_logs)
        print(f"Total time: {(last_log - first_log).total_seconds():.2f}s")
        print(f"Total steps: {sum(1 for log in all_logs if log.__is_step__)}")
        print(
            f"Total input tokens: {sum(log.input_tokens for log in all_logs if isinstance(log, LLMCallOptimizerLog))}"
        )
        print(
            f"Total output tokens: {sum(log.output_tokens for log in all_logs if isinstance(log, LLMCallOptimizerLog))}"
        )
        best_result = self.best_result()
        print(f"Best prompt (score {best_result.best_scores}): {best_result.best_prompt}")
        print("Detailed run statistics:")
        for run in self.context.runs:
            run.print_stats()


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

    def get_default_scorer(self) -> "OptimizationScorer":
        return NoopOptimizationScorer()

    async def run(self, prompt: str, run: OptimizerRun) -> PromptOptimizationLog:
        context = run.context
        task: str = context.get_param(Params.Task) or "task"
        instructions: str = context.get_param(Params.OptimizerPromptInstructions) or ""
        optimizer_prompt = self.optimizer_prompt.format(prompt=prompt, task=task, instructions=instructions)
        response = await context.llm_wrapper.complete([LLMMessage.user(optimizer_prompt)], seed=run.seed)
        new_prompt = get_tag(response.result, self.return_tag)
        input_tokens = response.input_tokens
        output_tokens = response.output_tokens
        if new_prompt is None:
            # retry once
            response = await context.llm_wrapper.complete(
                [LLMMessage.user(optimizer_prompt)], seed=run.seed + 1 if run.seed is not None else run.seed
            )
            new_prompt = get_tag(response.result, self.return_tag)
            input_tokens += response.input_tokens
            output_tokens += response.output_tokens
        if new_prompt is None:
            raise OptimizationRuntimeError("Error parsing new prompt")
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=optimizer_prompt,
            new_prompt=new_prompt,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            stop=True,
        )


class _Row(NamedTuple):
    input: Optional[Any]
    target: Optional[Any]
    reasoning: Optional[Any]
    prediction: Optional[Any]
    prediction_reasoning: Optional[Any]


def iter_mistakes(run: OptimizerRun) -> Iterator[_Row]:
    last_eval = run.get_last_log(PromptExecutionLog)
    if last_eval is None:
        raise OptimizationRuntimeError("Prompt was not executed.")

    if run.context.has_param(Params.Dataset):
        dataset = run.context.get_param(Params.Dataset, LLMDataset)
        train_mask = dataset.get_mask(LLMDatasetSplit.Train)
        preds = last_eval.result.get_predictions(train_mask)
        target = dataset[LLMDatasetSplit.Train].target
    else:
        dataset = LLMDataset(input_values=pd.Series())
        target_value: Any = run.context.get_param(
            Params.TargetValue,
            missing_error_message="Target value is required when using feedback strategy with no dataset",
        )
        preds = last_eval.result.get_predictions()
        target = pd.Series([target_value] * len(preds))
        train_mask = pd.Series([True] * len(preds))
    if target is None:
        raise OptimizationRuntimeError("Need to provide target column to filter failed rows.")

    df = pd.DataFrame({LLMDatasetColumns.Pred: preds})
    df[LLMDatasetColumns.Target] = target
    df[LLMDatasetColumns.InputValues] = dataset[LLMDatasetSplit.Train].input_values
    df[LLMDatasetColumns.Reasoning] = dataset[LLMDatasetSplit.Train].reasoning
    df[LLMDatasetColumns.PredReasoning] = (
        last_eval.result.reasoning[train_mask] if last_eval.result.reasoning is not None else ""
    )
    for _, row in df[preds != target].iterrows():
        yield _Row(
            row[LLMDatasetColumns.InputValues],
            row[LLMDatasetColumns.Target],
            row[LLMDatasetColumns.Reasoning],
            row[LLMDatasetColumns.Pred],
            row[LLMDatasetColumns.PredReasoning],
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

    def get_default_scorer(self) -> "OptimizationScorer":
        return AccuracyScorer()

    def get_default_data_split_shares(self) -> DatasetSplitShares:
        # todo: research better defaults
        return {
            LLMDatasetSplit.Train: 0.4,
            LLMDatasetSplit.Val: 0.4,
            LLMDatasetSplit.Test: 0.2,
        }

    async def run(self, prompt: str, run: OptimizerRun) -> PromptOptimizationLog:
        """Run the feedback optimization strategy for a given prompt and context."""
        rows = "\n".join(
            self.row_template.format(
                input=row.input,
                target=row.target,
                llm_response=row.prediction,
                human_reasoning=row.reasoning,
                llm_reasoning=row.prediction_reasoning,
            )
            for row in iter_mistakes(run)
        )
        optimizer_prompt = self.add_feedback_prompt.format(
            prompt="{prompt}", task="{task}", instructions="{instructions}", rows=rows
        )
        log = await SimplePromptOptimizer(optimizer_prompt=optimizer_prompt).run(prompt, run)
        return PromptOptimizationLog(
            input_prompt=prompt,
            optimizer_prompt=optimizer_prompt,
            new_prompt=log.new_prompt,
            input_tokens=log.input_tokens,
            output_tokens=log.output_tokens,
            stop=False,
        )

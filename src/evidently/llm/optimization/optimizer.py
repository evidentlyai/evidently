import datetime
import random
import uuid
from abc import ABC
from abc import abstractmethod
from asyncio import Lock
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.core import new_id
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.wrapper import LLMWrapper
from evidently.legacy.utils.llm.wrapper import get_llm_wrapper
from evidently.llm.optimization.errors import OptimizationConfigurationError
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class Params:
    """Parameter keys used throughout the optimizer context and configuration."""

    BasePrompt = "base_prompt"
    EarlyStop = "early_stop"
    LLMClassification = "llm_classification"
    Options = "options"
    Scorer = "scorer"
    Executor = "executor"
    Dataset = "dataset"
    TargetValue = "target_value"
    Task = "task"
    OptimizerPromptInstructions = "optimizer_prompt_instructions"
    DataSplitShares = "data_split_shares"


class LLMDatasetSplit:
    Train = "train"
    Val = "val"
    Test = "test"
    All = "all"


class LLMDatasetColumns:
    InputValues = "input_values"
    Target = "target"
    Reasoning = "reasoning"
    Scores = "scores"
    Pred = "preds"
    PredReasoning = "preds_reasoning"
    PredScores = "preds_scores"


class LLMDatasetSplitView:
    def __init__(self, dataset: "LLMDataset", split_name: str):
        self.split_name = split_name
        self.dataset = dataset

    @property
    def input_values(self) -> Optional[pd.Series]:
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.input_values is None
        ):
            return self.dataset.input_values
        return self.dataset.input_values[self.dataset.split_masks[self.split_name]]

    @property
    def target(self) -> Optional[pd.Series]:
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.target is None
        ):
            return self.dataset.target
        return self.dataset.target[self.dataset.split_masks[self.split_name]]

    @property
    def reasoning(self) -> Optional[pd.Series]:
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.reasoning is None
        ):
            return self.dataset.reasoning
        return self.dataset.reasoning[self.dataset.split_masks[self.split_name]]

    @property
    def predictions(self) -> Optional[pd.Series]:
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.predictions is None
        ):
            return self.dataset.predictions
        return self.dataset.predictions[self.dataset.split_masks[self.split_name]]

    @property
    def prediction_reasoning(self) -> Optional[pd.Series]:
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.prediction_reasoning is None
        ):
            return self.dataset.prediction_reasoning
        return self.dataset.prediction_reasoning[self.dataset.split_masks[self.split_name]]


class LLMDataset(BaseModel):
    input_values: pd.Series
    target: Optional[pd.Series] = None
    reasoning: Optional[pd.Series] = None
    predictions: Optional[pd.Series] = None
    prediction_reasoning: Optional[pd.Series] = None

    split_masks: Dict[str, pd.Series] = Field(default_factory=dict)

    def __getitem__(self, split_name: str) -> LLMDatasetSplitView:
        return LLMDatasetSplitView(self, split_name)

    def get_mask(self, split_name: str) -> pd.Series:
        if split_name not in self.split_masks or split_name == LLMDatasetSplit.All:
            return pd.Series(True, index=np.arange(len(self.input_values)))
        return self.split_masks[split_name]

    def split(self, shares: Dict[str, Optional[float]], seed: Optional[int]) -> None:
        n = len(self.input_values)
        indices = np.arange(n)

        # normalize shares (ignoring None)
        specified = {k: v for k, v in shares.items() if v is not None}
        total = sum(specified.values())
        if specified and not np.isclose(total, 1.0):
            raise ValueError("Specified shares must sum to 1.0")

        remaining_indices = indices
        remaining_shares = dict(specified)

        self.split_masks = {}

        for i, (name, share) in enumerate(shares.items()):
            if share is None:
                continue

            if i == len(specified) - 1:
                split_indices = remaining_indices
            else:
                test_size = share / sum(remaining_shares.values())
                _, split_indices = train_test_split(
                    remaining_indices,
                    test_size=test_size,
                    stratify=self.target[remaining_indices] if self.target is not None else None,  # type: ignore[index]
                    random_state=seed,
                )
                remaining_indices = np.setdiff1d(remaining_indices, split_indices)
                remaining_shares.pop(name)

            mask = pd.Series(False, index=np.arange(n))
            mask.iloc[split_indices] = True
            self.split_masks[name] = mask


class LLMResultDataset(BaseModel):
    predictions: Optional[pd.Series] = None
    reasoning: Optional[pd.Series] = None
    scores: Optional[pd.Series] = None

    @property
    def has_predictions(self) -> bool:
        return self.predictions is not None

    @property
    def has_reasoning(self) -> bool:
        return self.reasoning is not None

    @property
    def has_scores(self) -> bool:
        return self.scores is not None

    def get_predictions(self, mask: Optional[pd.Series] = None) -> pd.Series:
        if self.predictions is None:
            raise KeyError("Dataset has no predictions")
        if mask is not None:
            return self.predictions[mask]
        return self.predictions

    def get_reasoning(self, mask: Optional[pd.Series] = None) -> pd.Series:
        if self.reasoning is None:
            raise KeyError("Dataset has no reasoning")
        if mask is not None:
            return self.reasoning[mask]
        return self.reasoning

    def get_scores(self, mask: Optional[pd.Series] = None) -> pd.Series:
        if self.scores is None:
            raise KeyError("Dataset has no scores")
        if mask is not None:
            return self.scores[mask]
        return self.scores

    def items(self) -> Iterable[Tuple[str, pd.Series]]:
        for field_name in self.__fields__:
            value = getattr(self, field_name)
            if isinstance(value, pd.Series):
                yield field_name, value


class OptimizerConfig(AutoAliasMixin, EvidentlyBaseModel):
    """Configuration for the optimizer, including provider and model."""

    __alias_type__: ClassVar = "optimizer_config"

    class Config:
        is_base_type = True

    provider: str = "openai"
    model: str = "gpt-4o-mini"
    verbose: bool = False
    seed: Optional[int] = None


LogID = uuid.UUID
T = TypeVar("T")


class OptimizerLog(AutoAliasMixin, EvidentlyBaseModel, ABC):
    """Base class for all optimizer logs."""

    __alias_type__: ClassVar = "optimizer_log"
    __is_step__: ClassVar[bool] = False

    class Config:
        is_base_type = True

    id: LogID = Field(default_factory=new_id)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError()

    def full_message(self):
        return self.message()


class LLMCallOptimizerLog(OptimizerLog, ABC):
    input_tokens: int
    output_tokens: int


TLog = TypeVar("TLog", bound=OptimizerLog)
LogsDict = Dict[LogID, OptimizerLog]
RunID = int


class OptimizerRun(BaseModel):
    run_id: RunID
    logs: LogsDict = {}
    seed: Optional[int]
    start_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    _context: "OptimizerContext" = PrivateAttr()

    def bind(self, context: "OptimizerContext") -> "OptimizerRun":
        self._context = context
        return self

    @property
    def context(self) -> "OptimizerContext":
        return self._context

    def add_log(self, log: OptimizerLog):
        """Add a log entry to the context and log its message."""
        if self._context.config.verbose:
            print(f"[{self.run_id}]", log.message())
        self.logs[log.id] = log

    def get_log(self, log_id: LogID) -> OptimizerLog:
        """Retrieve a log entry by its ID."""
        if log_id not in self.logs:
            raise KeyError(f"Log with id {log_id} not found")
        return self.logs[log_id]

    def get_logs(self, log_type: Type[TLog]) -> List[TLog]:
        """Get all logs of a specific type."""
        return [log for log in self.logs.values() if isinstance(log, log_type)]

    def get_last_log(self, log_type: Type[TLog]) -> Optional[TLog]:
        """Get the most recent log of a specific type, or None if not found."""
        for log in reversed(self.logs.values()):
            if isinstance(log, log_type):
                return log
        return None

    def print_stats(self):
        print(f"Optimizer Run [{self.run_id}], seed [{self.seed}]")
        log_list = list(self.logs.values())
        last_log = log_list[-1]
        print(f"Steps: {sum(1 for log in log_list if log.__is_step__)}")
        print(f"Time: {(last_log.timestamp - self.start_time).total_seconds():.1f}s")
        print("Input tokens:", sum(log.input_tokens for log in self.get_logs(LLMCallOptimizerLog)))
        print("Output tokens:", sum(log.output_tokens for log in self.get_logs(LLMCallOptimizerLog)))
        start_time = self.start_time
        for log in log_list:
            elapsed = (log.timestamp - start_time).total_seconds()
            start_time = log.timestamp
            print(f"\t[{elapsed:.1f}s] {log.full_message()}")


def get_seeded_nth_int(seed: int, n: int) -> int:
    rng = random.Random(seed)
    value = None
    for _ in range(n):
        value = rng.getrandbits(32)
    return value or seed


_run_lock = Lock()


class OptimizerContext(BaseModel):
    """Holds the state, parameters, and logs for an optimization run."""

    config: OptimizerConfig
    params: Dict[str, Any]
    runs: List[OptimizerRun]
    locked: bool = False

    # @classmethod
    # def load(cls: Type[Self], path: str) -> Self:
    #     raise NotImplementedError()
    #
    # def save(self, path: str):
    #     raise NotImplementedError()

    async def new_run(self) -> OptimizerRun:
        async with _run_lock:
            seed = None if self.config.seed is None else get_seeded_nth_int(self.config.seed, len(self.runs))
            run = OptimizerRun(run_id=len(self.runs), seed=seed).bind(self)
            self.runs.append(run)
            return run

    @property
    def llm_wrapper(self) -> LLMWrapper:
        return get_llm_wrapper(self.config.provider, self.config.model, self.params[Params.Options])

    @property
    def options(self) -> Options:
        return self.params[Params.Options]

    def set_param(self, name: str, value: Any):
        """Set a parameter in the context. Raises if context is locked."""
        if self.locked:
            raise OptimizationConfigurationError("OptimizerContext is locked")
        self.params[name] = value
        if isinstance(value, InitContextMixin):
            value.on_param_set(self)

    def get_param(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        """Get a parameter, optionally checking type and raising with a custom message if missing."""
        if not self.locked:
            raise OptimizationConfigurationError("Attempted to get param from unlocked OptimizerContext")
        value = self.params.get(name, None)
        if value is None and missing_error_message is not None:
            raise OptimizationConfigurationError(missing_error_message)
        if cls is not None and not isinstance(value, cls):
            raise OptimizationConfigurationError(f"Expected {cls.__name__}, got {type(value).__name__}")
        return value

    def lock(self):
        self.locked = True
        for value in self.params.values():
            if isinstance(value, InitContextMixin):
                value.on_context_lock(self)

    def has_param(self, name: str):
        return name in self.params


class InitContextMixin(ABC):
    """Mixin for objects that need to alter OptimizerContext on init."""

    def on_param_set(self, context: OptimizerContext):
        pass

    def on_context_lock(self, context: OptimizerContext):
        pass


TOptimizerConfig = TypeVar("TOptimizerConfig", bound=OptimizerConfig)


class BaseOptimizer(ABC, Generic[TOptimizerConfig]):
    """Base class for all optimizers, handling context and parameter management."""

    def __init__(self, name: str, config: TOptimizerConfig, checkpoint_path: Optional[str] = None):
        self.name = name
        self.checkpoint_path = checkpoint_path or f".optimizer_checkpoint_{name}"
        # if os.path.exists(self.checkpoint_path):
        #     self.context = OptimizerContext.load(self.checkpoint_path)
        #     if self.context.config != config:
        #         raise ValueError(f"Optimizer config changed, cannot load from checkpoint at {self.checkpoint_path}")
        # else:
        #     self.context = OptimizerContext(config=config, inputs={}, logs={})
        self.context = OptimizerContext(config=config, params={}, runs=[])

    def _lock(self):
        """Lock the context to prevent further parameter changes."""
        self.context.lock()

    def set_param(self, name: str, value: Any):
        """Set a parameter in the optimizer context."""
        self.context.set_param(name, value)

    def get_param(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        """Get a parameter from the optimizer context."""
        return self.context.get_param(name, cls, missing_error_message)

    def has_param(self, name: str) -> bool:
        return self.context.has_param(name)

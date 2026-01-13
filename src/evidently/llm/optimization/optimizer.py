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
    """View of a specific split in an LLM dataset.

    Provides filtered access to dataset columns for a specific split
    (train, val, test, or all).
    """

    def __init__(self, dataset: "LLMDataset", split_name: str):
        """Initialize a split view.

        Args:
        * `dataset`: `LLMDataset` to view.
        * `split_name`: Name of the split to view.
        """
        self.split_name = split_name
        self.dataset = dataset

    @property
    def input_values(self) -> Optional[pd.Series]:
        """Get input values for this split.

        Returns:
        * `pd.Series` with input values, or `None` if not available.
        """
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.input_values is None
        ):
            return self.dataset.input_values
        return self.dataset.input_values[self.dataset.split_masks[self.split_name]]

    @property
    def target(self) -> Optional[pd.Series]:
        """Get target values for this split.

        Returns:
        * `pd.Series` with target values, or `None` if not available.
        """
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.target is None
        ):
            return self.dataset.target
        return self.dataset.target[self.dataset.split_masks[self.split_name]]

    @property
    def reasoning(self) -> Optional[pd.Series]:
        """Get reasoning for this split.

        Returns:
        * `pd.Series` with reasoning, or `None` if not available.
        """
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.reasoning is None
        ):
            return self.dataset.reasoning
        return self.dataset.reasoning[self.dataset.split_masks[self.split_name]]

    @property
    def predictions(self) -> Optional[pd.Series]:
        """Get predictions for this split.

        Returns:
        * `pd.Series` with predictions, or `None` if not available.
        """
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.predictions is None
        ):
            return self.dataset.predictions
        return self.dataset.predictions[self.dataset.split_masks[self.split_name]]

    @property
    def prediction_reasoning(self) -> Optional[pd.Series]:
        """Get prediction reasoning for this split.

        Returns:
        * `pd.Series` with prediction reasoning, or `None` if not available.
        """
        if (
            self.split_name == LLMDatasetSplit.All
            or self.split_name not in self.dataset.split_masks
            or self.dataset.prediction_reasoning is None
        ):
            return self.dataset.prediction_reasoning
        return self.dataset.prediction_reasoning[self.dataset.split_masks[self.split_name]]


class LLMDataset(BaseModel):
    """Dataset for LLM optimization tasks.

    Contains input values, targets, reasoning, predictions, and split masks
    for train/val/test splits.
    """

    input_values: pd.Series
    """Input values (e.g., prompts)."""
    target: Optional[pd.Series] = None
    """Optional target values (e.g., expected outputs)."""
    reasoning: Optional[pd.Series] = None
    """Optional reasoning for targets."""
    predictions: Optional[pd.Series] = None
    """Optional model predictions."""
    prediction_reasoning: Optional[pd.Series] = None
    """Optional reasoning for predictions."""
    split_masks: Dict[str, pd.Series] = Field(default_factory=dict)
    """Dictionary mapping split names to boolean masks."""

    def __getitem__(self, split_name: str) -> LLMDatasetSplitView:
        """Get a view of a specific split.

        Args:
        * `split_name`: Name of the split to view.

        Returns:
        * `LLMDatasetSplitView` for the specified split.
        """
        return LLMDatasetSplitView(self, split_name)

    def get_mask(self, split_name: str) -> pd.Series:
        """Get the boolean mask for a split.

        Args:
        * `split_name`: Name of the split.

        Returns:
        * `pd.Series` with boolean values indicating which rows belong to this split.
        """
        if split_name not in self.split_masks or split_name == LLMDatasetSplit.All:
            return pd.Series(True, index=np.arange(len(self.input_values)))
        return self.split_masks[split_name]

    def split(self, shares: Dict[str, Optional[float]], seed: Optional[int]) -> None:
        """Split the dataset into train/val/test splits.

        Creates boolean masks for each split based on the specified shares.
        Uses stratified splitting if target values are available.

        Args:
        * `shares`: Dictionary mapping split names to proportions (must sum to 1.0).
        * `seed`: Optional random seed for reproducibility.

        Raises:
        * `ValueError`: If shares don't sum to 1.0.
        """
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
    """Dataset containing LLM optimization results.

    Stores predictions, reasoning, and scores from optimization runs.
    """

    predictions: Optional[pd.Series] = None
    """Optional model predictions."""
    reasoning: Optional[pd.Series] = None
    """Optional reasoning for predictions."""
    scores: Optional[pd.Series] = None
    """Optional scores for predictions."""

    @property
    def has_predictions(self) -> bool:
        """Check if predictions are available.

        Returns:
        * `True` if predictions exist, `False` otherwise.
        """
        return self.predictions is not None

    @property
    def has_reasoning(self) -> bool:
        """Check if reasoning is available.

        Returns:
        * `True` if reasoning exists, `False` otherwise.
        """
        return self.reasoning is not None

    @property
    def has_scores(self) -> bool:
        """Check if scores are available.

        Returns:
        * `True` if scores exist, `False` otherwise.
        """
        return self.scores is not None

    def get_predictions(self, mask: Optional[pd.Series] = None) -> pd.Series:
        """Get predictions, optionally filtered by mask.

        Args:
        * `mask`: Optional boolean mask to filter predictions.

        Returns:
        * `pd.Series` with predictions.

        Raises:
        * `KeyError`: If predictions are not available.
        """
        if self.predictions is None:
            raise KeyError("Dataset has no predictions")
        if mask is not None:
            return self.predictions[mask]
        return self.predictions

    def get_reasoning(self, mask: Optional[pd.Series] = None) -> pd.Series:
        """Get reasoning, optionally filtered by mask.

        Args:
        * `mask`: Optional boolean mask to filter reasoning.

        Returns:
        * `pd.Series` with reasoning.

        Raises:
        * `KeyError`: If reasoning is not available.
        """
        if self.reasoning is None:
            raise KeyError("Dataset has no reasoning")
        if mask is not None:
            return self.reasoning[mask]
        return self.reasoning

    def get_scores(self, mask: Optional[pd.Series] = None) -> pd.Series:
        """Get scores, optionally filtered by mask.

        Args:
        * `mask`: Optional boolean mask to filter scores.

        Returns:
        * `pd.Series` with scores.

        Raises:
        * `KeyError`: If scores are not available.
        """
        if self.scores is None:
            raise KeyError("Dataset has no scores")
        if mask is not None:
            return self.scores[mask]
        return self.scores

    def items(self) -> Iterable[Tuple[str, pd.Series]]:
        """Iterate over all Series fields.

        Yields:
        * Tuples of (field_name, pd.Series) for each Series field.
        """
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
    """LLM provider name."""
    model: str = "gpt-4o-mini"
    """LLM model name."""
    verbose: bool = False
    """Whether to print optimization progress."""
    seed: Optional[int] = None
    """Optional random seed for reproducibility."""


LogID = uuid.UUID
T = TypeVar("T")


class OptimizerLog(AutoAliasMixin, EvidentlyBaseModel, ABC):
    """Base class for all optimizer logs.

    Logs track events and steps during optimization runs.
    """

    __alias_type__: ClassVar = "optimizer_log"
    __is_step__: ClassVar[bool] = False

    class Config:
        is_base_type = True

    id: LogID = Field(default_factory=new_id)
    """Unique log identifier."""
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    """Timestamp when the log was created."""

    @abstractmethod
    def message(self) -> str:
        """Get a human-readable message for this log.

        Returns:
        * String message describing the log event.
        """
        raise NotImplementedError()

    def full_message(self):
        """Get the full message for this log.

        Returns:
        * String message (may be overridden by subclasses for additional context).
        """
        return self.message()


class LLMCallOptimizerLog(OptimizerLog, ABC):
    """Log entry for an LLM API call during optimization.

    Tracks token usage for cost monitoring and rate limiting.
    """

    input_tokens: int
    """Number of input tokens used."""
    output_tokens: int
    """Number of output tokens used."""


TLog = TypeVar("TLog", bound=OptimizerLog)
LogsDict = Dict[LogID, OptimizerLog]
RunID = int


class OptimizerRun(BaseModel):
    """A single optimization run with logs and statistics.

    Tracks all events, steps, and LLM calls during an optimization run.
    """

    run_id: RunID
    """Unique identifier for this run."""
    logs: LogsDict = {}
    """Dictionary of log entries by log ID."""
    seed: Optional[int]
    """Random seed used for this run."""
    start_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    """Timestamp when the run started."""
    _context: "OptimizerContext" = PrivateAttr()

    def bind(self, context: "OptimizerContext") -> "OptimizerRun":
        """Bind this run to an optimizer context.

        Args:
        * `context`: `OptimizerContext` to bind to.

        Returns:
        * Self for method chaining.
        """
        self._context = context
        return self

    @property
    def context(self) -> "OptimizerContext":
        """Get the optimizer context.

        Returns:
        * `OptimizerContext` associated with this run.
        """
        return self._context

    def add_log(self, log: OptimizerLog):
        """Add a log entry to the context and log its message.

        Args:
        * `log`: `OptimizerLog` to add.
        """
        if self._context.config.verbose:
            print(f"[{self.run_id}]", log.message())
        self.logs[log.id] = log

    def get_log(self, log_id: LogID) -> OptimizerLog:
        """Retrieve a log entry by its ID.

        Args:
        * `log_id`: ID of the log to retrieve.

        Returns:
        * `OptimizerLog` with the specified ID.

        Raises:
        * `KeyError`: If log ID not found.
        """
        if log_id not in self.logs:
            raise KeyError(f"Log with id {log_id} not found")
        return self.logs[log_id]

    def get_logs(self, log_type: Type[TLog]) -> List[TLog]:
        """Get all logs of a specific type.

        Args:
        * `log_type`: Type of logs to retrieve.

        Returns:
        * List of logs of the specified type.
        """
        return [log for log in self.logs.values() if isinstance(log, log_type)]

    def get_last_log(self, log_type: Type[TLog]) -> Optional[TLog]:
        """Get the most recent log of a specific type, or None if not found.

        Args:
        * `log_type`: Type of log to retrieve.

        Returns:
        * Most recent log of the specified type, or `None` if not found.
        """
        for log in reversed(self.logs.values()):
            if isinstance(log, log_type):
                return log
        return None

    def print_stats(self):
        """Print statistics about this optimization run.

        Displays run ID, seed, number of steps, elapsed time, token usage,
        and a timeline of all log events.
        """
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
    """Holds the state, parameters, and logs for an optimization run.

    Manages configuration, parameters, and multiple optimization runs.
    Can be locked to prevent parameter changes during optimization.
    """

    config: OptimizerConfig
    """Optimizer configuration."""
    params: Dict[str, Any]
    """Dictionary of optimization parameters."""
    runs: List[OptimizerRun]
    """List of completed optimization runs."""
    locked: bool = False
    """Whether the context is locked (prevents parameter changes)."""

    # @classmethod
    # def load(cls: Type[Self], path: str) -> Self:
    #     raise NotImplementedError()
    #
    # def save(self, path: str):
    #     raise NotImplementedError()

    async def new_run(self) -> OptimizerRun:
        """Create a new optimization run.

        Generates a new run with a unique ID and seed (if configured).

        Returns:
        * New `OptimizerRun` bound to this context.
        """
        async with _run_lock:
            seed = None if self.config.seed is None else get_seeded_nth_int(self.config.seed, len(self.runs))
            run = OptimizerRun(run_id=len(self.runs), seed=seed).bind(self)
            self.runs.append(run)
            return run

    @property
    def llm_wrapper(self) -> LLMWrapper:
        """Get the LLM wrapper for this context.

        Returns:
        * `LLMWrapper` configured with the context's provider and model.
        """
        return get_llm_wrapper(self.config.provider, self.config.model, self.params[Params.Options])

    @property
    def options(self) -> Options:
        """Get the processing options.

        Returns:
        * `Options` from the context parameters.
        """
        return self.params[Params.Options]

    def set_param(self, name: str, value: Any):
        """Set a parameter in the context. Raises if context is locked.

        Args:
        * `name`: Parameter name.
        * `value`: Parameter value.

        Raises:
        * `OptimizationConfigurationError`: If context is locked.
        """
        if self.locked:
            raise OptimizationConfigurationError("OptimizerContext is locked")
        self.params[name] = value
        if isinstance(value, InitContextMixin):
            value.on_param_set(self)

    def get_param(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        """Get a parameter, optionally checking type and raising with a custom message if missing.

        Args:
        * `name`: Parameter name.
        * `cls`: Optional type to validate against.
        * `missing_error_message`: Optional custom error message if parameter is missing.

        Returns:
        * Parameter value.

        Raises:
        * `OptimizationConfigurationError`: If context is not locked, parameter is missing, or type mismatch.
        """
        if not self.locked:
            raise OptimizationConfigurationError("Attempted to get param from unlocked OptimizerContext")
        value = self.params.get(name, None)
        if value is None and missing_error_message is not None:
            raise OptimizationConfigurationError(missing_error_message)
        if cls is not None and not isinstance(value, cls):
            raise OptimizationConfigurationError(f"Expected {cls.__name__}, got {type(value).__name__}")
        return value

    def lock(self):
        """Lock the context to prevent further parameter changes.

        After locking, parameters can only be read, not modified.
        """
        self.locked = True
        for value in self.params.values():
            if isinstance(value, InitContextMixin):
                value.on_context_lock(self)

    def has_param(self, name: str):
        """Check if a parameter exists.

        Args:
        * `name`: Parameter name to check.

        Returns:
        * `True` if parameter exists, `False` otherwise.
        """
        return name in self.params


class InitContextMixin(ABC):
    """Mixin for objects that need to alter OptimizerContext on init.

    Provides hooks for objects to react to context parameter changes
    and context locking.
    """

    def on_param_set(self, context: OptimizerContext):
        """Called when this object is set as a context parameter.

        Args:
        * `context`: `OptimizerContext` that this parameter was set in.
        """
        pass

    def on_context_lock(self, context: OptimizerContext):
        """Called when the context is locked.

        Args:
        * `context`: `OptimizerContext` that was locked.
        """
        pass


TOptimizerConfig = TypeVar("TOptimizerConfig", bound=OptimizerConfig)


class BaseOptimizer(ABC, Generic[TOptimizerConfig]):
    """Base class for all optimizers, handling context and parameter management.

    Provides common functionality for managing optimizer configuration,
    parameters, and runs.
    """

    def __init__(self, name: str, config: TOptimizerConfig, checkpoint_path: Optional[str] = None):
        """Initialize the optimizer.

        Args:
        * `name`: Name of the optimizer.
        * `config`: `OptimizerConfig` with optimizer settings.
        * `checkpoint_path`: Optional path for saving/loading checkpoints.
        """
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
        """Set a parameter in the optimizer context.

        Args:
        * `name`: Parameter name.
        * `value`: Parameter value.
        """
        self.context.set_param(name, value)

    def get_param(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        """Get a parameter from the optimizer context.

        Args:
        * `name`: Parameter name.
        * `cls`: Optional type to validate against.
        * `missing_error_message`: Optional custom error message if parameter is missing.

        Returns:
        * Parameter value.
        """
        return self.context.get_param(name, cls, missing_error_message)

    def has_param(self, name: str) -> bool:
        """Check if a parameter exists.

        Args:
        * `name`: Parameter name to check.

        Returns:
        * `True` if parameter exists, `False` otherwise.
        """
        return self.context.has_param(name)

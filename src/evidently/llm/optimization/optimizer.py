import datetime
import uuid
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
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
    InputValues = "input_values"
    Target = "target"
    Reasoning = "reasoning"
    Scores = "scores"
    Pred = "preds"
    PredReasoning = "preds_reasoning"
    PredScores = "preds_scores"
    Task = "task"
    OptimizerPromptInstructions = "optimizer_prompt_instructions"


class OptimizerConfig(AutoAliasMixin, EvidentlyBaseModel):
    """Configuration for the optimizer, including provider and model."""

    __alias_type__: ClassVar = "optimizer_config"

    class Config:
        is_base_type = True

    provider: str = "openai"
    model: str = "gpt-4o-mini"


LogID = uuid.UUID
T = TypeVar("T")


class OptimizerLog(AutoAliasMixin, EvidentlyBaseModel, ABC):
    """Base class for all optimizer logs."""

    __alias_type__: ClassVar = "optimizer_log"

    class Config:
        is_base_type = True

    id: LogID = Field(default_factory=new_id)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError()


TLog = TypeVar("TLog", bound=OptimizerLog)


class OptimizerContext(BaseModel):
    """Holds the state, parameters, and logs for an optimization run."""

    config: OptimizerConfig
    params: Dict[str, Any]
    logs: Dict[LogID, OptimizerLog]
    locked: bool = False

    # @classmethod
    # def load(cls: Type[Self], path: str) -> Self:
    #     raise NotImplementedError()
    #
    # def save(self, path: str):
    #     raise NotImplementedError()

    @property
    def llm_wrapper(self) -> LLMWrapper:
        return get_llm_wrapper(self.config.provider, self.config.model, self.params[Params.Options])

    @property
    def options(self) -> Options:
        return self.params[Params.Options]

    def add_log(self, log: OptimizerLog):
        """Add a log entry to the context and log its message."""
        print(log.message())
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

    def set_param(self, name: str, value: Any):
        """Set a parameter in the context. Raises if context is locked."""
        if self.locked:
            raise OptimizationConfigurationError("OptimizerContext is locked")
        self.params[name] = value
        if isinstance(value, InitContextMixin):
            value.init(self)

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


class InitContextMixin(ABC):
    """Mixin for objects that need to alter OptimizerContext on init."""

    @abstractmethod
    def init(self, context: OptimizerContext):
        raise NotImplementedError()


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
        self.context = OptimizerContext(config=config, params={}, logs={})

    def _lock(self):
        """Lock the context to prevent further parameter changes."""
        self.context.locked = True

    def set_param(self, name: str, value: Any):
        """Set a parameter in the optimizer context."""
        self.context.set_param(name, value)

    def get_param(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        """Get a parameter from the optimizer context."""
        return self.context.get_param(name, cls, missing_error_message)

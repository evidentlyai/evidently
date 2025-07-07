import datetime
import os
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Self
from typing import Type
from typing import TypeVar

import pandas as pd
import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently.legacy.core import new_id
from evidently.legacy.options.base import Options
from evidently.legacy.utils.llm.wrapper import LLMWrapper
from evidently.legacy.utils.llm.wrapper import get_llm_wrapper
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class Inputs:
    BasePrompt = "base_prompt"
    EarlyStop = "early_stop"
    LLMClassification = "llm_classification"
    Options = "options"
    Scorer = "scorer"
    Evaluator = "evaluator"
    Values = "values"
    Target = "target"
    Reasoning = "reasoning"
    Scores = "scores"
    Pred = "preds"
    PredReasoning = "preds_reasoning"
    PredScores = "preds_scores"


class OptimizerConfig(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar = "optimizer_config"

    provider: str = "openai"
    model: str = "gpt-4o-mini"


LogID = uuid6.UUID
T = TypeVar("T")


class OptimizerLog(AutoAliasMixin, EvidentlyBaseModel, ABC):
    __alias_type__: ClassVar = "optimizer_log"

    id: LogID = Field(default_factory=new_id)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError()


class Mistakes(NamedTuple):
    values: pd.Series
    target: pd.Series
    reasoning: Optional[pd.Series]
    preds: pd.Series
    preds_reasoning: Optional[pd.Series]


TLog = TypeVar("TLog", bound=OptimizerLog)


class OptimizerContext(BaseModel):
    config: OptimizerConfig
    inputs: Dict[str, Any]
    logs: Dict[LogID, OptimizerLog]
    locked: bool = False

    @classmethod
    def load(cls: Type[Self], path: str) -> Self:
        raise NotImplementedError()

    def save(self, path: str):
        raise NotImplementedError()

    @property
    def llm_wrapper(self) -> LLMWrapper:
        return get_llm_wrapper(self.config.provider, self.config.model, self.inputs[Inputs.Options])

    @property
    def options(self) -> Options:
        return self.inputs[Inputs.Options]

    def add_log(self, log: OptimizerLog):
        print(log.message())
        self.logs[log.id] = log

    def get_log(self, log_id: LogID) -> OptimizerLog:
        if log_id not in self.logs:
            raise ValueError(f"Log with id {log_id} not found")
        return self.logs[log_id]

    def get_logs(self, log_type: Type[TLog]) -> List[TLog]:
        return [log for log in self.logs.values() if isinstance(log, log_type)]

    def get_last_log(self, log_type: Type[TLog]) -> Optional[TLog]:
        for log in reversed(self.logs.values()):
            if isinstance(log, log_type):
                return log
        return None

    def set_input(self, name: str, value: Any):
        if self.locked:
            raise ValueError("OptimizerContext is locked")
        self.inputs[name] = value

    def get_input(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        if not self.locked:
            raise ValueError("OptimizerContext is not locked")
        value = self.inputs.get(name, None)
        if value is None and missing_error_message is not None:
            raise ValueError(missing_error_message)
        if cls is not None and not isinstance(value, cls):
            raise ValueError(f"Expected {cls.__name__}, got {type(value).__name__}")
        return value


TOptimizerConfig = TypeVar("TOptimizerConfig", bound=OptimizerConfig)


class BaseOptimizer(ABC, Generic[TOptimizerConfig]):
    def __init__(self, name: str, config: TOptimizerConfig, checkpoint_path: Optional[str] = None):
        self.name = name
        self.checkpoint_path = checkpoint_path or f".optimizer_checkpoint_{name}"
        if os.path.exists(self.checkpoint_path):
            self.context = OptimizerContext.load(self.checkpoint_path)
            if self.context.config != config:
                raise ValueError(f"Optimizer config changed, cannot load from checkpoint at {self.checkpoint_path}")
        else:
            self.context = OptimizerContext(config=config, inputs={}, logs={})

    def _lock(self):
        self.context.locked = True

    def set_input(self, name: str, value: Any):
        self.context.set_input(name, value)

    def get_input(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        return self.context.get_input(name, cls, missing_error_message)

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


class OptimizerContext(BaseModel):
    config: OptimizerConfig
    inputs: Dict[str, Any]
    logs: List[OptimizerLog]

    @classmethod
    def load(cls: Type[Self], path: str) -> Self:
        raise NotImplementedError()

    def save(self, path: str):
        raise NotImplementedError()

    @property
    def llm_wrapper(self) -> LLMWrapper:
        return get_llm_wrapper(self.config.provider, self.config.model, self.inputs[Inputs.Options])

    @property
    def mistakes(self) -> Mistakes:
        from evidently.llm.optimization.prompts import PromptEvaluationLog

        last_eval = next((p for p in reversed(self.logs) if isinstance(p, PromptEvaluationLog)), None)
        if last_eval is None:
            raise ValueError("Prompt was not evaluated")
        target = self.inputs[Inputs.Target]
        preds = last_eval.data[Inputs.Pred]
        mask = preds == target
        return Mistakes(
            values=self.inputs[Inputs.Values][mask],
            target=target[mask],
            reasoning=self.inputs[Inputs.Reasoning][mask],
            preds=preds[mask],
            preds_reasoning=last_eval.data[Inputs.PredReasoning][mask],
        )

    @property
    def options(self) -> Options:
        return self.inputs[Inputs.Options]

    def add_log(self, log: OptimizerLog):
        print(log.message())
        self.logs.append(log)

    def get_log(self, log_id: LogID) -> OptimizerLog:
        for log in self.logs:
            if log.id == log_id:
                return log
        raise ValueError(f"Log with id {log_id} not found")


TOptimizerConfig = TypeVar("TOptimizerConfig", bound=OptimizerConfig)
T = TypeVar("T")


class BaseOptimizer(ABC, Generic[TOptimizerConfig]):
    def __init__(self, name: str, config: TOptimizerConfig, checkpoint_path: Optional[str] = None):
        self.name = name
        self.checkpoint_path = checkpoint_path or f".optimizer_checkpoint_{name}"
        if os.path.exists(self.checkpoint_path):
            self.context = OptimizerContext.load(self.checkpoint_path)
            if self.context.config != config:
                raise ValueError(f"Optimizer config changed, cannot load from checkpoint at {self.checkpoint_path}")
        else:
            self.context = OptimizerContext(config=config, inputs={}, logs=[])

    def set_input(self, name: str, value: Any):
        self.context.inputs[name] = value

    def get_input(self, name: str, cls: Optional[Type[T]] = None, missing_error_message: Optional[str] = None) -> T:
        value = self.context.inputs.get(name, None)
        if value is None and missing_error_message is not None:
            raise ValueError(missing_error_message)
        if cls is not None and not isinstance(value, cls):
            raise ValueError(f"Expected {cls.__name__}, got {type(value).__name__}")
        return value

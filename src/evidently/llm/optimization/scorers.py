from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Optional

import pandas as pd
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import brier_score_loss
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import precision_score
from sklearn.metrics import r2_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score

from evidently.legacy.options.base import Options
from evidently.llm.optimization.optimizer import LLMDataset
from evidently.llm.optimization.optimizer import LLMDatasetSplit
from evidently.llm.optimization.optimizer import OptimizerContext
from evidently.llm.optimization.optimizer import Params
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.arg_type_registry import BaseArgTypeRegistry

from .errors import OptimizationConfigurationError

if TYPE_CHECKING:
    from .prompts import PromptExecutionLog


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

    async def score(self, context: OptimizerContext, execution_log: "PromptExecutionLog") -> Optional[Dict[str, float]]:
        predictions = execution_log.result.get_predictions()
        if context.has_param(Params.Dataset):
            dataset = context.get_param(Params.Dataset, LLMDataset)
        else:
            target_value: Any = context.get_param(Params.TargetValue)
            return {
                LLMDatasetSplit.All: await self._score(
                    predictions=predictions,
                    target=pd.Series([target_value] * len(predictions)),
                    options=context.options,
                )
                or 0,
            }
        result = {}
        for split in (LLMDatasetSplit.Train, LLMDatasetSplit.Test, LLMDatasetSplit.Val):
            if split not in dataset.split_masks:
                continue
            target = dataset[split].target
            if target is None:
                raise OptimizationConfigurationError("Target is required for scoring")
            result[split] = await self._score(predictions[dataset.split_masks[split]], target, context.options) or 0
        if len(result) == 0:
            target = dataset.target
            if target is None:
                raise OptimizationConfigurationError("Target is required for scoring")
            result[LLMDatasetSplit.All] = await self._score(predictions, target, context.options) or 0
        return result


class AccuracyScorer(OptimizationScorer):
    """Scorer that computes accuracy of predictions."""

    __registry_alias__: ClassVar = "accuracy"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return (predictions == target).mean()


class MCCScorer(OptimizationScorer):
    """Scorer that computes Matthew's correlation coefficient."""

    __registry_alias__: ClassVar = "mcc"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return matthews_corrcoef(target.to_numpy(), predictions.to_numpy())


class PrecisionScorer(OptimizationScorer):
    """Scorer that computes Precision."""

    __registry_alias__: ClassVar = "precision"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return precision_score(target, predictions, average="macro", zero_division=0)


class RecallScorer(OptimizationScorer):
    """Scorer that computes Recall."""

    __registry_alias__: ClassVar = "recall"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return recall_score(target, predictions, average="macro", zero_division=0)


class F1Scorer(OptimizationScorer):
    """Scorer that computes F1 score."""

    __registry_alias__: ClassVar = "f1"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return f1_score(target, predictions, average="macro", zero_division=0)


class R2Scorer(OptimizationScorer):
    """Scorer that computes R² (regression only)."""

    __registry_alias__: ClassVar = "r2"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return r2_score(target, predictions)


class BalancedAccuracyScorer(OptimizationScorer):
    """Scorer that computes Balanced Accuracy."""

    __registry_alias__: ClassVar = "balanced_accuracy"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return balanced_accuracy_score(target, predictions)


class CohenKappaScorer(OptimizationScorer):
    """Scorer that computes Cohen's Kappa."""

    __registry_alias__: ClassVar = "cohen_kappa"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return cohen_kappa_score(target, predictions)


class RocAucScorer(OptimizationScorer):
    """Scorer that computes ROC AUC (probabilistic predictions required)."""

    __registry_alias__: ClassVar = "roc_auc"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        # predictions should be probabilities or scores
        return roc_auc_score(target, predictions, multi_class="ovr")


class LogLossScorer(OptimizationScorer):
    """Scorer that computes Log Loss (probabilistic predictions required)."""

    __registry_alias__: ClassVar = "log_loss"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return log_loss(target, predictions)


class BrierScoreScorer(OptimizationScorer):
    """Scorer that computes Brier Score (probabilistic predictions required)."""

    __registry_alias__: ClassVar = "brier_score"

    async def _score(self, predictions: pd.Series, target: pd.Series, options: Options) -> Optional[float]:
        return brier_score_loss(target, predictions)

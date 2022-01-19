from dataclasses import dataclass
from typing import Optional, Dict, Tuple, Union

DEFAULT_CONF_INTERVAL_SIZE = 1
DEFAULT_CLASSIFICATION_TRESHOLD = 0.5

@dataclass
class QualityMetricsOptions:
    conf_interval_n_sigmas: int = DEFAULT_CONF_INTERVAL_SIZE
    classification_treshold: float = DEFAULT_CLASSIFICATION_TRESHOLD
    cut_outliers: Union[None, Tuple[str, float], Dict[str, Tuple[str, float]]] = None

    def as_dict(self):
        return {
            "conf_interval_n_sigmas": self.conf_interval_n_sigmas,
            "classification_treshold": self.classification_treshold,
            "cut_outliers": self.remove_outliers
        }

    def get_rcut_outliers(self, feature_name: str) -> float:
        if isinstance(self.cut_outliers, float):
            return self.cut_outliers
        if isinstance(self.cut_outliers, dict):
            return self.rcut_outliers.get(feature_name, None)
        raise ValueError(f"""QualityMetricsOptions.remove_outliers 
                                is incorrect type {type(self.cut_outliers)}""")

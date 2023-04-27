import numpy as np
from typing import Dict


def numpy_to_standard_types(input_data: Dict) -> Dict:
    """Convert numpy type values to standard Python types in flat(!) dictionary.

    Args:
        input_data (Dict): Input data (flat dictionary).

    Returns:
        Dict: Dictionary with standard value types.
    """

    output_data: Dict = {}

    for k, v in input_data.items():
        if isinstance(v, np.generic):
            v = v.item()
        output_data[k] = v

    return output_data

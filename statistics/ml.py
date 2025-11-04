
from enum import Enum, auto
import numpy as np

class EntropyUnit(Enum):
    BITS = auto()
    NATS = auto()
    DITS = auto()

def entropy(array: np.ndarray, entropy_unit: EntropyUnit = EntropyUnit.BITS ) -> float:
    """
    Calculates the entropy of a given probability distribution


    :param array: probability distribution
    :param entropy_unit: entropy unit
    :return: entropy of the distribution in array
    """
    if entropy_unit == EntropyUnit.BITS:
        return -np.sum(array*np.log2(array))
    elif entropy_unit == EntropyUnit.NATS:
        return -np.sum(array*np.log(array))
    elif entropy_unit == EntropyUnit.DITS:
        return -np.sum(array*np.log10(array))
    else:
        raise ValueError(f"Unsupported entropy unit: {entropy_unit}")

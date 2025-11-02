

import numpy as np


def entropy(array: np.ndarray, binary=True) -> float:
    """

    :param binary:
    :param array:
    :return:
    """
    return -np.sum(array*np.log2(array)) if binary else -np.sum(array*np.log(array))
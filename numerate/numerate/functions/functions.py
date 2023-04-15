import numpy as np


def tophat(x, *, a=1, b=1, c=0):
    """
    Tophat function.

    Parameters
    ----------
    x : array_like
    x value.

    a : float
    Height scaling constant.

    b : float
    Width scaling constant.

    c : float
    Translation constant.

    Returns
    -------
    array_like
    The value of the tophat function at x.
    """
    return a * \
        (np.heaviside(x - c + b / 2, 1) - np.heaviside(x - c - b / 2, 1))


def gaussian(x, *, a=1, b=1, c=0):
    """
    Gaussian function.

    Parameters
    ----------
    x : array_like
    x value.

    a : float
    Height scaling constant.

    b : float
    Width scaling constant.

    c : float
    Translation constant.

    Returns
    -------
    array_like
    The value of gaussian function at x.
    """
    return a * np.exp(- ((x - c) ** 2) / (2 * b ** 2))

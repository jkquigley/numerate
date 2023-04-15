import numpy as np


def upwind(theta, **kwargs):
    """
    Upwind limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The limited value.
    """
    return np.zeros_like(theta)


def lax_wendroff(theta, **kwargs):
    """
    Lax-Wendroff limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    Constant 1.
    """
    return np.ones_like(theta)


def beam_warming(theta, **kwargs):
    """
    Beam-Warming limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The theta value.
    """
    return theta


def fromm(theta, **kwargs):
    """
    Fromm limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The limited value.
    """
    return 0.5 * (1 + theta)


def minmod(theta, **kwargs):
    """
    Minmod limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The limited value.
    """
    return np.maximum(0, np.minimum(1, theta))


def superbee(theta, **kwargs):
    """
    Superbee limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The limited value.
    """
    return np.maximum(
        0,
        np.maximum(np.minimum(1, 2 * theta), np.minimum(2, theta))
    )


def sweby(theta, *, beta=1.5, **kwargs):
    """
    Sweby limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    beta : float
    Parameter in interval [1, 2]

    Returns
    -------
    array_like
    The limited value.
    """
    return np.maximum(
        0,
        np.maximum(np.minimum(1, beta * theta), np.minimum(beta, theta)),
    )


def mc(theta, **kwargs):
    """
    Monotonized central limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The limited value.
    """
    return np.maximum(0, np.minimum((1 + theta) / 2, np.minimum(2, 2 * theta)))


def van_leer(theta, **kwargs):
    """
    Van Leer limiter.

    Parameters
    ----------
    theta : array_like
    The theta value.

    Returns
    -------
    array_like
    The limited value.
    """
    return (theta + np.abs(theta)) / (1 + np.abs(theta))

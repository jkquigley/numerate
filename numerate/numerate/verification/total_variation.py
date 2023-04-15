import numpy as np


def total_variation(sol):
    """
    Parameters
    ----------
    sol: array_like
    The numerical solution at some specific time step.

    Returns
    -------
    float
    The total variation of the solution at some specific time step.
    """
    return sum(np.abs(np.roll(sol, 1) - sol))


def is_tvd(sol):
    """
    Parameters
    ----------
    sol: array_like
    The full numerical solution over all space and time steps.

    Returns
    -------
    bool
    If the solution is total variation diminishing.
    """
    n = sol.shape[1]
    tv = np.zeros(n)

    for i in range(n):
        tv[i] = total_variation(sol[:, i])

    return np.all(np.diff(tv) <= 0)

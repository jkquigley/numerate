import numpy as np
from .upwind_forward import NumericalAdvectionEquationUpwindForward


def div(a, b, epsilon):
    """
    Divide two arrays but avoid divide-by-zero errors by replacing zero
    denominators with epsilon.

    Parameters
    ----------
    a : array_like
    The numerator

    b : array_like
    The denominator

    epsilon : float
    Value to replace zero denominators with.

    Returns
    -------
    c : array_like
    a / b, with zero denominators replaced by epsilon.
    """
    c = np.zeros_like(a)

    cond = np.logical_and(np.abs(a) <= epsilon, np.abs(b) <= epsilon)
    c[cond] = 1

    cond = np.logical_and(np.abs(a) > epsilon, np.abs(b) <= epsilon)
    c[cond] = np.sign(b)[cond] * a[cond] / epsilon

    cond = np.abs(b) > epsilon
    c[cond] = a[cond] / b[cond]

    return c


class NumericalAdvectionEquationFluxLimiter(
    NumericalAdvectionEquationUpwindForward
):
    def __init__(
            self,
            a,
            u0,
            phi,
            *,
            x0=0,
            x1=1,
            xs=1e3,
            revolutions=1,
            ts=1e3,
            epsilon=1e-12,
            **kwargs,
    ):
        super().__init__(
            a, u0, x0=x0, x1=x1, xs=xs, revolutions=revolutions, ts=ts
        )
        self.phi = phi
        self.kwargs = kwargs
        self.epsilon = epsilon

    def recurrence_relation(self, n, mats, sol):
        deltas = sol[:, n].toarray() - np.roll(sol[:, n].toarray(), 1)
        thetas = div(np.roll(deltas, 1), deltas, self.epsilon)
        phi_theta_deltas = self.phi(thetas, **self.kwargs) * deltas
        correction = 0.5 * self.c * (1 - self.c) * \
            (np.roll(phi_theta_deltas, -1) - phi_theta_deltas)

        super().recurrence_relation(n, mats, sol)
        sol[:, n+1] -= correction

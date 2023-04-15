import numpy as np
import scipy.sparse as sp
from .upwind_forward import NumericalAdvectionEquationUpwindForward


class NumericalAdvectionEquationLeapfrog(
    NumericalAdvectionEquationUpwindForward
):
    def __init__(self, a, u0, *, x0=0, x1=1, xs=1e3, revolutions=1, ts=1e3):
        super().__init__(
            a, u0, x0=x0, x1=x1, xs=xs, revolutions=revolutions, ts=ts
        )

    def get_matrices(self):
        diagonals = [
            self.c,
            - self.c * np.ones(self.xs - 1),
            self.c * np.ones(self.xs - 1),
            - self.c,
        ]

        offsets = [
            self.xs - 1,
            1,
            - 1,
            - self.xs + 1,
        ]

        mat = sp.diags(
            diagonals,
            offsets=offsets,
            format='csr',
            dtype=float
        )

        return mat,

    def recurrence_relation(self, n, mats, sol):
        # Apply upwind forward scheme on the first step
        if n == 0:
            mats = super().get_matrices()
            super().recurrence_relation(n, mats, sol)
        # Otherwise just do leapfrog
        else:
            sol[:, n + 1] = sol[:, n - 1] + mats[0] @ sol[:, n]

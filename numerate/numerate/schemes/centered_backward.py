import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
from .base import NumericalAdvectionEquation


class NumericalAdvectionEquationCenteredBackward(
    NumericalAdvectionEquation
):
    def __init__(self, a, u0, *, x0=0, x1=1, xs=1e3, revolutions=1, ts=1e3):
        super().__init__(
            a, u0, x0=x0, x1=x1, xs=xs, revolutions=revolutions, ts=ts
        )

    def get_matrices(self):
        diagonals = [
            - self.c / 2,
            (self.c / 2) * np.ones(self.xs - 1),
            np.ones(self.xs),
            - (self.c / 2) * np.ones(self.xs - 1),
            self.c / 2,
        ]

        offsets = [
            self.xs - 1,
            1,
            0,
            -1,
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
        sol[:, n + 1] = spsolve(mats[0], (sol[:, n]))

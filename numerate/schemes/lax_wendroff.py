import numpy as np
import scipy.sparse as sp
from .base import NumericalAdvectionEquation


class NumericalAdvectionEquationLaxWendroff(
    NumericalAdvectionEquation
):
    def __init__(self, a, u0, *, x0=0, x1=1, xs=1e3, revolutions=1, ts=1e3):
        super().__init__(
            a, u0, x0=x0, x1=x1, xs=xs, revolutions=revolutions, ts=ts
        )

    def get_matrices(self):
        first_diagonals = [
            -1,
            np.ones(self.xs - 1),
            -np.ones(self.xs - 1),
            1,
        ]

        first_offsets = [
            -self.xs + 1,
            -1,
            1,
            self.xs - 1,
        ]

        second_diagonals = [
            1,
            np.ones(self.xs - 1),
            -2,
            np.ones(self.xs - 1),
            1,
        ]

        second_offsets = [
            -self.xs + 1,
            -1,
            0,
            1,
            self.xs - 1,
        ]

        mat1 = 0.5 * self.c * sp.diags(
            first_diagonals,
            offsets=first_offsets,
            format='csr',
            dtype=float,
        )

        mat2 = 0.5 * (self.c ** 2) * sp.diags(
            second_diagonals,
            offsets=second_offsets,
            format='csr',
            dtype=float,
        )

        return mat1, mat2,

    def recurrence_relation(self, n, mats, sol):
        sol[:, n + 1] = sol[:, n] + mats[0] @ sol[:, n] + mats[1] @ sol[:, n]

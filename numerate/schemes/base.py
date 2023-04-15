import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ..functions import periodically_continued


class NumericalAdvectionEquation:
    """
    Base class to represent and numerically solve the 1-D advection equation.
    """
    def __init__(self, a, u0, *, x0=0, x1=1, xs=1e2, revolutions=1, ts=1e3):
        """
        Constructor.

        Parameters
        __________
        a : float
        Velocity constant.

        u0 : function
        The initial conditions as a function over the space interval.

        x0 : float
        Lower x interval bound.
        x1 : float
        Upper x interval bound.

        xs : int
        Number of grid cells over the space interval.

        revolutions : int
        Number of periodic revolutions through the domain.

        ts :int
        Number of grid cells over the time interval.
        """
        self.a = a
        self.x0 = x0
        self.x1 = x1
        self.u0 = periodically_continued(self.x0, self.x1)(u0)
        self.xs = int(xs)
        self.revolutions = revolutions
        self.t1 = self.revolutions * (self.x1 - self.x0) / a
        self.ts = int(ts)
        self.dx = (self.x1 - self.x0) / self.xs
        self.dt = self.t1 / self.ts
        self.c = self.a * self.dt / self.dx
        self.x_range = np.linspace(self.x0, self.x1, self.xs)
        self.t_range = np.linspace(0, self.t1, self.ts)

    def get_initial_condition(self):
        """
        Get the initial values of the solution.

        Returns
        _______
        sol : array_like
        A matrix of size xs x ts with the initial values of the solution in
        the first column and zeros elsewhere.
        """
        sol = sp.lil_matrix((self.xs, self.ts), dtype=float)
        sol[:, 0] = self.u0(self.x_range)

        return sol

    def get_matrices(self):
        """
        Create matrices corresponding to the scheme to solve the equation.

        Returns
        -------
        mats : tuple of array_like
        A tuple of matrices of size of xs x xs corresponding to the scheme.
        """
        raise NotImplementedError()

    def recurrence_relation(self, n, mats, sol):
        """
        Apply the scheme in place to solve the (n+1)th time index.

        Parameters
        ----------
        n : int
        Time index.

        mats : tuple of array_like
        Matrices of size xs x xs corresponding to the scheme.

        sol : array_like
        Solution matrix of size xs x ts.
        """
        raise NotImplementedError()

    def solve(self):
        """
        Solve the equation.

        Returns
        -------
        sol : array_like
        The solution as a matrix of size xs x ts to the equation corresponding
        to the initial conditions.
        """
        mats = self.get_matrices()
        sol = self.get_initial_condition()

        for i in range(self.ts - 1):
            self.recurrence_relation(i, mats, sol)

        return sol

    def get_temporal_index(self, s):
        """
        Get the temporal index at the specified revolution.

        Parameters
        ----------
        s : int
        The number of full revolutions in the time domain at which to get the
        temporal index.
        """
        i = int(s * (self.x1 - self.x0) / (self.a * self.dt))

        if i >= self.t_range.shape[0]:
            return -1

        else:
            return i

    def plot(self, sol, *, t=None, separate=False, filename=None):
        """
        Plot the numerical solutions in the spacial domain at a specific or
        all full revolutions in the periodic domain.

        Parameters
        ----------
        sol : array_like
        The numerical solution to plot.

        t : int
        Period number. The solution will be plotted at the start of the
        revolution t around the domain.

        separate : bool
        Whether to plot the curves on the same or separate axes. This is only
        relevant if t is None.

        filename : string
        Name of the file to save to. If None no image is saved.
        """
        if t is None and not separate:
            fig, ax = plt.subplots()

            for s in range(self.revolutions + 1):
                i = self.get_temporal_index(s)

                if i >= self.t_range.shape[0]:
                    i = -1

                ax.plot(self.x_range, sol[:, i].toarray(), label=f"t = {s}")

            ax.legend()

        elif t is None and separate:
            fig, ax = plt.subplots(self.revolutions)

            for s in range(self.revolutions):
                r = s + 1
                i = self.get_temporal_index(r)

                ax[s].plot(
                    self.x_range,
                    self.u0(self.x_range - self.a * self.t_range[i]),
                    label="Exact"
                )
                ax[s].plot(
                    self.x_range,
                    sol[:, i].toarray(),
                    label="Numerical"
                )

                ax[s].legend()
                fig.tight_layout()

        else:
            fig, ax = plt.subplots()

            i = self.get_temporal_index(t)

            ax.plot(
                self.x_range,
                self.u0(self.x_range - self.a * self.t_range[i]),
                label="Exact"
            )
            ax.plot(
                self.x_range,
                sol[:, i].toarray(),
                label="Numerical"
            )

            ax.legend()

        if filename:
            plt.savefig(filename)
        else:
            plt.show()

    def animate(self, sol, *, drop=1, interval=20, filename=None):
        """
        Animate the numerical and true solutions over the time interval.

        Parameters
        ----------
        sol : array_like
        Numerical solution.

        filename : string
        Name of the file to save to. If None no animation is saved.

        Returns
        -------
        anim : FuncAnimation
        The animation.
        """
        fig, ax = plt.subplots()

        true_line, = ax.plot(self.x_range, self.u0(self.x_range))
        num_line, = ax.plot(self.x_range, sol[:, 0].toarray())
        n_label = ax.text(0, 1, "$n = 0$", transform=ax.transAxes, fontsize=13)

        plt.ylim(
            np.min(sol.toarray().flatten()) - plt.rcParams['axes.ymargin'],
            np.max(sol.toarray().flatten()) + plt.rcParams['axes.ymargin'],
        )

        def func(i):
            true_line.set_ydata(
                self.u0(self.x_range - self.a * self.t_range[i])
            )
            num_line.set_ydata(sol[:, i].toarray())
            n_label.set_text(f"$n = {i}$")

            return true_line, num_line, n_label,

        anim = animation.FuncAnimation(
            fig,
            func,
            frames=range(0, self.ts, drop),
            interval=drop * interval / self.a,
            blit=True,
            repeat=False
        )

        plt.close()

        if filename:
            writergif = animation.PillowWriter(fps=30)
            anim.save(filename, writer=writergif)

        return anim

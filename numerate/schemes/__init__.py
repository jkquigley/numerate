from matplotlib.pyplot import rcParams
from .centered_backward import NumericalAdvectionEquationCenteredBackward
from .centered_forward import NumericalAdvectionEquationCenteredForward
from .centered_trapezoidal import NumericalAdvectionEquationCenteredTrapezoidal
from .flux_limiter import NumericalAdvectionEquationFluxLimiter
from .lax_wendroff import NumericalAdvectionEquationLaxWendroff
from .leapfrog import NumericalAdvectionEquationLeapfrog
from .upwind_backward import NumericalAdvectionEquationUpwindBackward
from .upwind_forward import NumericalAdvectionEquationUpwindForward
from .upwind_trapezoidal import NumericalAdvectionEquationUpwindTrapezoidal


rcParams['axes.xmargin'] = 0

__all__ = [
    'NumericalAdvectionEquationCenteredBackward',
    'NumericalAdvectionEquationCenteredForward',
    'NumericalAdvectionEquationCenteredTrapezoidal',
    'NumericalAdvectionEquationFluxLimiter',
    'NumericalAdvectionEquationLaxWendroff',
    'NumericalAdvectionEquationLeapfrog',
    'NumericalAdvectionEquationUpwindBackward',
    'NumericalAdvectionEquationUpwindForward',
    'NumericalAdvectionEquationUpwindTrapezoidal',
]

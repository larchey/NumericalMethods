"""Root finding: bisection, Newton, secant and Mueller's method.

Every method returns a RootResult holding the root and each successive
estimate, and raises ConvergenceError instead of looping forever.
"""

import cmath
import math
from dataclasses import dataclass


class ConvergenceError(ArithmeticError):
    """The method broke down or ran out of iterations."""


@dataclass(frozen=True)
class RootResult:
    root: float | complex
    estimates: list

    @property
    def iterations(self):
        return len(self.estimates)


def _check(tol, max_iter):
    if not tol > 0:
        raise ValueError("tolerance must be positive")
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1")


def _require_finite(value):
    if not cmath.isfinite(value):
        raise ConvergenceError("the estimates diverged")


def bisection(f, a, b, tol=1e-10, max_iter=1000):
    """Halve [a, b] until the root is known to within tol."""
    _check(tol, max_iter)
    fa, fb = f(a), f(b)
    if fa == 0:
        return RootResult(a, [a])
    if fb == 0:
        return RootResult(b, [b])
    if math.copysign(1, fa) == math.copysign(1, fb):
        raise ValueError("f(a) and f(b) must have opposite signs")

    estimates = []
    for _ in range(max_iter):
        m = a + (b - a) / 2
        fm = f(m)
        estimates.append(m)
        # m == a or b means floats cannot split the interval any further.
        if fm == 0 or abs(b - a) / 2 < tol or m in (a, b):
            return RootResult(m, estimates)
        if math.copysign(1, fm) == math.copysign(1, fa):
            a, fa = m, fm
        else:
            b = m
    raise ConvergenceError(f"no convergence after {max_iter} iterations")


def newton(f, df, x, tol=1e-10, max_iter=100):
    """Follow the tangent line from x. df is the derivative of f."""
    _check(tol, max_iter)
    estimates = []
    for _ in range(max_iter):
        fx = f(x)
        if fx == 0:
            return RootResult(x, estimates or [x])
        slope = df(x)
        if slope == 0:
            raise ConvergenceError(f"the derivative is zero at x = {x}")
        new = x - fx / slope
        _require_finite(new)
        estimates.append(new)
        if abs(new - x) < tol:
            return RootResult(new, estimates)
        x = new
    raise ConvergenceError(f"no convergence after {max_iter} iterations")


def newton_piecewise(f, df, g, dg, split, x, tol=1e-10, max_iter=100):
    """Newton's method on a function that is f for x <= split, g for x > split."""
    return newton(
        lambda t: f(t) if t <= split else g(t),
        lambda t: df(t) if t <= split else dg(t),
        x, tol, max_iter,
    )


def secant(f, x0, x1, tol=1e-10, max_iter=100):
    """Newton's method with the slope taken from the last two estimates."""
    _check(tol, max_iter)
    f0, f1 = f(x0), f(x1)
    if f0 == 0:
        return RootResult(x0, [x0])
    estimates = []
    for _ in range(max_iter):
        if f1 == 0:
            return RootResult(x1, estimates or [x1])
        if f1 == f0:
            raise ConvergenceError(f"the secant line is flat between {x0} and {x1}")
        new = x1 - f1 * (x1 - x0) / (f1 - f0)
        _require_finite(new)
        estimates.append(new)
        if abs(new - x1) < tol:
            return RootResult(new, estimates)
        x0, f0, x1, f1 = x1, f1, new, f(new)
    raise ConvergenceError(f"no convergence after {max_iter} iterations")


def mueller(f, x0, x1, x2, tol=1e-10, max_iter=100):
    """Fit a parabola through three points. Can find complex roots.

    f must accept complex numbers. The root is returned as a float when its
    imaginary part is negligible.
    """
    _check(tol, max_iter)
    if len({x0, x1, x2}) < 3:
        raise ValueError("the three starting points must be different")
    x0, x1, x2 = complex(x0), complex(x1), complex(x2)
    f0, f1, f2 = f(x0), f(x1), f(x2)
    for point, value in ((x0, f0), (x1, f1), (x2, f2)):
        if value == 0:
            root = _simplify(point, tol)
            return RootResult(root, [root])
    estimates = []
    for _ in range(max_iter):
        h1, h2 = x1 - x0, x2 - x1
        if 0 in (h1, h2, h1 + h2):
            raise ConvergenceError("the estimates collapsed onto one point")
        slope1, slope2 = (f1 - f0) / h1, (f2 - f1) / h2
        a = (slope2 - slope1) / (h1 + h2)
        b = slope2 + h2 * a
        discriminant = cmath.sqrt(b * b - 4 * f2 * a)
        # The larger denominator gives the root of the parabola nearest x2.
        denominator = max(b + discriminant, b - discriminant, key=abs)
        if denominator == 0:
            raise ConvergenceError("the three points lie on a flat line")
        step = -2 * f2 / denominator
        new = x2 + step
        _require_finite(new)
        estimates.append(_simplify(new, tol))
        f_new = f(new)
        if abs(step) < tol or f_new == 0:
            return RootResult(estimates[-1], estimates)
        x0, f0, x1, f1, x2, f2 = x1, f1, x2, f2, new, f_new
    raise ConvergenceError(f"no convergence after {max_iter} iterations")


def _simplify(z, tol):
    if abs(z.imag) < tol:
        return z.real
    if abs(z.real) < tol:
        return complex(0, z.imag)
    return z

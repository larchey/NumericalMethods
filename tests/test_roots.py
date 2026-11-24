import cmath
import math

import pytest

from numerical_methods.roots import (
    ConvergenceError, bisection, mueller, newton, newton_piecewise, secant,
)


def f(x):
    return x**3 - x - 1


def df(x):
    return 3 * x**2 - 1


ROOT = 1.324717957244746


@pytest.mark.parametrize("result", [
    bisection(f, 1, 2), bisection(f, 2, 1), newton(f, df, 1.5), secant(f, 1, 2), mueller(f, 0, 1, 2),
], ids=["bisection", "reversed", "newton", "secant", "mueller"])
def test_methods_agree(result):
    assert result.root == pytest.approx(ROOT, abs=1e-9)
    assert isinstance(result.root, float)
    assert result.estimates[-1] == result.root


def test_bisection_root_at_endpoint():
    assert bisection(lambda x: x - 1, 1, 3).root == 1
    assert bisection(lambda x: x - 3, 1, 3).root == 3


def test_bisection_needs_sign_change():
    with pytest.raises(ValueError, match="opposite signs"):
        bisection(lambda x: x**2 + 1, 0, 2)


def test_bisection_tolerance_bounds_the_error_for_flat_functions():
    # |f| is tiny far from this root, so testing |f| < tol would stop early.
    assert bisection(lambda x: (x - 1) ** 9, 0, 2.5, 1e-8).root == pytest.approx(1, abs=1e-8)


def test_bisection_tolerance_below_float_spacing():
    assert bisection(lambda x: x**2 - 2, 0, 2, 1e-300).root == pytest.approx(math.sqrt(2))


def test_bisection_does_not_underflow():
    assert bisection(lambda x: (x - 1) * 1e-200, 0, 3).root == pytest.approx(1)


def test_newton_failures():
    with pytest.raises(ConvergenceError, match="derivative"):
        newton(lambda x: x**2 + 1, lambda x: 2 * x, 1)
    with pytest.raises(ConvergenceError, match="100 iterations"):
        newton(lambda x: x**3 - 2 * x + 2, lambda x: 3 * x**2 - 2, 0)


def test_newton_double_root_and_exact_start():
    assert newton(lambda x: x * x, lambda x: 2 * x, 0).root == 0
    assert newton(lambda x: (x - 1) ** 2, lambda x: 2 * (x - 1), 5).root == pytest.approx(1)


def test_piecewise_uses_the_branch_containing_x():
    # x + 1 for x <= 0, x - 5 above: both pieces have a root in their own half.
    pieces = (lambda x: x + 1, lambda x: 1, lambda x: x - 5, lambda x: 1, 0)
    assert newton_piecewise(*pieces, 2).root == 5
    assert newton_piecewise(*pieces, -3).root == -1


def test_piecewise_ignores_roots_outside_a_branch():
    # x - 1 has a root at 1, but that piece only applies for x <= 0.
    result = newton_piecewise(lambda x: x - 1, lambda x: 1, lambda x: x - 4, lambda x: 1, 0, -2)
    assert result.root == 4


def test_secant_flat():
    with pytest.raises(ConvergenceError, match="flat"):
        secant(lambda x: x**2 - 1, -2, 2)


def test_secant_exact_start():
    assert secant(lambda x: x - 1, 1, 5).root == 1
    assert secant(lambda x: x - 1, 5, 1).root == 1


def test_mueller_complex():
    assert mueller(lambda x: x**2 + 1, 0, 1, 2).root == pytest.approx(1j)
    root = mueller(lambda x: cmath.exp(x) + 1, 0, 1, 2).root
    assert cmath.exp(root) == pytest.approx(-1)


def test_mueller_edge_cases():
    assert mueller(lambda x: x - 1, 1, 2, 3).root == 1
    assert mueller(lambda x: 2 * x - 1, 1, 2, 3).root == pytest.approx(0.5)
    with pytest.raises(ValueError, match="different"):
        mueller(f, 1, 1, 2)
    with pytest.raises(ConvergenceError):
        mueller(lambda x: 1, 1, 2, 3)


@pytest.mark.parametrize("tol", [0, -1, math.nan])
def test_bad_tolerance(tol):
    with pytest.raises(ValueError):
        bisection(f, 1, 2, tol)

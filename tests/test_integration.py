import math

import pytest

from numerical_methods.integration import left, right, simpson, trapezoid


def test_known_values():
    assert left(lambda x: x, 0, 1, 10) == pytest.approx(0.45)
    assert right(lambda x: x, 0, 1, 10) == pytest.approx(0.55)
    assert trapezoid(lambda x: x, 0, 1, 10) == pytest.approx(0.5)
    assert simpson(lambda x: x**3, 0, 2, 2) == pytest.approx(4)
    assert simpson(math.sin, 0, math.pi, 100) == pytest.approx(2, abs=1e-6)


@pytest.mark.parametrize("rule", [trapezoid, simpson])
def test_reversed_limits_negate(rule):
    assert rule(lambda x: x, 1, 0, 10) == pytest.approx(-0.5)


@pytest.mark.parametrize("rule", [left, right, trapezoid, simpson])
def test_needs_a_subinterval(rule):
    with pytest.raises(ValueError):
        rule(lambda x: x, 0, 1, 0)


def test_simpson_needs_even_n():
    with pytest.raises(ValueError, match="even"):
        simpson(lambda x: x, 0, 1, 3)

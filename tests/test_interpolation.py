import pytest

from numerical_methods.expressions import parse_function
from numerical_methods.interpolation import (
    divided_differences, lagrange, lagrange_expression, newton_expression, newton_polynomial,
)

XS, YS = [-1, 0, 2, 3.5], [4, -2, 0.5, 7]


@pytest.mark.parametrize("make", [
    lagrange,
    newton_polynomial,
    lambda xs, ys: parse_function(lagrange_expression(xs, ys)),
    lambda xs, ys: parse_function(newton_expression(xs, ys)),
])
def test_passes_through_points_and_agrees(make):
    polynomial = make(XS, YS)
    assert [polynomial(x) for x in XS] == pytest.approx(YS)
    assert polynomial(1.3) == pytest.approx(lagrange(XS, YS)(1.3))
    assert make([2], [5])(9) == 5


def test_reproduces_a_cubic():
    xs = [0, 1, 2, 3]
    assert newton_polynomial(xs, [x**3 for x in xs])(10) == pytest.approx(1000)


def test_table():
    assert divided_differences([0, 1, 2], [0, 1, 4]) == [[0, 1, 4], [1, 3], [1]]


@pytest.mark.parametrize("xs, ys", [([], []), ([1, 1], [2, 3]), ([1], [1, 2])])
@pytest.mark.parametrize("make", [lagrange, newton_polynomial, lagrange_expression, newton_expression])
def test_bad_points(make, xs, ys):
    with pytest.raises(ValueError):
        make(xs, ys)

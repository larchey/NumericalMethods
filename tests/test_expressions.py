import math

import pytest

from numerical_methods.expressions import ExpressionError, parse_function, parse_number


@pytest.mark.parametrize("text, x, expected", [
    ("x**2 - 2*x + 1", 3, 4),
    ("2*x^2", 3, 18),
    ("-x**2", 3, -9),
    ("sin(pi*x)", 0.5, 1),
    ("log(x, 2)", 8, 3),
    ("e**x", 1, math.e),
    ("abs(x)", -2, 2),
])
def test_evaluates(text, x, expected):
    assert parse_function(text)(x) == pytest.approx(expected)


@pytest.mark.parametrize("text", [
    "__import__('os').getcwd()", "x.__class__", "[x]", "'a'*9", "lambda: 1",
    "open('f')", "y", "foo(x)", "x if x else 1", "", "x +", "sin(x=1)", "True",
    "(" * 5000,
])
def test_rejects(text):
    with pytest.raises(ExpressionError):
        parse_function(text)


def test_huge_powers_fail_instead_of_hanging():
    with pytest.raises(ExpressionError):
        parse_function("9**9**9**9")(0)


@pytest.mark.parametrize("text, x", [("1/x", 0), ("sqrt(x)", -1), ("x**0.5", -1), ("sin(x, x)", 1)])
def test_undefined_points(text, x):
    with pytest.raises(ExpressionError):
        parse_function(text)(x)


def test_complex():
    f = parse_function("sqrt(x) + exp(x)*0", allow_complex=True)
    assert f(complex(-4)) == pytest.approx(2j)


def test_numbers():
    assert parse_number("pi/2") == math.pi / 2
    assert parse_number(" -3") == -3
    for bad in ("x", "0*x", "1j", ""):
        with pytest.raises(ExpressionError):
            parse_number(bad)

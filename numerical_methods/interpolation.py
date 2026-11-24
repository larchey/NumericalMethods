"""Polynomial interpolation through a list of points."""

import math


def _check(xs, ys):
    if not xs:
        raise ValueError("at least one point is needed")
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if len(set(xs)) != len(xs):
        raise ValueError("every x value must be different")


def lagrange(xs, ys):
    """Return the Lagrange interpolating polynomial as a function."""
    xs, ys = list(xs), list(ys)
    _check(xs, ys)

    def polynomial(x):
        return math.fsum(
            yk * math.prod((x - xj) / (xk - xj) for j, xj in enumerate(xs) if j != k)
            for k, (xk, yk) in enumerate(zip(xs, ys))
        )

    return polynomial


def lagrange_expression(xs, ys):
    """Write the Lagrange polynomial out as text."""
    _check(xs, ys)
    terms = []
    for k, (xk, yk) in enumerate(zip(xs, ys)):
        factors = "".join(f"*(x - {_num(xj)})" for j, xj in enumerate(xs) if j != k)
        denominator = math.prod(xk - xj for j, xj in enumerate(xs) if j != k)
        terms.append(f"{_num(yk)}{factors}/{_num(denominator)}")
    return " + ".join(terms)


def divided_differences(xs, ys):
    """Return the divided difference table, one column per order.

    Column 0 is ys. The first entry of each column is a coefficient of the
    Newton form.
    """
    _check(xs, ys)
    table = [list(ys)]
    for order in range(1, len(xs)):
        previous = table[-1]
        table.append([
            (previous[i + 1] - previous[i]) / (xs[i + order] - xs[i])
            for i in range(len(previous) - 1)
        ])
    return table


def newton_polynomial(xs, ys):
    """Return the Newton divided difference polynomial as a function."""
    xs = list(xs)
    coefficients = [column[0] for column in divided_differences(xs, ys)]

    def polynomial(x):
        total = coefficients[-1]
        for coefficient, xk in zip(coefficients[-2::-1], xs[-2::-1]):
            total = total * (x - xk) + coefficient
        return total

    return polynomial


def newton_expression(xs, ys):
    """Write the Newton form out as text."""
    terms = []
    for k, column in enumerate(divided_differences(xs, ys)):
        factors = "".join(f"*(x - {_num(xj)})" for xj in xs[:k])
        terms.append(f"{_num(column[0])}{factors}")
    return " + ".join(terms)


def _num(value):
    return f"({value})" if value < 0 else str(value)

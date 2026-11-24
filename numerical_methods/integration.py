"""Numerical integration of f from a to b using n equal subintervals.

If a > b the result is negated, as it is for the exact integral.
"""

import math


def _step(a, b, n):
    if n < 1:
        raise ValueError("the number of subintervals must be at least 1")
    return (b - a) / n


def left(f, a, b, n):
    h = _step(a, b, n)
    return h * math.fsum(f(a + i * h) for i in range(n))


def right(f, a, b, n):
    h = _step(a, b, n)
    return h * math.fsum(f(a + i * h) for i in range(1, n + 1))


def trapezoid(f, a, b, n):
    h = _step(a, b, n)
    inside = math.fsum(f(a + i * h) for i in range(1, n))
    return h * ((f(a) + f(b)) / 2 + inside)


def simpson(f, a, b, n):
    h = _step(a, b, n)
    if n % 2:
        raise ValueError("Simpson's rule needs an even number of subintervals")
    odd = math.fsum(f(a + i * h) for i in range(1, n, 2))
    even = math.fsum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * (f(a) + 4 * odd + 2 * even + f(b))

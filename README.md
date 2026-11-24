# NumericalMethods

Root finding, curve fitting and integration techniques programmed in Python.

Needs Python 3.10 or newer. There are no other requirements, except
matplotlib if you want graphs.

## Usage

    git clone https://github.com/larchey/NumericalMethods.git
    cd NumericalMethods
    python -m numerical_methods --help

To install the `numerical-methods` command, with graphs:

    pip install ".[plot]"

| Command | What it does | Example |
| --- | --- | --- |
| `bisection` | root by halving an interval | `bisection "x**3-x-1" 1 2` |
| `newton` | root using the derivative | `newton "x**2-2" "2*x" 1` |
| `newton-piecewise` | Newton's method on a function in two pieces | `newton-piecewise "x+1" 1 "x-5" 1 0 2` |
| `secant` | root from two estimates | `secant "cos(x)-x" 0 1` |
| `mueller` | real or complex root from three estimates | `mueller "x**2+1" 0 1 2` |
| `integrate` | left, right, trapezoid and Simpson's rules | `integrate "sin(x)" 0 pi 100` |
| `lagrange` | Lagrange polynomial through points | `lagrange 0,0 1,1 2,4 --at 3 --plot` |
| `divided-difference` | Newton divided difference polynomial | `divided-difference 0,0 1,1 2,4 --save graph.png` |
| `to-base`, `from-base` | convert between decimal and bases 2 to 36 | `to-base 255 16` |
| `next-subset` | next binary string | `next-subset 1011` |
| `bubble-sort` | sort, showing each swap | `bubble-sort 3 1 2` |
| `iterate` | apply a function repeatedly | `iterate "cos(x)" 1 20` |

Root finders print every estimate and accept `--tol`, `--max-iter` and
`--quiet`.

Functions are written in terms of `x`, with `+ - * / // %`, `**` or `^` for
powers, the constants `pi`, `e` and `tau`, and `sqrt exp log log2 log10 abs
floor ceil` plus the trigonometric and hyperbolic functions and their inverses.
They are parsed rather than passed to `eval`, so they cannot run other code.

The methods can also be imported:

```python
from numerical_methods.roots import bisection

bisection(lambda x: x**2 - 2, 0, 2).root
```

## Tests

    pip install ".[plot,test]"
    pytest

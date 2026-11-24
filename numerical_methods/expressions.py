"""Turn a string such as "x**2 - sin(x)" into a function, without eval().

Only arithmetic, the variable x, and the names listed below are accepted, so
an expression cannot read files, import modules or call arbitrary code.
"""

import ast
import cmath
import math
import operator

CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}


class ExpressionError(ValueError):
    """The expression is not valid, or has no value at the requested point."""


def _real_or_complex(name):
    real, complex_ = getattr(math, name), getattr(cmath, name)
    return lambda *args: (
        complex_(*args) if any(isinstance(a, complex) for a in args) else real(*args)
    )


FUNCTIONS = {
    name: _real_or_complex(name)
    for name in (
        "sqrt", "exp", "log", "log10",
        "sin", "cos", "tan", "asin", "acos", "atan",
        "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
    )
}
FUNCTIONS |= {
    "abs": abs,
    "log2": math.log2,
    "floor": math.floor,
    "ceil": math.ceil,
}


def _power(base, exponent):
    # Integer powers are exact in Python, so 9**9**9 would run forever.
    # Past a few thousand bits, fall back to floats, which overflow instead.
    if isinstance(base, int) and isinstance(exponent, int):
        if base.bit_length() * abs(exponent) > 4096:
            return float(base) ** float(exponent)
    return base**exponent


_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: _power,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _compile(node):
    """Return a function of x that computes one node of the syntax tree."""
    match node:
        case ast.Constant(value=value) if type(value) in (int, float, complex):
            return lambda x: value
        case ast.Name(id="x"):
            return lambda x: x
        case ast.Name(id=name) if name in CONSTANTS:
            return lambda x: CONSTANTS[name]
        case ast.UnaryOp(op=op, operand=operand) if type(op) in _UNARY:
            apply, inner = _UNARY[type(op)], _compile(operand)
            return lambda x: apply(inner(x))
        case ast.BinOp(left=left, op=op, right=right) if type(op) in _BINARY:
            apply, lhs, rhs = _BINARY[type(op)], _compile(left), _compile(right)
            return lambda x: apply(lhs(x), rhs(x))
        case ast.Call(func=ast.Name(id=name), args=args, keywords=[]) if name in FUNCTIONS:
            apply, inners = FUNCTIONS[name], [_compile(a) for a in args]
            return lambda x: apply(*(inner(x) for inner in inners))
        case ast.Name(id=name):
            raise ExpressionError(f"unknown name {name!r}")
        case ast.Call(func=ast.Name(id=name)):
            raise ExpressionError(f"unknown function {name!r}")
    raise ExpressionError(f"unsupported syntax: {ast.unparse(node)}")


def parse_function(text, *, allow_complex=False):
    """Return a Python function of x. Both ** and ^ mean "to the power of"."""
    try:
        tree = ast.parse(text.strip().replace("^", "**"), mode="eval")
        compiled = _compile(tree.body)
    except ExpressionError:
        raise
    except (SyntaxError, ValueError, RecursionError, MemoryError) as error:
        raise ExpressionError(f"cannot understand {text!r}") from error

    def function(x):
        try:
            value = compiled(x)
        except (ArithmeticError, ValueError, TypeError) as error:
            raise ExpressionError(f"{text.strip()} fails at x = {x}: {error}") from error
        if isinstance(value, complex) and not allow_complex:
            raise ExpressionError(f"{text.strip()} is not real at x = {x}")
        return value

    return function


def parse_number(text):
    """Evaluate a constant expression such as "3", "-1.5" or "pi/2"."""

    try:
        tree = ast.parse(text.strip().replace("^", "**"), mode="eval")
    except (SyntaxError, ValueError, RecursionError, MemoryError) as error:
        raise ExpressionError(f"cannot understand {text!r}") from error
    if any(isinstance(n, ast.Name) and n.id == "x" for n in ast.walk(tree)):
        raise ExpressionError(f"expected a number, got {text!r}")
    return parse_function(text)(0)

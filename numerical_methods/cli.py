"""Command line interface: python -m numerical_methods <command> ..."""

import argparse
import sys

from . import discrete, integration, interpolation, roots
from .expressions import parse_function, parse_number


def _show_root(args, result, f):
    if not args.quiet:
        for i, estimate in enumerate(result.estimates, 1):
            print(f"{i:>4}  x = {estimate}  f(x) = {f(estimate)}")
    print(f"root: {result.root}  ({result.iterations} iterations)")


def _numbers(*texts):
    return [parse_number(text) for text in texts]


def run_bisection(args):
    f = parse_function(args.f)
    a, b = _numbers(args.a, args.b)
    _show_root(args, roots.bisection(f, a, b, args.tol, args.max_iter), f)


def run_newton(args):
    f, df = parse_function(args.f), parse_function(args.df)
    (x,) = _numbers(args.x)
    _show_root(args, roots.newton(f, df, x, args.tol, args.max_iter), f)


def run_newton_piecewise(args):
    f, df, g, dg = map(parse_function, (args.f, args.df, args.g, args.dg))
    split, x = _numbers(args.split, args.x)
    result = roots.newton_piecewise(f, df, g, dg, split, x, args.tol, args.max_iter)
    _show_root(args, result, lambda t: f(t) if t <= split else g(t))


def run_secant(args):
    f = parse_function(args.f)
    a, b = _numbers(args.a, args.b)
    _show_root(args, roots.secant(f, a, b, args.tol, args.max_iter), f)


def run_mueller(args):
    f = parse_function(args.f, allow_complex=True)
    points = _numbers(args.x0, args.x1, args.x2)
    result = roots.mueller(f, *points, args.tol, args.max_iter)
    _show_root(args, result, lambda x: f(complex(x)))


def run_integrate(args):
    f = parse_function(args.f)
    a, b = _numbers(args.a, args.b)
    for rule in (integration.left, integration.right, integration.trapezoid):
        print(f"{rule.__name__ + ':':<11}{rule(f, a, b, args.n)}")
    # Simpson's rule needs an even count, so an odd one is doubled.
    n = args.n if args.n % 2 == 0 else 2 * args.n
    note = "" if n == args.n else f"  (n = {n})"
    print(f"{'simpson:':<11}{integration.simpson(f, a, b, n)}{note}")


def _points(texts):
    points = []
    for text in texts:
        parts = text.split(",")
        if len(parts) != 2:
            raise ValueError(f"expected a point such as 1,2 but got {text!r}")
        points.append(_numbers(*parts))
    return [x for x, _ in points], [y for _, y in points]


def _show_polynomial(args, polynomial, expression, title, xs, ys):
    print(f"P(x) = {expression}")
    for text in args.at or []:
        (x,) = _numbers(text)
        print(f"P({x}) = {polynomial(x)}")
    if args.plot or args.save:
        from .plotting import plot_polynomial

        plot_polynomial(polynomial, xs, ys, title, args.save)


def run_lagrange(args):
    xs, ys = _points(args.points)
    _show_polynomial(
        args, interpolation.lagrange(xs, ys),
        interpolation.lagrange_expression(xs, ys), "Lagrange polynomial", xs, ys,
    )


def run_divided_difference(args):
    xs, ys = _points(args.points)
    for order, column in enumerate(interpolation.divided_differences(xs, ys)):
        print(f"order {order}: {column}")
    _show_polynomial(
        args, interpolation.newton_polynomial(xs, ys),
        interpolation.newton_expression(xs, ys),
        "Newton divided difference polynomial", xs, ys,
    )


def run_to_base(args):
    print(discrete.to_base(args.number, args.base))


def run_from_base(args):
    print(discrete.from_base(args.digits, args.base))


def run_sort(args):
    result, swaps = discrete.bubble_sort(_numbers(*args.values))
    if not args.quiet:
        for step in swaps:
            print(*step)
    print("sorted:", *result)


def run_next_subset(args):
    following = discrete.next_subset(args.bits)
    print("this string is all 1s" if following is None else following)


def run_iterate(args):
    (x,) = _numbers(args.x)
    values = discrete.iterate(parse_function(args.f), x, args.n)
    for i, value in enumerate(values, 1):
        print(f"f^{i}({x}) = {value}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="numerical_methods", description="Classic numerical methods."
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="command")

    def add(name, run, text, *arguments):
        command = commands.add_parser(name, help=text, description=text)
        command.set_defaults(run=run)
        for argument in arguments:
            command.add_argument(argument)
        return command

    for name, run, text, max_iter, arguments in (
        ("bisection", run_bisection, "find a root by halving [a, b]", 1000, ["f", "a", "b"]),
        ("newton", run_newton, "find a root using the derivative df", 100, ["f", "df", "x"]),
        ("newton-piecewise", run_newton_piecewise,
         "Newton's method on f for x <= split and g for x > split", 100,
         ["f", "df", "g", "dg", "split", "x"]),
        ("secant", run_secant, "find a root from two estimates", 100, ["f", "a", "b"]),
        ("mueller", run_mueller, "find a real or complex root from three estimates", 100,
         ["f", "x0", "x1", "x2"]),
    ):
        command = add(name, run, text, *arguments)
        command.add_argument("--tol", type=float, default=1e-10, help="default: %(default)s")
        command.add_argument("--max-iter", type=int, default=max_iter, help="default: %(default)s")
        command.add_argument("-q", "--quiet", action="store_true", help="only print the root")

    command = add("integrate", run_integrate, "integrate f from a to b", "f", "a", "b")
    command.add_argument("n", type=int, help="number of subintervals")

    for name, run, text in (
        ("lagrange", run_lagrange, "Lagrange polynomial through points"),
        ("divided-difference", run_divided_difference, "Newton polynomial through points"),
    ):
        command = add(name, run, text)
        command.add_argument("points", nargs="+", metavar="x,y")
        command.add_argument("--at", action="append", metavar="X", help="evaluate at X (repeatable)")
        command.add_argument("--plot", action="store_true", help="show a graph")
        command.add_argument("--save", metavar="FILE", help="save the graph instead of showing it")

    command = add("to-base", run_to_base, "write a decimal integer in another base")
    command.add_argument("number", type=int)
    command.add_argument("base", type=int)
    command = add("from-base", run_from_base, "convert digits in some base to decimal", "digits")
    command.add_argument("base", type=int)
    command = add("bubble-sort", run_sort, "sort numbers, showing each swap")
    command.add_argument("values", nargs="+")
    command.add_argument("-q", "--quiet", action="store_true", help="only print the result")
    add("next-subset", run_next_subset, "next binary string after bits", "bits")
    command = add("iterate", run_iterate, "apply f to x repeatedly, n times", "f", "x")
    command.add_argument("n", type=int)
    return parser


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    # argparse takes "-x**2" for an option; a leading space marks it as a value.
    argv = [
        f" {arg}" if arg[:1] == "-" and arg[:2] != "--" and arg not in ("-h", "-q") else arg
        for arg in argv
    ]
    args = build_parser().parse_args(argv)
    try:
        args.run(args)
    except ModuleNotFoundError as error:
        print(f"error: {error.name} is not installed; graphs need matplotlib", file=sys.stderr)
        return 1
    except (ValueError, ArithmeticError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0

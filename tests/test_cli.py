import pytest

from numerical_methods.cli import main


@pytest.mark.parametrize("argv, expected", [
    (["bisection", "x**2-2", "0", "2", "-q"], "root: 1.41421356"),
    (["newton", "-x**2+2", "-2*x", "1"], "root: 1.41421356"),
    (["newton-piecewise", "x+1", "1", "x-5", "1", "0", "-3"], "root: -1"),
    (["secant", "x-pi", "-1", "pi/2"], "root: 3.14159265"),
    (["mueller", "x**2+1", "0", "1", "2"], "root: 1j"),
    (["mueller", "exp(x)+1", "0", "1", "2"], "root: "),
    (["integrate", "x", "0", "1", "3"], "(n = 6)"),
    (["lagrange", "0,0", "1,1", "2,4", "--at", "3"], "P(3) = 9.0"),
    (["divided-difference", "-1,1", "0,0", "2,4", "--at", "-3"], "P(-3) = 9.0"),
    (["to-base", "-255", "16"], "-ff"),
    (["from-base", "-ff", "16"], "-255"),
    (["bubble-sort", "3", "-1", "2"], "sorted: -1 2 3"),
    (["next-subset", "1011"], "1100"),
    (["iterate", "2*x", "1", "3"], "f^3(1) = 8"),
])
def test_commands(argv, expected, capsys):
    assert main(argv) == 0
    assert expected in capsys.readouterr().out


@pytest.mark.parametrize("argv", [
    ["bisection", "x**2+1", "0", "2"],
    ["newton", "x**2+1", "2*x", "1"],
    ["integrate", "1/x", "0", "1", "4"],
    ["integrate", "x", "0", "1", "0"],
    ["lagrange", "1", "2,3"],
    ["iterate", "__import__('os')", "1", "1"],
])
def test_errors_are_reported(argv, capsys):
    assert main(argv) == 1
    assert capsys.readouterr().err.startswith("error: ")


def test_saves_a_plot(tmp_path):
    pytest.importorskip("matplotlib")
    target = tmp_path / "plot.png"
    assert main(["lagrange", "0,0", "1,1", "2,4", "--save", str(target)]) == 0
    assert target.stat().st_size > 0

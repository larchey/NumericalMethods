import pytest

from numerical_methods.discrete import bubble_sort, from_base, iterate, next_subset, to_base


def test_bases():
    assert to_base(255, 16) == "ff"
    assert to_base(0, 2) == "0"
    assert to_base(-5, 2) == "-101"
    assert from_base("FF", 16) == 255
    for base in range(2, 37):
        for number in (-1000, -1, 0, 1, 12345):
            text = to_base(number, base)
            assert from_base(text, base) == number == int(text, base)


@pytest.mark.parametrize("text, base", [("9", 2), ("", 10), ("-", 10), ("1", 1), ("1", 37), ("1.5", 10)])
def test_bad_digits(text, base):
    with pytest.raises(ValueError):
        from_base(text, base)


def test_bubble_sort():
    values = [1, 5, 3, 7, 4]
    result, swaps = bubble_sort(values)
    assert result == swaps[-1] == [1, 3, 4, 5, 7]
    assert values == [1, 5, 3, 7, 4]
    assert bubble_sort([]) == ([], [])


def test_next_subset_counts_in_binary():
    bits = "0000"
    for expected in range(1, 16):
        bits = next_subset(bits)
        assert int(bits, 2) == expected and len(bits) == 4
    assert next_subset(bits) is None
    for bad in ("", "012"):
        with pytest.raises(ValueError):
            next_subset(bad)


def test_iterate():
    assert iterate(lambda x: 2 * x, 1, 4) == [2, 4, 8, 16]
    assert iterate(lambda x: x, 1, 0) == []
    with pytest.raises(ValueError):
        iterate(lambda x: x, 1, -1)

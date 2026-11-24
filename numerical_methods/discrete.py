"""Number bases, bubble sort, binary subsets and function iteration."""

import string

DIGITS = string.digits + string.ascii_lowercase


def _check_base(base):
    if not 2 <= base <= len(DIGITS):
        raise ValueError(f"the base must be between 2 and {len(DIGITS)}")


def to_base(number, base):
    """Write an integer in another base: to_base(255, 16) is "ff"."""
    _check_base(base)
    sign, number = ("-", -number) if number < 0 else ("", number)
    digits = []
    while number:
        number, remainder = divmod(number, base)
        digits.append(DIGITS[remainder])
    return sign + ("".join(reversed(digits)) or "0")


def from_base(text, base):
    """Read an integer written in another base: from_base("ff", 16) is 255."""
    _check_base(base)
    digits = text.strip().lower()
    negative = digits.startswith("-")
    if negative:
        digits = digits[1:]
    if not digits:
        raise ValueError("no digits were given")
    total = 0
    for digit in digits:
        value = DIGITS.find(digit)
        if not 0 <= value < base:
            raise ValueError(f"{digit!r} is not a digit in base {base}")
        total = total * base + value
    return -total if negative else total


def bubble_sort(values):
    """Return the sorted values and the list as it stood after each swap."""
    values, swaps = list(values), []
    for done in range(len(values) - 1):
        swapped = False
        for k in range(len(values) - 1, done, -1):
            if values[k] < values[k - 1]:
                values[k], values[k - 1] = values[k - 1], values[k]
                swaps.append(list(values))
                swapped = True
        if not swapped:
            break
    return values, swaps


def next_subset(bits):
    """Return the next binary string, or None when bits is all ones."""
    if not bits or set(bits) - {"0", "1"}:
        raise ValueError("expected a string of 0s and 1s")
    position = bits.rfind("0")
    if position == -1:
        return None
    return bits[:position] + "1" + "0" * (len(bits) - position - 1)


def iterate(f, x, n):
    """Return [f(x), f(f(x)), ...] with n entries."""
    if n < 0:
        raise ValueError("n cannot be negative")
    values = []
    for _ in range(n):
        x = f(x)
        values.append(x)
    return values

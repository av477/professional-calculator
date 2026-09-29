import pytest

from app.calculator import add, divide, multiply, subtract

# This module tests the primitive arithmetic functions with normal, negative, fractional, and
# division-by-zero inputs.

@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (9, 6, 15),
        (-5, 11, 6),
        (0, 4, 4),
        (12.5, 3.5, 16.0),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (17, 9, 8),
        (-4, 6, -10),
        (0, 5, -5),
        (18.75, 2.25, 16.5),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (7, 8, 56),
        (-3, 9, -27),
        (0, 13, 0),
        (3.5, 4, 14.0),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (45, 5, 9),
        (24, 3, 8),
        (-16, 4, -4),
        (10.5, 2.5, 4.2),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (22, 0),
        (0, 0),
        (-8, 0),
    ],
)
def test_divide_by_zero(a, b):
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(a, b)



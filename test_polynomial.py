"""
Tests for polynomial.py
"""
# pylint: disable=missing-function-docstring

import pytest
from polynomial import Polynomial, INFINITY


zero = Polynomial.zero()
sample = Polynomial([1, -4, 0, 2])


def test_zero():
    assert Polynomial([]) == Polynomial([0]) == Polynomial([0, 0]) == zero


def test_eq():
    assert sample == Polynomial([1, -4, 0, 2])
    assert sample != "not ok"


def test_print():
    assert str(sample) == "+ 1*X^0 - 4*X^1 + 2*X^3"
    assert str(zero) == "0"


def test_copy():
    assert sample.copy() == Polynomial([1, -4, 0, 2])
    assert sample.copy() is not sample


def test_degree():
    assert sample.degree() == 3
    assert zero.degree() == -INFINITY


def test_neg():
    assert -sample == Polynomial([-1, 4, 0, -2])
    assert -zero == zero


def test_sum():
    assert zero + sample == sample + zero == sample
    assert sample == Polynomial([1, 0, 0]) + Polynomial([0, -4, 0, 2])
    assert sample + (-sample) == zero
    assert sample + sample == Polynomial([2, -8, 0, 4])


def test_sub():
    assert sample - Polynomial([1, 1]) == Polynomial([0, -5, 0, 2])
    assert sample - zero == sample
    assert zero - sample == -sample


def test_x():
    x = Polynomial.X()
    assert x.degree() == 1
    assert x.coeffs == [0, 1]
    assert x == Polynomial.X(1)
    assert Polynomial.X(2).degree() == 2
    assert Polynomial.X(2).coeffs == [0, 0, 1]


def test_mul():
    assert zero * zero == zero
    assert sample * zero == zero * sample == zero
    assert sample * Polynomial([1, 2]) == Polynomial([1, -2, -8, 2, 4])
    assert Polynomial([1, 2]) * sample == Polynomial([1, -2, -8, 2, 4])
    assert sample * Polynomial.X(2) == Polynomial([0, 0, 1, -4, 0, 2])
    assert sample * Polynomial([3]) == Polynomial([3, -12, 0, 6])
    with pytest.raises(TypeError):
        isinstance("not ok" * sample, Polynomial)


def test_lead_coefficient():
    with pytest.raises(ValueError):
        zero.lead_coefficient()
    assert sample.lead_coefficient() == 2
    assert Polynomial.X(5).lead_coefficient() == 1


def test_is_monic():
    assert not zero.is_monic()
    assert not sample.is_monic()
    assert Polynomial.X(5).is_monic()


def test_make_monic():
    with pytest.raises(ValueError):
        zero.make_monic()
    assert sample.make_monic() == Polynomial([0.5, -2, 0, 1])
    assert Polynomial.X(5).make_monic() == Polynomial.X(5)


def test_polydiv():
    assert divmod(sample, Polynomial([1, 1])) == (
        Polynomial([-2, -2, 2]),
        Polynomial([3]),
    )
    assert divmod(sample, sample) == (Polynomial([1]), zero)
    assert divmod(Polynomial.X(7), Polynomial.X(2)) == (
        Polynomial.X(5),
        zero,
    )
    with pytest.raises(ZeroDivisionError):
        divmod(sample, zero)


def test_gcd():
    one = Polynomial([1])
    assert Polynomial.gcd(sample, zero) == sample.make_monic()
    assert Polynomial.gcd(zero, sample) == sample.make_monic()
    assert Polynomial.gcd(zero, zero) == zero
    assert Polynomial.gcd(sample, Polynomial.X()) == one
    assert Polynomial.gcd(Polynomial([1, 2]), sample) == one
    assert Polynomial.gcd(sample, Polynomial([1, 2, 3])) == one
    assert Polynomial.gcd(Polynomial([-1, 0, 1]), Polynomial([1, 2, 1])) == Polynomial(
        [1, 1]
    )


def test_parse():
    assert Polynomial.parse("-X^0") == Polynomial([-1])
    assert Polynomial.parse("X^0") == Polynomial([1])
    assert Polynomial.parse("X") == Polynomial.X()
    assert Polynomial.parse("X^2") == Polynomial.X(2)
    assert Polynomial.parse("2 * X") == Polynomial([0, 2])
    assert Polynomial.parse("-2 * X") == Polynomial([0, -2])
    assert Polynomial.parse("2 + X") == Polynomial([2, 1])
    assert Polynomial.parse("-2 + X") == Polynomial([-2, 1])
    assert Polynomial.parse("2 * X^2 - 2 * X^2") == zero
    assert Polynomial.parse("1 + 2 * X + X^2") == Polynomial([1, 2, 1])
    assert Polynomial.parse("T^0 - T^1 + T^2", "T") == Polynomial([1, -1, 1])
    assert Polynomial.parse("U^3 - U", var="U") == Polynomial([0, -1, 0, 1])

    with pytest.raises(ValueError):
        Polynomial.parse("2*X - X^")
    with pytest.raises(ValueError):
        Polynomial.parse("2*X - a * X^2")
    with pytest.raises(ValueError):
        Polynomial.parse("2*X - X^r")
    with pytest.raises(ValueError):
        Polynomial.parse("X", "T")
    with pytest.raises(ValueError):
        Polynomial.parse("")


def test_pow():
    assert zero**0 == sample**0 == Polynomial([1])
    assert sample**1 == sample
    assert sample**2 == Polynomial([1, -8, 16, 4, -16, 0, 4])
    with pytest.raises(ValueError):
        pow(sample, -2)
    with pytest.raises(TypeError):
        pow(sample, "not ok")


def test_call():
    assert zero(2) == 0
    assert sample(0) == 1
    assert sample(1) == -1
    assert Polynomial.X(7)(2) == 2**7 == 128


def test_derivative():
    assert sample.derivative(0) == sample
    assert sample.derivative(1) == Polynomial([-4, 0, 6])
    assert sample.derivative(2) == Polynomial([0, 12])
    assert sample.derivative(3) == Polynomial([12])
    assert sample.derivative(4) == zero
    for n in range(1, 10):
        assert Polynomial.X(n).derivative() == Polynomial([n]) * Polynomial.X(n - 1)
    with pytest.raises(ValueError):
        sample.derivative(-5)
    with pytest.raises(TypeError):
        sample.derivative("not ok")

import pytest
from polynomial import Polynomial, INFINITY


def test_eq():
    assert Polynomial([1, 4, 2]) == Polynomial([1, 4, 2])
    assert not Polynomial([1, 4, 2]) == "somestring"


def test_print():
    assert str(Polynomial([1, 0, -2])) == "+ 1*X^0 - 2*X^2"
    assert str(Polynomial()) == "0"
    assert str(Polynomial([0])) == "0"
    assert str(Polynomial.zero()) == "0"


def test_copy():
    assert Polynomial([2, 3, 4]).copy() == Polynomial([2, 3, 4])
    assert Polynomial([2, 3, 4]).copy() is not Polynomial([2, 3, 4])


def test_degree():
    assert Polynomial([1]).degree() == 0
    assert Polynomial.zero().degree() == -INFINITY
    assert Polynomial([0, 0, 2, 0]).degree() == 2
    assert Polynomial([1, 0, 0, -1]).degree() == 3


def test_sum():
    assert -Polynomial([2, 3]) == Polynomial([-2, -3])
    assert Polynomial.zero() + Polynomial([2]) == Polynomial([2])
    assert Polynomial([2]) + Polynomial([3]) == Polynomial([5])
    assert Polynomial([2]) + Polynomial([-2]) == Polynomial.zero()
    assert Polynomial([4, 2, 1]) + Polynomial([0, 3, -1, 3]) == Polynomial([4, 5, 0, 3])
    assert Polynomial([0, 0, 1, 0]) + Polynomial([0, 0, 0, 1]) == Polynomial(
        [0, 0, 1, 1]
    )


def test_sub():
    assert Polynomial([2, 4]) - Polynomial([1, 1]) == Polynomial([1, 3])
    assert Polynomial([2, 4]) - Polynomial.zero() == Polynomial([2, 4])


def test_X():
    assert Polynomial.X().degree() == 1
    assert Polynomial.X().coeffs == [0, 1]
    assert Polynomial.X(2).degree() == 2
    assert Polynomial.X(2).coeffs == [0, 0, 1]
    assert Polynomial.X(1) == Polynomial.X()


def test_mul():
    assert Polynomial.zero() * Polynomial.zero() == Polynomial([0])
    assert Polynomial([1, 2, 3]) * Polynomial([0, 0, 1]) == Polynomial([0, 0, 1, 2, 3])
    assert Polynomial([1, 2, 3]) * Polynomial([0]) == Polynomial.zero()
    assert Polynomial([1, 1]) * Polynomial([1, 1]) == Polynomial([1, 2, 1])
    assert Polynomial([-1, 1]) * Polynomial([1, 1, 1, 1]) == Polynomial(
        [-1, 0, 0, 0, 1]
    )
    assert Polynomial([2, 3]) * 5 == Polynomial([10, 15])
    assert 2 * Polynomial([1, -1]) == Polynomial([2, -2])
    assert Polynomial([10, 2]) * 0.1 == Polynomial([1, 0.2])
    with pytest.raises(TypeError):
        "test" * Polynomial([10, 2])


def test_lead_coefficient():
    with pytest.raises(ValueError):
        Polynomial.zero().lead_coefficient()
    assert Polynomial([4, -1]).lead_coefficient() == -1
    assert Polynomial([2, 0, 2, 0]).lead_coefficient() == 2
    assert Polynomial([4, 1]).is_monic()
    assert not Polynomial([4, 2]).is_monic()


def test_normed():
    assert Polynomial([3, 2]).make_monic() == Polynomial([1.5, 1])
    with pytest.raises(ValueError):
        Polynomial.zero().make_monic()
    assert Polynomial.X(5).make_monic() == Polynomial.X(5)


def test_polydiv():
    assert divmod(Polynomial([5, 4, 1]), Polynomial([1, 1])) == (
        Polynomial([3, 1]),
        Polynomial([2]),
    )
    assert divmod(Polynomial.X(7), Polynomial.X(2)) == (
        Polynomial.X(5),
        Polynomial.zero(),
    )
    assert divmod(Polynomial([1, 1]), Polynomial([2])) == (
        Polynomial([0.5, 0.5]),
        Polynomial.zero(),
    )
    assert divmod(Polynomial([2, 3]), Polynomial([4, 2])) == (
        Polynomial([1.5]),
        Polynomial([-4]),
    )
    with pytest.raises(ZeroDivisionError):
        divmod(Polynomial([2, 2]), Polynomial.zero())


def test_gcd():
    assert Polynomial.gcd(Polynomial([1, 2]), Polynomial.zero()) == Polynomial([0.5, 1])
    assert Polynomial.gcd(Polynomial.zero(), Polynomial([1, 2])) == Polynomial([0.5, 1])
    assert Polynomial.gcd(Polynomial.zero(), Polynomial.zero()) == Polynomial.zero()
    assert Polynomial.gcd(Polynomial([0, 1, 1]), Polynomial([0, -1, 1])) == Polynomial(
        [0, 1]
    )
    assert Polynomial.gcd(
        Polynomial([0, 1, 1]), Polynomial([0, -1, 0, 1])
    ) == Polynomial([0, 1, 1])
    assert Polynomial.gcd(
        Polynomial([0, 2, 1]), Polynomial([0, -1, 0, 1])
    ) == Polynomial([0, 1])
    assert Polynomial.gcd(Polynomial([0, 1]), Polynomial([2, 1])) == Polynomial([1])
    assert Polynomial.gcd(
        Polynomial([-1, 0, -1, 0, 1, 0, 1]), Polynomial([1, -3, 2, -3, 1])
    ) == 0.9999999999999999 * Polynomial([1, 0, 1])
    # rounding error because of float's shortcomings, better use Decimal instead
    # https://docs.python.org/3/library/decimal.html


def test_parse():
    assert Polynomial.parse("2 * X^2 - 4 * X + 6 * X^0") == Polynomial([6, -4, 2])
    assert Polynomial.parse("2 * X^2 - 2 * X^2") == Polynomial.zero()
    assert Polynomial.parse("4 * X^4 - 2 * X^2 - 4 * X^6") == Polynomial(
        [0, 0, -2, 0, 4, 0, -4]
    )
    assert Polynomial.parse("X^0 + X + X^2") == Polynomial([1, 1, 1])
    assert Polynomial.parse("T^0 + T + T^2", "T") == Polynomial([1, 1, 1])
    assert Polynomial.parse("2 * X") == 2 * Polynomial.X()
    assert Polynomial.parse("-2 * X") == -2 * Polynomial.X()
    with pytest.raises(ValueError):
        Polynomial.parse("2*X - X^")
    with pytest.raises(ValueError):
        Polynomial.parse("2*X - a * X^2")
    with pytest.raises(ValueError):
        Polynomial.parse("2*X - X^r")
    with pytest.raises(ValueError):
        Polynomial.parse("X", "T")


def test_pow():
    assert Polynomial([1, 1]) ** 2 == Polynomial([1, 2, 1])
    assert Polynomial([1, 1]) ** 3 == Polynomial([1, 3, 3, 1])
    assert Polynomial([1, 1]) ** 4 == Polynomial([1, 4, 6, 4, 1])
    with pytest.raises(ValueError):
        pow(Polynomial([5, 2]), -2)
    with pytest.raises(TypeError):
        pow(Polynomial([5, 2]), "not ok")


def test_call():
    assert Polynomial([1, 0, 3])(2) == 13
    assert Polynomial.zero()(2) == 0
    assert Polynomial.X(7)(2) == 128


def test_derivative():
    assert Polynomial.X(5).derivative() == Polynomial([0, 0, 0, 0, 5])
    assert Polynomial([4, 2, 1]).derivative() == Polynomial([2, 2])
    assert Polynomial([4, 2, 1]).derivative(2) == Polynomial([2])
    assert Polynomial([4, 2, 1]).derivative(3) == Polynomial.zero()
    with pytest.raises(ValueError):
        Polynomial([1, 2]).derivative(-5)
    with pytest.raises(TypeError):
        Polynomial([0, 1]).derivative("not ok")

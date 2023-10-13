from polynomial import *


def test_print():
    assert str(Polynomial([1, 0, -2])) == "+ 1*X^0 - 2*X^2"
    assert str(Polynomial()) == "0"
    assert str(Polynomial([0])) == "0"
    assert str(Polynomial.zero()) == "0"


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


def test_lead_coefficient():
    assert Polynomial.zero().lead_coefficient() == 0
    assert Polynomial([4, -1]).lead_coefficient() == -1
    assert Polynomial([2, 0, 2, 0]).lead_coefficient() == 2
    assert Polynomial([4, 1]).is_monic()
    assert not Polynomial([4, 2]).is_monic()


def test_normed():
    assert Polynomial([3, 2]).normed() == Polynomial([1.5, 1])
    assert Polynomial.zero().normed() == Polynomial.zero()
    assert Polynomial.X(5).normed() == Polynomial.X(5)


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


def test_gcd():
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
    ) == Polynomial(
        [0.9999999999999999, 0, 0.9999999999999999]  # rounding error!
    )


if __name__ == "__main__":
    test_print()
    test_degree()
    test_sum()
    test_sub()
    test_X()
    test_mul()
    test_lead_coefficient()
    test_normed()
    test_polydiv()
    test_gcd()
    print("Everything passed")

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
    assert Polynomial.zero().add(Polynomial([2])) == Polynomial([2])
    assert Polynomial([2]).add(Polynomial([3])) == Polynomial([5])
    assert Polynomial([2]).add(Polynomial([-2])) == Polynomial.zero()
    assert Polynomial([4, 2, 1]).add(Polynomial([0, 3, -1, 3])) == Polynomial(
        [4, 5, 0, 3]
    )
    assert Polynomial([0, 0, 1, 0]).add(Polynomial([0, 0, 0, 1])) == Polynomial(
        [0, 0, 1, 1]
    )


def test_subtr():
    assert Polynomial([2, 4]).subtr(Polynomial([1, 1])) == Polynomial([1, 3])
    assert Polynomial([2, 4]).subtr(Polynomial.zero()) == Polynomial([2, 4])


def test_X():
    assert Polynomial.X().degree() == 1
    assert Polynomial.X().coeffs == [0, 1]
    assert Polynomial.X(2).degree() == 2
    assert Polynomial.X(2).coeffs == [0, 0, 1]
    assert Polynomial.X(1) == Polynomial.X()


def test_mult():
    assert Polynomial.zero().mult(Polynomial.zero()) == Polynomial([0])
    assert Polynomial([1, 2, 3]).mult(Polynomial([0, 0, 1])) == Polynomial(
        [0, 0, 1, 2, 3]
    )
    assert Polynomial([1, 2, 3]).mult(Polynomial([0])) == Polynomial.zero()
    assert Polynomial([1, 1]).mult(Polynomial([1, 1])) == Polynomial([1, 2, 1])
    assert Polynomial([-1, 1]).mult(Polynomial([1, 1, 1, 1])) == Polynomial(
        [-1, 0, 0, 0, 1]
    )


def test_lead_coefficient():
    assert Polynomial.zero().lead_coefficient() == 0
    assert Polynomial([4, -1]).lead_coefficient() == -1
    assert Polynomial([2, 0, 2, 0]).lead_coefficient() == 2


def test_scale():
    assert Polynomial([0, 1]).scale(2) == Polynomial([0, 2])
    assert Polynomial([1, 1, 1]).scale(0) == Polynomial.zero()
    assert Polynomial([4, -1, 2, 0]).scale(-1) == Polynomial([-4, 1, -2])


def test_polydiv():
    assert Polynomial([5, 4, 1]).div(Polynomial([1, 1])) == (
        Polynomial([3, 1]),
        Polynomial([2]),
    )
    assert Polynomial.X(7).div(Polynomial.X(2)) == (Polynomial.X(5), Polynomial.zero())
    assert Polynomial([1, 1]).div(Polynomial([2])) == (
        Polynomial([0.5, 0.5]),
        Polynomial.zero(),
    )
    assert Polynomial([2, 3]).div(Polynomial([4, 2])) == (
        Polynomial([1.5]),
        Polynomial([-4]),
    )


if __name__ == "__main__":
    test_print()
    test_degree()
    test_sum()
    test_subtr()
    test_mult()
    test_lead_coefficient()
    test_scale()
    test_polydiv()
    print("Everything passed")

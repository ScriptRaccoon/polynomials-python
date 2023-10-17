"""
Module containing the Polynomial class. See docstring there.
"""

from __future__ import annotations
from typing import cast
from utils import parse_by_operators

INFINITY = float("inf")
"""Number 'infinity'"""


class Polynomial:
    """
    Class for polynomials in one variable over the rational numbers

    Attributes:

        coeffs - List of coefficients. The list [a_0,a_1,a_2,...]
            represents the polynomial a_0 + a_1 X + a_2 X^2 + ....

        var - Variable of the polynomial, defaults to X. Used for printing.

    """

    def __init__(self, coeffs: list[float | int], var: str = "X") -> None:
        """
        Constructor function creating a new polynomial.

        Arguments:
            coeffs - List of coefficients

            var - Variable for the polynomial
        """
        self.coeffs = coeffs
        self.var = var
        self.__shorten()

    def __shorten(self) -> None:
        """
        Internal method removing the zero coefficients in the end.
        """
        i = len(self) - 1
        while i >= 0 and self.coeffs[i] == 0:
            self.coeffs.pop()
            i -= 1

    def copy(self) -> Polynomial:
        """
        Creates a copy of a polynomial
        """
        return Polynomial(self.coeffs[:])

    def __eq__(self, other: object) -> bool:
        """
        Checks if a polynomial is equal to another polynomial.
        This Dunder method is executed when writing p == q for a polynomial p.
        """
        if not isinstance(other, Polynomial):
            return False
        return self.coeffs == other.coeffs

    def __str__(self) -> str:
        """
        Dunder method producing a readable string representation of a polynomial p.
        This string is printed when calling print(p).
        For example, Polynomial([0,1,3]) will return the string "1*X^1 + 3*X^3".

        Returns:
            String representation of a polynomial
        """
        if all(c == 0 for c in self.coeffs):
            return "0"

        s = ""

        for i, coeff in enumerate(self.coeffs):
            if coeff == 0:
                continue

            if coeff > 0:
                s += f"+ {coeff}*{self.var}^{i} "
            elif coeff < 0:
                s += f"- {-coeff}*{self.var}^{i} "

        return s.strip()

    def __len__(self) -> int:
        """
        Computes the length of a polynomial p, defined as the length of its
        list of coefficients. This Dunder method can be called with len(p).

        Returns:
            Length of the list of coefficients
        """
        return len(self.coeffs)

    def __call__(self, num: int | float) -> int | float:
        """
        Evaluates a polynomial p at any given number num.
        This Dunder method can be called as p(num).

        Arguments:
            num - Any number

        Returns:
            Value of the polynomial at the given number
        """
        return sum(self.coeffs[k] * num**k for k in range(len(self)))

    @staticmethod
    def zero() -> Polynomial:
        """
        Computes the zero polynomial, whose list of coefficients is empty.

        Returns:
            The zero polynomial
        """
        return Polynomial([])

    def is_zero(self) -> bool:
        """
        Checks if a polynomial is zero.

        Returns:
            True if the polynomial is zero, False otherwise
        """
        return len(self) == 0

    def degree(self) -> float | int:
        """
        Computes the degree of a polynomial.
        The zero polynomial has degree -infinity, which is a float.
        For all other polynomials the degree is a natural number.

        Returns:
            The degree of the polynomial
        """
        if len(self) == 0:
            return -INFINITY
        return len(self) - 1

    def __scale(self, u: float | int) -> Polynomial:
        """
        Returns a scalar multiple of the polynomial.

        Arguments:
            u: The scalar

        Returns:
            The scalar multiple u * self
        """
        return Polynomial([u * coeff for coeff in self.coeffs])

    @staticmethod
    # pylint: disable=invalid-name
    def X(n: int = 1) -> Polynomial:
        """
        Computes the polynomial X^n, the default being n = 1.
        For example, X^3 has coefficient list [0,0,0,1].

        Arguments:
            n: The exponent

        Returns:
            The polynomial X^n
        """
        coeffs = cast(list[int | float], [0] * n + [1])
        return Polynomial(coeffs)

    def lead_coefficient(self) -> float | int:
        """
        Computes the lead coefficient of a polynomial, which is the last non-zero coefficient.
        The zero polynomial has no lead coefficient.

        Returns:
            The lead coefficient

        Raises:
            ValueError: When the polynomial is zero
        """
        if self.is_zero():
            raise ValueError("The zero polynomial has no lead coefficient.")
        return self.coeffs[-1]

    def is_monic(self) -> bool:
        """
        Checks if a polynomial is monic, i.e. its lead coefficient is 1.
        The zero polynomial is not monic.

        Returns:
            True if the polynomial is monic, False otherwise
        """
        return not self.is_zero() and self.lead_coefficient() == 1

    def make_monic(self) -> Polynomial:
        """
        Makes a polynomial monic by dividing it through its lead coefficient.
        The zero polynomial cannot be made monic, since it has no lead coefficient.

        Returns:
            A new monic polynomial

        Raises:
            ValueError: When the polynomial is zero
        """
        if self.is_zero():
            raise ValueError("The zero polynomial cannot be made monic.")
        a = self.lead_coefficient()
        return self.__scale(1 / a)

    def __neg__(self) -> Polynomial:
        """
        Computes the additive inverse of a polynomial p.
        This Dunder method can be executed by writing -p.

        Returns:
            The additive inverse
        """
        return self.__scale(-1)

    def __add__(self, other: Polynomial) -> Polynomial:
        """
        Computes the sum of two polynomials.
        This Dunder method can be executing by writing p + q.

        Arguments:
            other: a polynomial

        Returns:
            The sum of the two polynomials
        """
        n = max(len(self), len(other))
        sum_coeffs = []
        for i in range(n):
            a = self.coeffs[i] if i < len(self) else 0
            b = other.coeffs[i] if i < len(other) else 0
            sum_coeffs.append(a + b)
        return Polynomial(sum_coeffs)

    def __sub__(self, q: Polynomial) -> Polynomial:
        """
        Computes the difference (subtraction) of two polynomials.
        This Dunder method can be executed by writing p - q.

        Arguments:
            other: a polynomial

        Returns:
            The difference of the two polynomials
        """
        return self + (-q)

    def __mul__(self, other: Polynomial) -> Polynomial:
        """
        Computes the product of two polynomials.
        This Dunder method can be executed by writing p * q.

        Arguments:
            other: a polynomial

        Returns:
            The product of two polynomials
        """
        coeffs: list[int | float] = []
        if self.is_zero() or other.is_zero():
            return Polynomial.zero()
        n = cast(int, self.degree())
        m = cast(int, other.degree())
        for k in range(n + m + 1):
            seq = [
                self.coeffs[i] * other.coeffs[k - i]
                for i in range(k + 1)
                if i <= n and k - i <= m
            ]
            coeffs.append(sum(seq))
        return Polynomial(coeffs)

    def __pow__(self, n: int) -> Polynomial:
        """
        Computes the nth power of a polynomial p.
        This Dunder method can be executed by writing p ** n.

        Returns:
            The power

        Raises:
            TypeError: When the exponent is not an integer
            ValueError: When the exponent is negative
        """

        if not isinstance(n, int):
            raise TypeError("Exponent needs to be an integer.")
        if n < 0:
            raise ValueError("Exponent needs to be non-negative.")
        if n == 0:
            return Polynomial([1])
        return self * pow(self, n - 1)

    def __divmod__(self, other: Polynomial) -> tuple[Polynomial, Polynomial]:
        """
        Polynomial division: Given two polynomials self, other, computes
        a tuple (q,r) of polynomials such that self = q * other + r
        and deg(r) < deg(other). The implementation is recursive.
        This Dunder method can be executed by writing divmod(self,other).

        Arguments:
            other: any polynomial

        Returns:
            Tuple (q,r) consiting of quotient q and remainder r of the polynomial division

        Raises:
            ZeroDivisionError: When the other polynomial is zero
        """
        if other.is_zero():
            raise ZeroDivisionError(
                "Polynomial division is not allowed for the zero polynomial."
            )

        if self.is_zero():
            return Polynomial.zero(), Polynomial.zero()

        n = cast(int, self.degree())
        m = cast(int, other.degree())

        if n < m:
            return Polynomial.zero(), self

        lead_self = self.lead_coefficient()
        lead_other = other.lead_coefficient()

        corr_term = Polynomial([lead_self / lead_other]) * Polynomial.X(n - m)
        f = self - corr_term * other
        quot, rem = divmod(f, other)

        return quot + corr_term, rem

    @staticmethod
    def gcd(p: Polynomial, q: Polynomial) -> Polynomial:
        """
        Computes the greatest common divisor of two polynomials with the
        Euclidean algorithm (https://en.wikipedia.org/wiki/Euclidean_algorithm).
        To make the gcd unique, the result is made monic in case it's non-zero.

        Arguments:
            other: any polynomial

        Returns:
            The greatest common divisor (gcd) of the two polynomials
        """
        if p.is_zero() and q.is_zero():
            return p
        if p.is_zero():
            return q.make_monic()
        if q.is_zero():
            return p.make_monic()
        if p.degree() < q.degree():
            # pylint: disable=arguments-out-of-order
            return Polynomial.gcd(q, p)
        _, rem = divmod(p, q)
        return Polynomial.gcd(q, rem)

    @staticmethod
    def __parse_monomial(monomial_str: str, var="X") -> tuple[int, int | float]:
        """
        If the monomial string is c * X^k, returns the tuple (k, c).
        The strings X^k, c, c * X, X are also parsed correctly as
        (k,1), (0,c), (1,c), (1,1).

        Arguments:
            monomial_str: any string which is supposed to represent a monomial
            var: the variable of the monomial, defaults to X

        Returns:
            the tuple (k,c) such that the monomial is represented by c * X^k

        Raises:
            ValueError: when the string cannot be parsed as a monomial
        """
        if monomial_str.isnumeric():
            return 0, int(monomial_str)
        if "*" in monomial_str:
            coeff_str, power = monomial_str.split("*")
        else:
            coeff_str = "1"
            power = monomial_str
        try:
            coeff = float(coeff_str)
        except Exception as exc:
            raise ValueError(f"Coefficient '{coeff_str}' is not a number.") from exc
        if power == var:
            power = var + "^1"

        power_valid = (
            power.startswith(var + "^") and power[2:].isnumeric() and len(power) > 2
        )
        if not power_valid:
            raise ValueError(f"'{power}' is not a valid power of {var}.")

        exponent = int(power[2:])

        return exponent, coeff

    @staticmethod
    def parse(poly_str: str, var="X") -> Polynomial:
        """
        Parses a string to a polynomial if possible.
        For example, "2 * X^2 - 4 * X + 6 * X^0" returns Polynomial([6, -4, 2]).

        Arguments:
            poly_str: a string representation a polynomial
            var: the variable, defaults to "X"

        Returns:
            a polynomial representing the given string

        Raises:
            ValueError: When the string cannot be parsed to a polynomial
        """
        coeffs: list[float | int] = [0]
        sign = {"+": 1, "-": -1}
        operators = ["+", "-"]
        parse_by_operators(poly_str, operators, "+")

        for operator, monomial_str in parse_by_operators(poly_str, operators, "+"):
            exponent, coeff = Polynomial.__parse_monomial(monomial_str, var)
            while exponent >= len(coeffs):
                coeffs.append(0)
            coeffs[exponent] += sign[operator] * coeff

        return Polynomial(coeffs, var)

    def derivative(self, n: int = 1) -> Polynomial:
        """
        Computes the n-th derivative of a polynomial.

        Arguments:
            n: the degree of the derivative, defaults to 1

        Returns:
            the n-th derivative

        Raises:
            TypeError: When the exponent is not an integer
            ValueError: When the exponent is negative
        """
        if not isinstance(n, int):
            raise TypeError("Exponent needs to be an integer.")
        if n < 0:
            raise ValueError("Exponent needs to be non-negative.")
        if n == 0:
            return self
        p = self.derivative(n - 1)
        new_coeffs = [(k + 1) * p.coeffs[k + 1] for k in range(len(p) - 1)]
        return Polynomial(new_coeffs)

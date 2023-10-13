from __future__ import annotations

INFINITY = float("inf")


class Polynomial:
    """Class for polynomials over the rational numbers
    The polynomial a_0 + a_1 X + a_2 X^2 + .... is encoded by the finite sequence
    [a_0, a_1, a_2, ...]"""

    def __init__(self, coeffs: list[float | int] = [], var: str = "X"):
        """constructor accepting a list of coefficients"""
        self.coeffs = coeffs
        self.var = var
        self.__shorten()

    def __shorten(self):
        """removes the zero coefficients in the end"""
        i = len(self) - 1
        while i >= 0 and self.coeffs[i] == 0:
            self.coeffs.pop()
            i -= 1

    def __eq__(self, other: Polynomial):
        """equality test"""
        return self.coeffs == other.coeffs

    def __str__(self):
        """pretty string representation"""
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

    def __len__(self):
        """returns the number of coefficients"""
        return len(self.coeffs)

    def __call__(self, val: int | float) -> int | float:
        return sum([self.coeffs[k] * val**k for k in range(len(self))])

    @staticmethod
    def zero():
        """returns the zero polynomial"""
        return Polynomial([])

    def is_zero(self):
        """checks if polynomial is zero"""
        return len(self) == 0

    def degree(self):
        """returns the degree of the polynomial.
        the zero polynomial has degree -infinity"""
        if len(self) == 0:
            return -INFINITY
        return len(self) - 1

    def __scale(self, u: float | int):
        """returns a scalar multiple of the polynomial"""
        return Polynomial([u * coeff for coeff in self.coeffs])

    @staticmethod
    def X(n: int = 1):
        """returns the polynomial X^n, with n=1 being default"""
        coeffs = [0] * n + [1]
        return Polynomial(coeffs)

    def lead_coefficient(self) -> float | int:
        """gets the lead coefficient of the polynomial, 0 in case it's the zero polynomial"""
        if self.is_zero():
            return 0
        return self.coeffs[-1]

    def is_monic(self) -> bool:
        """checks if a polynomial is monic"""
        return self.lead_coefficient() == 1

    def normed(self):
        """makes a polynomial monic"""
        if self.is_zero():
            return self
        a = self.lead_coefficient()
        return self.__scale(1 / a)

    def __neg__(self):
        """computes the additive inverse of a polynomial"""
        return self.__scale(-1)

    def __add__(self, other: Polynomial):
        """adds two polynomials"""
        n = max(len(self), len(other))
        sum_coeffs = []
        for i in range(n):
            a = self.coeffs[i] if i < len(self) else 0
            b = other.coeffs[i] if i < len(other) else 0
            sum_coeffs.append(a + b)
        return Polynomial(sum_coeffs)

    def __sub__(self, q: Polynomial):
        "subtracts two polynomials"
        return self + (-q)

    def __mul__(self, other: Polynomial):
        """multiplies two polynomials"""
        if isinstance(other, float | int):
            return self.__scale(other)
        coeffs = []
        n = self.degree()
        m = other.degree()
        if n < 0 or m < 0:
            return Polynomial.zero()
        for k in range(n + m + 1):
            seq = [
                self.coeffs[i] * other.coeffs[k - i]
                for i in range(k + 1)
                if i <= n and k - i <= m
            ]
            coeffs.append(sum(seq))
        return Polynomial(coeffs)

    def __rmul__(self, other):
        """computes a scalar multiple with a polynomial on the right"""
        if isinstance(other, float | int):
            return self.__scale(other)
        return None

    def __pow__(self, n: int) -> Polynomial:
        """computes the power p^n of a polynomial to a natural number n"""
        if n == 0:
            return Polynomial([1])
        return self * pow(self, n - 1)

    def __divmod__(self, other: Polynomial):
        """computes a tuple (q,r) of polynomials such that self = q * other + r
        and deg(r) < deg(other). only allowed when other is not zero."""
        err_msg = "Polynomial division is not allowed for the zero polynomial."
        if other.is_zero():
            raise ZeroDivisionError(err_msg)

        n = self.degree()
        m = other.degree()

        if n < m:
            return Polynomial.zero(), self

        lead_self = self.lead_coefficient()
        lead_other = other.lead_coefficient()

        corr_term = Polynomial.X(n - m) * (lead_self / lead_other)
        f = self - corr_term * other
        quot, rem = divmod(f, other)

        return quot + corr_term, rem

    @staticmethod
    def gcd(p: Polynomial, q: Polynomial):
        """computes the greatest common divisor of two polynomials p,q
        with the Euclidean algorithm"""
        if p.is_zero():
            return q.normed()
        if q.is_zero():
            return p.normed()
        if p.degree() < q.degree():
            return Polynomial.gcd(q, p)
        _, rem = divmod(p, q)
        return Polynomial.gcd(q, rem)

    @staticmethod
    def parse(str: str, var="X") -> Polynomial:
        """parses a string to a polynomial if possible"""
        coeffs = []
        str = str.strip().replace("-", "+-").replace(" ", "")
        summands = str.split("+")
        for summand in summands:
            if len(summand) == 0:
                continue
            if "*" in summand:
                coeff, monomial = summand.split("*")
            else:
                coeff, monomial = "1", summand

            try:
                coeff = float(coeff)
            except:
                raise ValueError(f"Coefficient '{coeff}' is not a number")

            if monomial == var:
                monomial += "^1"
            monomial_valid = (
                monomial.startswith(var + "^")
                and monomial[2:].isnumeric()
                and len(monomial) > 2
            )
            if not monomial_valid:
                raise ValueError(f"'{monomial}' is not a valid monomial in {var}")

            exponent = int(monomial[2:])
            while exponent >= len(coeffs):
                coeffs.append(0)

            coeffs[exponent] += coeff

        return Polynomial(coeffs, var)

    def derivative(self, n: int = 1):
        if n == 0:
            return self
        p = self.derivative(n - 1)
        new_coeffs = [(k + 1) * p.coeffs[k + 1] for k in range(len(p) - 1)]
        return Polynomial(new_coeffs)

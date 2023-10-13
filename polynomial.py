from __future__ import annotations

INFINITY = float("inf")  # gros schreiben evtl


class Polynomial:
    """Class for polynomials over the rational numbers
    The polynomial a_0 + a_1 X + a_2 X^2 + .... is encoded by the finite sequence
    [a_0, a_1, a_2, ...]"""

    def __init__(self, coeffs: list[float] = []):
        """constructor accepting a list of coefficients"""
        self.coeffs = coeffs
        self.__shorten()

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
                s += f"+ {coeff}*X^{i} "
            elif coeff < 0:
                s += f"- {-coeff}*X^{i} "

        return s.strip()

    @staticmethod
    def zero():
        """returns the zero polynomial"""
        return Polynomial([])

    def is_zero(self):
        """checks if polynomial is zero"""
        return len(self.coeffs) == 0

    def __shorten(self):
        """removes the zero coefficients in the end"""
        i = len(self.coeffs) - 1
        while i >= 0 and self.coeffs[i] == 0:
            self.coeffs.pop()
            i -= 1

    def degree(self):
        """returns the degree of the polynomial.
        the zero polynomial has degree -infinity"""
        if len(self.coeffs) == 0:
            return -INFINITY
        return len(self.coeffs) - 1

    def scale(self, u):
        """returns a scalar multiple of the polynomial"""
        return Polynomial([u * c for c in self.coeffs])

    def add(self, other: Polynomial):
        """adds a polynomial to the polynomial, returns a new one"""
        n = max(len(self.coeffs), len(other.coeffs))
        sum_coeffs = []
        for i in range(n):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            sum_coeffs.append(a + b)
        return Polynomial(sum_coeffs)

    def subtr(self, q):
        "substracts a polynomial from the polynomial, returns a new one"
        return self.add(q.scale(-1))

    @staticmethod
    def X(n=1):
        """returns the polynomial X^n, with n=1 being default"""
        coeffs = [0] * n + [1]
        return Polynomial(coeffs)

    def mult(self, other):
        """multiplies the polynomial with another polynomial, returns a new one"""
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

    def lead_coefficient(self) -> float:
        """gets the lead coefficient of the polynomial, 0 in case it's the zero polynomial"""
        if self.is_zero():
            return 0
        return self.coeffs[-1]

    def div(self, other):
        """polynomial division: computes a tuple (q,r) of polynomials such that
        self = q * g + r and deg(r) < deg(g). only allowed when g is not zero."""
        if other.is_zero():
            raise ZeroDivisionError(
                "Polynomial division is not allowed for the zero polynomial."
            )

        n = self.degree()
        m = other.degree()

        if n < m:
            return Polynomial.zero(), self

        lead_self = self.lead_coefficient()
        lead_other = other.lead_coefficient()

        corr_term = Polynomial.X(n - m).scale(lead_self / lead_other)
        f = self.subtr(corr_term.mult(other))
        quot, rem = f.div(other)

        return quot.add(corr_term), rem

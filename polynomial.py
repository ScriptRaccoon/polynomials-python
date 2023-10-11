inf = float("inf")


class Polynomial:
    """Class for polynomials over the rational numbers
    The polynomial a_0 + a_1 X + a_2 X^2 + .... is encoded by the finite sequence
    [a_0, a_1, a_2, ...]"""

    def __init__(self, coeffs=[]):
        """constructor accepting a list of coefficients"""
        self.coeffs = coeffs
        self.shorten()

    def __eq__(self, other):
        """equality test"""
        return self.coeffs == other.coeffs

    def __str__(self):
        """pretty string representation"""
        if all(c == 0 for c in self.coeffs):
            return "0"

        s = ""

        for i, c in enumerate(self.coeffs):
            if c == 0:
                continue

            if c > 0:
                s += f"+ {c}*X^{i} "
            elif c < 0:
                s += f"- {-c}*X^{i} "

        return s.strip()

    def zero():
        """returns the zero polynomial"""
        return Polynomial([])

    def is_zero(self):
        """checks if polynomial is zero"""
        return len(self.coeffs) == 0

    def shorten(self):
        """removes the zero coefficients in the end"""
        if len(self.coeffs) == 0:
            return
        i = len(self.coeffs) - 1
        while i >= 0 and self.coeffs[i] == 0:
            del self.coeffs[i]
            i -= 1

    def degree(self):
        """returns the degree of the polynomial.
        the zero polynomial has degree -infinity"""
        if len(self.coeffs) == 0:
            return -inf
        return len(self.coeffs) - 1

    def scale(self, u):
        """returns a scalar multiple of the polynomial"""
        return Polynomial([u * c for c in self.coeffs])

    def add(self, q):
        """adds a polynomial to the polynomial, returns a new one"""
        n = max(len(self.coeffs), len(q.coeffs))
        sum_coeffs = []
        for i in range(n):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = q.coeffs[i] if i < len(q.coeffs) else 0
            sum_coeffs.append(a + b)
        return Polynomial(sum_coeffs)

    def subtr(self, q):
        """substracts a polynomial from the polynomial, returns a new one"""
        n = max(len(self.coeffs), len(q.coeffs))
        substr_coeffs = []
        for i in range(n):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = q.coeffs[i] if i < len(q.coeffs) else 0
            substr_coeffs.append(a - b)
        return Polynomial(substr_coeffs)

    def X(n=1):
        """returns the polynomial X^n, with n=1 being default"""
        coeffs = [1 if k == n else 0 for k in range(n + 1)]
        return Polynomial(coeffs)

    def mult(self, q):
        """multiplies the polynomial with another polynomial, returns a new one"""
        coeffs = []
        n = self.degree()
        m = q.degree()
        if n < 0 or m < 0:
            return Polynomial.zero()
        for k in range(n + m + 1):
            a = [
                self.coeffs[i] * q.coeffs[k - i]
                for i in range(k + 1)
                if i <= n and k - i <= m
            ]
            coeffs.append(sum(a))
        return Polynomial(coeffs)

    def lead_coefficient(self):
        """gets the lead coefficient of the polynomial, 0 in case it's the zero polynomial"""
        if self.is_zero():
            return 0
        return self.coeffs[-1]

    def div(self, g):
        """polynomial division: computes a tuple (q,r) of polynomials such that
        self = q * g + r and deg(r) < deg(g). only allowed when g is not zero."""
        if g.is_zero():
            raise Exception(
                "Polynomial division is not allowed for the zero polynomial."
            )

        n = self.degree()
        m = g.degree()

        if n < m:
            return (Polynomial.zero(), self)

        a = self.lead_coefficient()
        b = g.lead_coefficient()

        h = Polynomial.X(n - m).scale(a / b)
        f = self.subtr(h.mult(g))
        q, r = f.div(g)

        return (q.add(h), r)

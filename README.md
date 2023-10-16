# Polynomial class for Python

The class `Polynomial` implements several functions to calculate with polynomials in Python. These are encoded by their lists of coefficients. The class is mainly a personal exercise to get used with OOP, TDD, type checking and linting in Python. For production-level applications, better choose [numpy.polynomials](https://numpy.org/doc/stable/reference/routines.polynomials.html).

## Examples

```python
# Parsing
Polynomial.parse("1 + 2 * X + 3 * X^2") == Polynomial([1, 2, 3])

# Printing
str(Polynomial([1, -4, 0, 2])) == "+ 1*X^0 - 4*X^1 + 2*X^3"

# Products
Polynomial([1, -4, 0, 2]) * Polynomial.X(2) == Polynomial([0, 0, 1, -4, 0, 2])

# Evaluation
Polynomial([1, -4, 0, 2])(1) == -1

# Monic polynomials
Polynomial([1, -4, 0, 2]).make_monic() == Polynomial([0.5, -2, 0, 1])

# Derivative
Polynomial([1, -4, 0, 2]).derivative(2) == Polynomial([0, 12])

# Greatest common divisor
Polynomial.gcd(Polynomial([-1, 0, 1]), Polynomial([1, 2, 1])) == Polynomial([1, 1])

# Polynomial division (quotient and remainder)
divmod(Polynomial([1, -4, 0, 2]), Polynomial([1, 1])) == (
    Polynomial([-2, -2, 2]),
    Polynomial([3]),
)
```

## Commands for Development

1. Execute `polynomial.py` continuously with [nodemon](https://www.npmjs.com/package/nodemon): `nodemon polynomial.py`

2. Run the tests with [pytest](https://pypi.org/project/pytest/): `pytest`

3. Run the tests continuously using [pytest-watch](https://pypi.org/project/pytest-watch/): `ptw`

4. Generate a test coverage report with [pytest-cov](https://pypi.org/project/pytest-cov/): `pytest --cov --cov-report term-missing`

5. Type checking with [mypy](https://pypi.org/project/mypy/): `mypy polynomial.py`

6. Static code analysis with [pylint](https://pypi.org/project/pylint/): `pylint polynomial.py`

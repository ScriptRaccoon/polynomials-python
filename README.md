# Polynomial class for Python

This class implements several functions to calculate with polynomials. It is mainly a personal exercise to get used with OOP, TDD and Typechecking in Python. For production-level applications, probably [numpy.polynomials](https://numpy.org/doc/stable/reference/routines.polynomials.html) will be faster.

## Commands for Development

1. Execute `polynomial.py` continuously with [nodemon](https://www.npmjs.com/package/nodemon): `nodemon polynomial.py`

2. Run the tests with [pytest](https://pypi.org/project/pytest/): `pytest`

3. Run the tests continuously using [pytest-watch](https://pypi.org/project/pytest-watch/): `pwt`

4. Generate a test coverage report with [pytest-cov](https://pypi.org/project/pytest-cov/): `pytest --cov --cov-report term-missing` or `pytest --cov --cov-report html`

5. Type checking with [mypy](https://pypi.org/project/mypy/): `mypy polynomial.py`

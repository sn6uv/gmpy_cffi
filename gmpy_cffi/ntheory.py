import sys

from gmpy_cffi.interface import gmp
from gmpy_cffi.mpz import mpz, _new_mpz


PY3 = sys.version.startswith('3')


if PY3:
    long = int
    xrange = range


def _check_mpz(function_name, value_name, value):
    if isinstance(value, mpz):
        return value
    if isinstance(value, (int, long)):
        return mpz(value)
    else:
        raise TypeError('%s() expected integer %s got %s' % (
            function_name, value_name, type(value)))


def _check_int(function_name, value_name, value):
    if isinstance(value, mpz):
        value = int(value)
    if not (isinstance(value, (int, long)) and
            -sys.maxsize - 1 <= value <= sys.maxsize):
        raise TypeError('%s() expected integer %s got %s' % (
            function_name, value_name, type(value)))
    return value


def is_prime(x, n=25):
    """
    is_prime(x[, n=25]) -> bool

    Return True if x is _probably_ prime, else False if x is
    definately composite. x is checked for small divisors and up
    to n Miller-Rabin tests are performed.
    """
    x = _check_mpz('is_prime', 'x', x)
    n = _check_int('is_prime', 'n', n)
    if n <= 0:
        raise ValueError("is_prime repitition count must be positive")
    return gmp.mpz_probab_prime_p(x._mpz, n) != 0


def next_prime(x):
    """
    next_prime(x) -> mpz

    Return the next _probable_ prime number > x.
    """
    x = _check_mpz('next_prime', 'x', x)
    res = _new_mpz()
    gmp.mpz_nextprime(res, x._mpz)
    return mpz._from_c_mpz(res)


def gcd(a, b):
    """
    gcd(a, b) -> mpz

    Return the greatest common denominator of integers a and b.
    """
    a = _check_mpz('gcd', 'a', a)
    b = _check_mpz('gcd', 'b', b)
    res = _new_mpz()
    gmp.mpz_gcd(res, a._mpz, b._mpz)
    return mpz._from_c_mpz(res)


def gcdext(a, b):
    """
    gcdext(a, b) - > tuple

    Return a 3-element tuple (g,s,t) such that
        g == gcd(a,b) and g == a*s + b*t
    """
    a = _check_mpz('gcdext', 'a', a)
    b = _check_mpz('gcdext', 'b', b)
    mpz_g, mpz_s, mpz_t = _new_mpz(), _new_mpz(), _new_mpz()
    gmp.mpz_gcdext(mpz_g, mpz_s, mpz_t, a._mpz, b._mpz)
    return (mpz._from_c_mpz(mpz_g),
            mpz._from_c_mpz(mpz_s),
            mpz._from_c_mpz(mpz_t))


def lcm(a, b):
    """
    lcm(a, b) -> mpz

    Return the lowest common multiple of integers a and b.
    """
    a = _check_mpz('lcm', 'a', a)
    b = _check_mpz('lcm', 'b', b)
    res = _new_mpz()
    gmp.mpz_lcm(res, a._mpz, b._mpz)
    return mpz._from_c_mpz(res)


def invert(x, m):
    """
    invert(x, m) -> mpz

    Return y such that x*y == 1 (mod m). Raises ZeroDivisionError if no
    inverse exists.
    """
    x = _check_mpz('invert', 'x', x)
    m = _check_mpz('invert', 'm', m)
    res = _new_mpz()
    if gmp.mpz_invert(res, x._mpz, m._mpz) == 0:
        raise ZeroDivisionError
    return mpz._from_c_mpz(res)


def jacobi(x, y):
    """
    jacobi(x, y) -> mpz

    Return the Jacobi symbol (x|y). y must be odd and >0.
    """
    x = _check_mpz('jacobi', 'x', x)
    y = _check_mpz('jacobi', 'y', y)
    if y <= 0 or not (y % 2):
        raise ValueError('jacobi() expected y to be positive and odd')
    return gmp.mpz_legendre(x._mpz, y._mpz)


def legendre(x, y):
    """
    legendre(x, y) -> mpz

    Return the Legendre symbol (x|y). y is assumed to be an odd prime.
    """
    x = _check_mpz('legendre', 'x', x)
    y = _check_mpz('legendre', 'y', y)
    if y <= 0 or not (y % 2):
        raise ValueError('legendre() expected y to be positive and odd')
    return gmp.mpz_legendre(x._mpz, y._mpz)


def kronecker(x, y):
    """
    kronecker(x, y) -> mpz

    Return the Kronecker-Jacobi symbol (x|y)
    """
    x = _check_mpz('kronecker', 'x', x)
    y = _check_mpz('kronecker', 'y', y)
    return gmp.mpz_kronecker(x._mpz, y._mpz)


def fac(n):
    """
    fac(n) -> mpz

    Return the exact factorial of n.

    See factorial(n) to get the floating-point approximation.
    """
    n = _check_int('fac', 'n', n)
    if n < 0:
        raise ValueError('fac() of negative number')
    res = _new_mpz()
    gmp.mpz_fac_ui(res, n)
    return mpz._from_c_mpz(res)


def bincoef(x, n):
    """
    bincoef(x, n) -> mpz

    Return the binomial coefficient ('x over n'). n >= 0.
    """
    n = _check_int('bincoef', 'n', n)
    if n < 0:
        raise ValueError('binomial coefficient with negative k')
    res = _new_mpz()
    if isinstance(x, mpz):
        gmp.mpz_bin_ui(res, x._mpz, n)
    elif isinstance(x, (int, long)) and -sys.maxsize - 1 <= x <= sys.maxsize:
        gmp.mpz_bin_uiui(res, x, n)
    else:
        raise TypeError
    return mpz._from_c_mpz(res)


def fib(n):
    """
    fib(n) -> mpz

    Return the n-th Fibonacci number.
    """
    n = _check_int('fib', 'n', n)
    if n < 0:
        raise ValueError('Fibonacci of negative number')
    res = _new_mpz()
    gmp.mpz_fib_ui(res, n)
    return mpz._from_c_mpz(res)


def fib2(n):
    """
    fib2(n) -> tuple

    Return a 2-tuple with the (n-1)-th and n-th Fibonacci numbers.
    """
    n = _check_int('fib2', 'n', n)
    if n < 0:
        raise ValueError('Fibonacci of negative number')
    res, res1 = _new_mpz(), _new_mpz()
    gmp.mpz_fib2_ui(res, res1, n)
    return (mpz._from_c_mpz(res), mpz._from_c_mpz(res1))


def lucas(n):
    """
    lucas(n) -> mpz

    Return the n-th Lucas number.
    """
    n = _check_int('lucas', 'n', n)
    if n < 0:
        raise ValueError('Lucas of negative number')
    res = _new_mpz()
    gmp.mpz_lucnum_ui(res, n)
    return mpz._from_c_mpz(res)


def lucas2(n):
    """
    lucas2(n) -> tuple

    Return a 2-tuple with the (n-1)-th and n-th Lucas numbers.
    """
    n = _check_int('lucas2', 'n', n)
    if n < 0:
        raise ValueError('Lucas of negative number')
    res, res1 = _new_mpz(), _new_mpz()
    gmp.mpz_lucnum2_ui(res, res1, n)
    return (mpz._from_c_mpz(res), mpz._from_c_mpz(res1))

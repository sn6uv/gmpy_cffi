import sys

from gmpy_cffi.interface import gmp
from gmpy_cffi.mpz import mpz, _new_mpz


PY3 = sys.version_info >= (3, 0)


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


def is_prime(x, n=25):
    """
    is_prime(x[, n=25]) -> bool

    Return True if x is _probably_ prime, else False if x is
    definately composite. x is checked for small divisors and up
    to n Miller-Rabin tests are performed.
    """
    x = _check_mpz('is_prime', 'x', x)
    if not (isinstance(n, int) and n <= sys.maxsize):
        raise TypeError('is_prime() expected integer n got %s' % type(n))
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
    return (mpz._from_c_mpz(mpz_g), mpz._from_c_mpz(mpz_s), mpz._from_c_mpz(mpz_t))


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

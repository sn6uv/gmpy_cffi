import sys

from gmpy_cffi.interface import gmp
from gmpy_cffi.mpz import mpz, _new_mpz


PY3 = sys.version_info >= (3, 0)


if PY3:
    long = int
    xrange = range



def is_prime(x, n=25):
    """
    is_prime(x[, n=25]) -> bool

    Return True if x is _probably_ prime, else False if x is
    definately composite. x is checked for small divisors and up
    to n Miller-Rabin tests are performed.
    """

    if isinstance(x, mpz):
        pass
    elif isinstance(x, (int, long)):
        x = mpz(x)
    else:
        raise TypeError('is_prime() expected integer x got %s' % type(x))

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

    if isinstance(x, mpz):
        pass
    elif isinstance(x, (int, long)):
        x = mpz(x)
    else:
        raise TypeError('next_prime() expected integer x got %s' % type(x))

    res = _new_mpz()
    gmp.mpz_nextprime(res, x._mpz)
    return mpz._from_c_mpz(res)


def gcd(a, b):
    """
    gcd(a, b) -> mpz

    Return the greatest common denominator of integers a and b.
    """

    if isinstance(a, mpz):
        pass
    elif isinstance(a, (int, long)):
        a = mpz(a)
    else:
        raise TypeError('gcd() expected integer a got %s' % type(a))

    if isinstance(b, mpz):
        pass
    elif isinstance(b, (int, long)):
        b = mpz(b)
    else:
        raise TypeError('gcd() expected integer b got %s' % type(b))

    res = _new_mpz()
    gmp.mpz_gcd(res, a._mpz, b._mpz)
    return mpz._from_c_mpz(res)

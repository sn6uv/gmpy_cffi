import sys

from gmpy_cffi.interface import gmp
from gmpy_cffi.mpz import mpz, _new_mpz


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

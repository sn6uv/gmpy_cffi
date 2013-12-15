import sys

from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.mpz import mpz, _new_mpz, _del_mpz
from gmpy_cffi.mpfr import mpfr, _new_mpfr, _del_mpfr
from gmpy_cffi.mpc import mpc, _new_mpc, _del_mpc
from gmpy_cffi.convert import _pyint_to_mpz


if sys.version > '3':
    long = int
    xrange = range


def _new_randstate():
    state = ffi.new('gmp_randstate_t')
    gmp.gmp_randinit_default(state)
    return state


def _del_randstate(state):
    pass


class RandomState(object):
    def __init__(self):
        self._state = ffi.gc(_new_randstate(), _del_randstate)

    def __repr__(self):
        return '<gmpy_cffi.RandomState>'


def random_state(*args):
    """
    random_state([seed]) -> object

    Return new object containing state information for the random number
    generator. An optional integer can be specified as the seed value.
    """
    if len(args) == 0:
        result = RandomState()
        gmp.gmp_randseed_ui(result._state, 0)
    elif len(args) == 1 and isinstance(args[0], (int, long)):
        result = RandomState()
        temp_mpz = _new_mpz()
        _pyint_to_mpz(args[0], temp_mpz)
        gmp.gmp_randseed(result._state, temp_mpz)
        _del_mpz(temp_mpz)
    elif len(args) == 1 and isinstance(args[0], mpz):
        result = RandomState()
        gmp.gmp_randseed(result._state, args[0]._mpz)
    else:
        raise TypeError("random_state requires one or zero integer arguments")
    return result


def mpz_random(random_state, n):
    """
    mpz_random(random_state, n) -> mpz

    Return a uniformly distributed random integer between 0 and n-1.
    """
    if not isinstance(random_state, RandomState):
        raise TypeError("Expected RandomState in position 1 (got %s)" % type(
            random_state))
    res = _new_mpz()
    if isinstance(n, mpz):
        gmp.mpz_urandomm(res, random_state._state, n._mpz)
    elif isinstance(n, (int, long)):
        tmp_mpz = _new_mpz()
        _pyint_to_mpz(n, tmp_mpz)
        gmp.mpz_urandomm(res, random_state._state, tmp_mpz)
        _del_mpz(tmp_mpz)
    else:
        raise TypeError("Expected integer in position 1 (got %s)" % type(n))
    return mpz._from_c_mpz(res)


def mpfr_random(random_state):
    """
    mpfr_random(random_state) -> mpfr

    Return a uniformly distributed number in the interval [0,1].
    """
    if not isinstance(random_state, RandomState):
        raise TypeError("Expected RandomState in position 1 (got %s)" % type(
            random_state))
    res = _new_mpfr()
    gmp.mpfr_urandom(res, random_state._state, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def mpc_random(random_state):
    """
    mpc_random(random_state) -> mpc

    Return a uniformly distributed number in the unit square [0,1]x[0,1].
    """
    if not isinstance(random_state, RandomState):
        raise TypeError("Expected RandomState in position 1 (got %s)" % type(
            random_state))
    res = _new_mpc()
    gmp.mpc_urandom(res, random_state._state)
    return mpc._from_c_mpc(res)


def mpfr_grandom(random_state):
    """
    mpfr_grandom(random_state) -> (mpfr, mpfr)

    Return two random numbers with gaussian distribution.
    """
    if not isinstance(random_state, RandomState):
        raise TypeError("Expected RandomState in position 1 (got %s)" % type(
            random_state))
    res1, res2 = _new_mpfr(), _new_mpfr()
    gmp.mpfr_grandom(res1, res2, random_state._state, gmp.MPFR_RNDN)
    return (mpfr._from_c_mpfr(res1), mpfr._from_c_mpfr(res2))

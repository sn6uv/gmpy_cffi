import sys
import array
from math import log10

from gmpy_cffi.interface import gmp, ffi


MAX_UI = 2 * sys.maxsize + 1
PY3 = sys.version.startswith('3')


if PY3:
    long = int
    xrange = range


def _pyint_to_mpz(n, a):
    """
    Set `a` from `n`.
    :type n: int,long
    :type a: mpz_t
    """

    if -sys.maxsize - 1 <= n <= sys.maxsize:
        gmp.mpz_set_si(a, n)
    elif sys.maxsize < n <= MAX_UI:
        gmp.mpz_set_ui(a, n)
    else:
        gmp.mpz_set_str(a, hex(n).rstrip('L').encode('UTF-8'), 0)


def _pylong_to_mpz(n, a):
    """
    Set `a` from `n`.

    :type n: long
    :type a: mpz_t
    """
    gmp.mpz_set_str(a, hex(n).rstrip('L').encode('UTF-8'), 0)


def _mpz_to_pylong(a):
    """
    Convert a to a python long.

    :type a: mpz_t
    :rtype: long
    """

    size = ffi.sizeof('uint64_t')
    numb = 8 * size
    count = (gmp.mpz_sizeinbase(a, 2) + numb - 1) // numb
    p = ffi.new('uint64_t[]', count)
    gmp.mpz_export(p, ffi.NULL, 1, size, 0, 0, a)
    res = 0
    for n in p:
        res = (res << numb) + n

    return res * gmp.mpz_sgn(a)


def _mpz_to_str(a, base):
    """
    Return string representation of a in base base.

    :type a: mpz_t
    :param base: 2..62
    :type base: int
    :rtype: str
    """

    l = gmp.mpz_sizeinbase(a, base) + 2
    p = ffi.new('char[]', l)
    gmp.mpz_get_str(p, base, a)
    if PY3:
        return ffi.string(p).decode('UTF-8')
    else:
        return ffi.string(p)


def _pyint_to_mpq(n, a):
    if -sys.maxsize - 1 <= n <= sys.maxsize:
        gmp.mpq_set_si(a, n, 1)
    elif sys.maxsize < n <= MAX_UI:
        gmp.mpq_set_ui(a, n, 1)
    else:
        assert isinstance(n, long)
        num, den = gmp.mpq_numref(a), gmp.mpq_denref(a)
        _pylong_to_mpz(n, num)
        gmp.mpz_set_ui(den, 1)


def _mpq_to_str(a, base):
    l = (gmp.mpz_sizeinbase(gmp.mpq_numref(a), base) +
         gmp.mpz_sizeinbase(gmp.mpq_denref(a), base) + 3)
    p = ffi.new('char[]', l)
    gmp.mpq_get_str(p, base, a)
    if PY3:
        return ffi.string(p).decode('UTF-8')
    else:
        return ffi.string(p)


def _str_to_mpq(s, base, a):
    if isinstance(base, (int, long)):
        if base == 0 or 2 <= base <= 62:
            if gmp.mpq_set_str(a, s.encode('UTF-8'), base) == -1:
                raise ValueError("Can't create mpq from %s with base %s" % (s, base))
        else:
            raise ValueError('base must be 0 or 2..62, not %s' % base)
    else:
        raise TypeError('an integer is required')


def _pyint_to_mpfr(n, a):
    if -sys.maxsize - 1 <= n <= sys.maxsize:
        gmp.mpfr_set_si(a, n, gmp.MPFR_RNDN)
    elif sys.maxsize < n <= MAX_UI:
        gmp.mpfr_set_ui(a, n, gmp.MPFR_RNDN)
    else:
        assert isinstance(n, long)
        tmp_mpz = ffi.new('mpz_t')
        gmp.mpz_init(tmp_mpz)
        _pylong_to_mpz(n, tmp_mpz)
        gmp.mpfr_set_z(a, tmp_mpz, gmp.MPFR_RNDN)
        gmp.mpz_clear(tmp_mpz)


def _mpfr_to_str(a):
    precision = int(log10(2) * gmp.mpfr_get_prec(a) + 2)
    buf = ffi.new('char []', precision + 10)
    fmtstr = "%.{0}Rg".format(precision)
    buflen = gmp.mpfr_sprintf(buf, fmtstr.encode('UTF-8'), a)
    if PY3:
        pybuf = ffi.string(buf).decode('UTF-8')
    else:
        pybuf = ffi.string(buf)
    if gmp.mpfr_number_p(a) and '.' not in pybuf:
        pybuf = pybuf + '.0'
    return pybuf


def _str_to_mpfr(s, base, a):
    if isinstance(base, (int, long)):
        if base == 0 or 2 <= base <= 62:
            if gmp.mpfr_set_str(a, s.encode('UTF-8'), base, gmp.MPFR_RNDN) == -1:
                raise ValueError(
                    "Can't create mpfr from %s with base %s" % (s, base))
        else:
            raise ValueError('base must be 0 or 2..62, not %s' % base)
    else:
        raise TypeError('an integer is required')


def _mpc_to_str(a, base):
    real_str = _mpfr_to_str(gmp.mpc_realref(a))
    imag_str = _mpfr_to_str(gmp.mpc_imagref(a))
    if imag_str.startswith('-'):
        return real_str + imag_str + 'j'
    else:
        return real_str + '+' + imag_str + 'j'


def _str_to_mpc(s, base, a):
    # Strip trailing 'j'
    if s.endswith('j'):
        s = s[:-1]

    # Space required between real and imag parts
    s = s.replace('+', ' +').replace('-', ' -').replace('e +', 'e+').replace('e -', 'e-')
    if s.find(' +', 1) == -1 and s.find(' -', 1) == -1:
        s = s + ' +0.0'

    # Wrap string in brackets
    s = '(' + s + ')'

    if 2 <= base <= 36:
        if gmp.mpc_set_str(a, s.encode('UTF-8'), base, gmp.MPC_RNDNN) == -1:
            raise ValueError("invalid string in mpc()")
    else:
        raise ValueError(
            "base for mpc() must be in the interval 2 ... 36.")

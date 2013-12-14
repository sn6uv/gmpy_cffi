import sys

from gmpy_cffi.interface import gmp, ffi
from gmpy_cffi.mpz import mpz
from gmpy_cffi.mpq import mpq
from gmpy_cffi.mpfr import mpfr, _new_mpfr
from gmpy_cffi.mpc import mpc, _new_mpc
from gmpy_cffi.convert import _pyint_to_mpfr, MAX_UI


if sys.version > '3':
    long = int
    xrange = range


def _init_check_mpfr(x):
    """
    Returns a new mpfr and a pointer to a c mpfr storing the value of x
    """
    if isinstance(x, mpfr):
        res = _new_mpfr(gmp.mpfr_get_prec(x._mpfr))
        mpfr_x = x._mpfr
    elif isinstance(x, float):
        res = _new_mpfr()
        mpfr_x = res        # avoid initialising another c mpfr
        gmp.mpfr_set_d(mpfr_x, x, gmp.MPFR_RNDN)
    elif isinstance(x, (int, long)):
        res = _new_mpfr()
        mpfr_x = res        # avoid initialising another c mpfr
        _pyint_to_mpfr(x, mpfr_x)
    elif isinstance(x, mpz):
        res = _new_mpfr()
        mpfr_x = res        # avoid initialising another c mpfr
        gmp.mpfr_set_z(mpfr_x, x._mpz, gmp.MPFR_RNDN)
    elif isinstance(x, mpq):
        res = _new_mpfr()
        mpfr_x = res        # avoid initialising another c mpfr
        gmp.mpfr_set_q(mpfr_x, x._mpq, gmp.MPFR_RNDN)
    else:
        raise TypeError
    return res, mpfr_x


def _init_check_mpc(x):
    """
    Returns a new mpc and a pointer to a c mpc storing the value of x
    """
    if isinstance(x, mpc):
        res = _new_mpc()
        mpc_x = x._mpc
    elif isinstance(x, complex):
        res = _new_mpc()
        mpc_x = res        # avoid initialising another c mpc
        gmp.mpc_set_d_d(mpc_x, x.real, x.imag, gmp.MPC_RNDNN)
    elif isinstance(x, mpfr):
        res = _new_mpc()
        mpc_x = res        # avoid initialising another c mpc
        gmp.mpc_set_fr(mpc_x, x, gmp.MPC_RNDNN)
    elif isinstance(x, float):
        res = _new_mpc()
        gmp.mpc_set_d(mpc_x, x, gmp.MPC_RNDNN)
    elif isinstance(x, (int, long)):
        res = _new_mpc()
        mpc_x = res        # avoid initialising another c mpc
        _pyint_to_mpfr(x, gmp.mpc_realref(mpc_x))
        gmp.mpfr_set_ui(gmp.mpc_imagref(mpc_x), 0, gmp.MPC_RNDNN)
    elif isinstance(x, mpz):
        res = _new_mpc()
        mpc_x = res        # avoid initialising another c mpc
        gmp.mpc_set_z(mpc_x, x._mpz, gmp.MPC_RNDNN)
    elif isinstance(x, mpq):
        res = _new_mpc()
        mpc_x = res        # avoid initialising another c mpc
        gmp.mpc_set_q(mpc_x, x._mpq, gmp.MPC_RNDNN)
    else:
        raise TypeError
    return res, mpc_x


def log(x):
    """
    log(x) -> number

    Return the natural logarithm of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_log(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_log(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def log2(x):
    """
    log2(x) -> number

    Return the base-2 logarithm of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_log2(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def log10(x):
    """
    log10(x) -> number

    Return the base-10 logarithm of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_log10(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)
    # except TypeError:
    #     res, x = _init_check_mpc(x)
    #     gmp.mpc_log10(res, x, gmp.MPC_RNDNN)
    #     return mpc._from_c_mpc(res)


def exp(x):
    """
    exp(x) -> number

    Return the exponential of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_exp(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_exp(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def exp2(x):
    """
    exp2(x) -> number

    Return 2**x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_exp2(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def exp10(x):
    """
    exp10(x) -> number

    Return 10**x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_exp10(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def cos(x):
    """
    cos(x) -> number

    Return the cosine of x; x in radians.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_cos(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_cos(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def sin(x):
    """
    sin(x) -> number

    Return the sine of x; x in radians.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_sin(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_sin(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def tan(x):
    """
    tan(x) -> number

    Return the tangent of x; x in radians.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_tan(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_tan(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def sin_cos(x):
    """
    sin_cos(x) -> (number, number)

    Return a tuple containing the sine and cosine of x; x in radians.
    """
    if isinstance(x, mpfr):
        res1 = _new_mpfr(gmp.mpfr_get_prec(x._mpfr))
        res2 = _new_mpfr(gmp.mpfr_get_prec(x._mpfr))
        mpfr_x = x._mpfr
    elif isinstance(x, float):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
    elif isinstance(x, (int, long)):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        _pyint_to_mpfr(x, mpfr_x)
    elif isinstance(x, mpz):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        gmp.mpfr_set_z(mpfr_x, x._mpz, gmp.MPFR_RNDN)
    elif isinstance(x, mpq):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        gmp.mpfr_set_q(mpfr_x, x._mpq, gmp.MPFR_RNDN)
    else:
        if isinstance(x, mpc):
            res1 = _new_mpc()
            res2 = _new_mpc()
            mpc_x = x._mpc
        elif isinstance(x, complex):
            res1 = _new_mpc()
            res2 = _new_mpc()
            mpc_x = res1
            gmp.mpc_set_d_d(mpc_x, x.real, x.imag, gmp.MPC_RNDNN)
        else:
            raise TypeError
        gmp.mpc_sin_cos(res1, res2, mpc_x, gmp.MPC_RNDNN, gmp.MPC_RNDNN)
        return (mpc._from_c_mpc(res1), mpc._from_c_mpc(res2))
    gmp.mpfr_sin_cos(res1, res2, mpfr_x, gmp.MPFR_RNDN)
    return (mpfr._from_c_mpfr(res1), mpfr._from_c_mpfr(res2))


def sec(x):
    """
    sec(x) -> number

    Return the secant of x; x in radians.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_sec(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def csc(x):
    """
    csc(x) -> number

    Return the cosecant of x; x in radians.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_csc(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def cot(x):
    """
    cot(x) -> number

    Return the cotangent of x; x in radians.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_cot(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def acos(x):
    """
    acos(x) -> number

    Return the arc-cosine of x; x in radians.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_acos(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_acos(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def asin(x):
    """
    asin(x) -> number

    Return the arc-sine of x; x in radians.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_asin(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_asin(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def atan(x):
    """
    atan(x) -> number

    Return the arc-tangent of x; x in radians.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_atan(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_atan(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def atan2(y, x):
    """
    atan2(y, x) -> number

    Return the arc-tangent of (y/x).
    """
    # X
    if isinstance(x, mpfr):
        mpfr_x = x._mpfr
    elif isinstance(x, float):
        mpfr_x = _new_mpfr()
        gmp.mpfr_set_d(mpfr_x, x, gmp.MPFR_RNDN)
    elif isinstance(x, (int, long)):
        mpfr_x = _new_mpfr()
        _pyint_to_mpfr(x, mpfr_x)
    elif isinstance(x, mpz):
        mpfr_x = _new_mpfr()
        gmp.mpfr_set_z(mpfr_x, x._mpz, gmp.MPFR_RNDN)
    elif isinstance(x, mpq):
        mpfr_x = _new_mpfr()
        gmp.mpfr_set_q(mpfr_x, x._mpq, gmp.MPFR_RNDN)
    else:
        raise TypeError

    # Y
    if isinstance(y, mpfr):
        mpfr_y = y._mpfr
    elif isinstance(y, float):
        mpfr_y = _new_mpfr()
        gmp.mpfr_set_d(mpfr_y, y, gmp.MPFR_RNDN)
    elif isinstance(y, (int, long)):
        mpfr_y = _new_mpfr()
        _pyint_to_mpfr(y, mpfr_y)
    elif isinstance(y, mpz):
        mpfr_y = _new_mpfr()
        gmp.mpfr_set_z(mpfr_y, y._mpz, gmp.MPFR_RNDN)
    elif isinstance(y, mpq):
        mpfr_y = _new_mpfr()
        gmp.mpfr_set_q(mpfr_y, y._mpq, gmp.MPFR_RNDN)
    else:
        raise TypeError

    res = _new_mpfr(min(gmp.mpfr_get_prec(mpfr_x), gmp.mpfr_get_prec(mpfr_x)))
    gmp.mpfr_atan2(res, mpfr_y, mpfr_x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def cosh(x):
    """
    cosh(x) -> number

    Return the hyperbolic cosine of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_cosh(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_cosh(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def sinh(x):
    """
    sinh(x) -> number

    Return the hyperbolic sine of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_sinh(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_sinh(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def tanh(x):
    """
    tanh(x) -> number

    Return the hyperbolic tangent of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_tanh(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_tanh(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def sinh_cosh(x):
    """
    sinh_cosh(x) -> (number, number)

    Return a tuple containing the hyperbolic sine and cosine of x.
    """
    if isinstance(x, mpfr):
        res1 = _new_mpfr(gmp.mpfr_get_prec(x._mpfr))
        res2 = _new_mpfr(gmp.mpfr_get_prec(x._mpfr))
        mpfr_x = x._mpfr
    elif isinstance(x, float):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        gmp.mpfr_set_d(mpfr_x, x, gmp.MPFR_RNDN)
    elif isinstance(x, (int, long)):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        _pyint_to_mpfr(x, mpfr_x)
    elif isinstance(x, mpz):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        gmp.mpfr_set_z(mpfr_x, x._mpz, gmp.MPFR_RNDN)
    elif isinstance(x, mpq):
        res1 = _new_mpfr()
        res2 = _new_mpfr()
        mpfr_x = res1
        gmp.mpfr_set_q(mpfr_x, x._mpq, gmp.MPFR_RNDN)
    else:
        raise TypeError
    gmp.mpfr_sinh_cosh(res1, res2, mpfr_x, gmp.MPFR_RNDN)
    return (mpfr._from_c_mpfr(res1), mpfr._from_c_mpfr(res2))


def sech(x):
    """
    sech(x) -> number

    Return the hyperbolic secant of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_sech(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def csch(x):
    """
    csch(x) -> number

    Return the hyperbolic cosecant of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_csch(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def coth(x):
    """
    coth(x) -> number

    Return the hyperbolic cotangent of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_coth(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def acosh(x):
    """
    acosh(x) -> number

    Return the inverse hyperbolic cosine of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_acosh(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_acosh(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def asinh(x):
    """
    asinh(x) -> number

    Return the inverse hyperbolic sine of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_asinh(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_asinh(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def atanh(x):
    """
    atanh(x) -> number

    Return the inverse hyperbolic tangent of x.
    """
    try:
        res, x = _init_check_mpfr(x)
        gmp.mpfr_atanh(res, x, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        res, x = _init_check_mpc(x)
        gmp.mpc_atanh(res, x, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def factorial(n):
    """
    factorial(n) -> number

    Return the floating-point approximation to the factorial of n.

    See fac(n) to get the exact integer result.
    """
    if isinstance(n, (int, long)):
        if 0 <= n <= MAX_UI:
            res = _new_mpfr()
            gmp.mpfr_fac_ui(res, n, gmp.MPFR_RNDN)
            return mpfr._from_c_mpfr(res)
        elif n < 0:
            raise ValueError("factorial() of negative number")
    raise TypeError("factorial() requires 'int' argument")


def log1p(x):
    """
    log1p(x) -> number

    Return the logarithm of (1+x).
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_log1p(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def expm1(x):
    """
    expm1(x) -> number

    Return exponential(x) - 1.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_expm1(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def eint(x):
    """
    eint(x) -> number

    Return the exponential integral of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_eint(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def li2(x):
    """
    li2(x) -> number

    Return the real part of dilogarithm of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_li2(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def gamma(x):
    """
    gamma(x) -> number

    Return gamma of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_gamma(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def lngamma(x):
    """
    lngamma(x) -> number

    Return logarithm of gamma(x).
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_lngamma(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def lgamma(x):
    """
    lgamma(x) -> (number, int)

    Return a tuple containing the logarithm of the absolute value of
    gamma(x) and the sign of gamma(x)
    """
    res, x = _init_check_mpfr(x)
    sgn = ffi.new('int *')
    gmp.mpfr_lgamma(res, sgn, x, gmp.MPFR_RNDN)
    return (mpfr._from_c_mpfr(res), int(sgn[0]))


def digamma(x):
    """
    digamma(x) -> number

    Return digamma of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_digamma(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def zeta(x):
    """
    zeta(x) -> number

    Return Riemann zeta of x.
    """
    # if isinstance(x, (int, long)) and 0 <= x <= MAX_UI:
    #     res = _new_mpfr()
    #     gmp.mpfr_zeta_ui(res, x, gmp.MPFR_RNDN)
    res, x = _init_check_mpfr(x)
    gmp.mpfr_zeta(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def erf(x):
    """
    zeta(x) -> number

    Return error function of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_erf(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def erfc(x):
    """
    zeta(x) -> number

    Return complementary error function of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_erfc(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def j0(x):
    """
    j0(x) -> number

    Return the first kind Bessel function of order 0 of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_j0(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def j1(x):
    """
    j1(x) -> number

    Return the first kind Bessel function of order 1 of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_j1(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def jn(x, n):
    """
    jn(x, n) -> number

    Return the first kind Bessel function of order n of x.
    """
    if not (isinstance(n, (int, long)) and -sys.maxsize-1 <= n <= sys.maxsize):
        raise TypeError("yn() requires 'mpfr', 'int' arguments")
    res, x = _init_check_mpfr(x)
    gmp.mpfr_jn(res, n, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def y0(x):
    """
    y0(x) -> number

    Return the second kind Bessel function of order 0 of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_y0(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def y1(x):
    """
    y1(x) -> number

    Return the second kind Bessel function of order 1 of x.
    """
    res, x = _init_check_mpfr(x)
    gmp.mpfr_y1(res, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def yn(x, n):
    """
    yn(x, n) -> number

    Return the second kind Bessel function of order n of x.
    """
    if not (isinstance(n, (int, long)) and -sys.maxsize-1 <= n <= sys.maxsize):
        raise TypeError("yn() requires 'mpfr', 'int' arguments")
    res, x = _init_check_mpfr(x)
    gmp.mpfr_yn(res, n, x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def fma(x, y, z):
    """
    fma(x, y, z) -> number

    Return the correctly rounded result of (x * y) + z.
    """
    try:
        # XXX Optimise
        res, mpfr_x = _init_check_mpfr(x)
        res, mpfr_y = _init_check_mpfr(y)
        res, mpfr_z = _init_check_mpfr(z)
        gmp.mpfr_fma(res, mpfr_x, mpfr_y, mpfr_z, gmp.MPFR_RNDN)
        return mpfr._from_c_mpfr(res)
    except TypeError:
        # XXX Optimise
        res, mpc_x = _init_check_mpc(x)
        res, mpc_y = _init_check_mpc(y)
        res, mpc_z = _init_check_mpc(z)
        gmp.mpc_fma(res, mpc_x, mpc_y, mpc_z, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)


def fms(x, y, z):
    """
    fms(x, y, z) -> number

    Return the correctly rounded result of (x * y) - z.
    """
    # XXX Optimise
    res, mpfr_x = _init_check_mpfr(x)
    res, mpfr_y = _init_check_mpfr(y)
    res, mpfr_z = _init_check_mpfr(z)
    gmp.mpfr_fms(res, mpfr_x, mpfr_y, mpfr_z, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def agm(x, y):
    """
    agm(x, y) -> number

    Return the arithmetic-geometric mean of x and y.
    """
    # XXX Optimise
    res, mpfr_x = _init_check_mpfr(x)
    res, mpfr_y = _init_check_mpfr(y)
    gmp.mpfr_agm(res, mpfr_x, mpfr_y, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def hypot(x, y):
    """
    hypot(y, x) -> number

    Return the square root of (x**2 + y**2).
    """
    # XXX Optimise
    res, mpfr_x = _init_check_mpfr(x)
    res, mpfr_y = _init_check_mpfr(y)
    gmp.mpfr_hypot(res, mpfr_x, mpfr_y, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def ai(x):
    """
    ai(x) -> number

    Return the Airy function of x.
    """
    res, mpfr_x = _init_check_mpfr(x)
    gmp.mpfr_ai(res, mpfr_x, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def const_log2(precision=0):
    """
    const_log2([precision=0]) -> mpfr

    Return the log2 constant  using the specified precision. If no
    precision is specified, the default precision is used.
    """
    res = _new_mpfr(precision)
    gmp.mpfr_const_log2(res, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def const_pi(precision=0):
    """
    const_pi([precision=0]) -> mpfr

    Return the constant pi using the specified precision. If no
    precision is specified, the default precision is used.
    """
    res = _new_mpfr(precision)
    gmp.mpfr_const_pi(res, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def const_euler(precision=0):
    """
    const_euler([precision=0]) -> mpfr

    Return the euler constant using the specified precision. If no
    precision is specified, the default precision is used.
    """
    res = _new_mpfr(precision)
    gmp.mpfr_const_euler(res, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)


def const_catalan(precision=0):
    """
    const_catalan([precision=0]) -> mpfr

    Return the catalan constant  using the specified precision. If no
    precision is specified, the default precision is used.
    """
    res = _new_mpfr(precision)
    gmp.mpfr_const_catalan(res, gmp.MPFR_RNDN)
    return mpfr._from_c_mpfr(res)

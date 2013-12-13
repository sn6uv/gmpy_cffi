from gmpy_cffi.interface import ffi, gmp

__version__ = '0.0.1'


def version():
    """
    version() -> string

    Return string giving current GMPY2 version.
    """
    return __version__


def mp_version():
    """
    mp_version() -> string

    Return string giving the name and version of the multiple precision
    library used.
    """
    return "GMP {0}".format(ffi.string(gmp.gmp_version))


def mpfr_version():
    """
    mpfr_version() -> string

    Return string giving current MPFR version. Return None if MPFR
    support is not available.
    """
    return "MPFR {0}".format(ffi.string(gmp.mpfr_get_version()))


def mpc_version():
    """
    mpc_version() -> string

    Return string giving current MPC version. Return None if MPC
    support is not available.
    """
    return "MPC {0}".format(ffi.string(gmp.mpc_get_version()))

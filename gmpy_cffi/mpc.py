import sys

from gmpy_cffi.interface import ffi, gmp
from gmpy_cffi.convert import _str_to_mpc, _mpc_to_str, _pyint_to_mpfr, _pyint_to_mpz, MAX_UI
from gmpy_cffi.mpz import mpz
from gmpy_cffi.mpq import mpq
from gmpy_cffi.mpfr import mpfr
from gmpy_cffi.cache import _new_mpc, _del_mpc, _new_mpfr, _new_mpz, _del_mpz


if sys.version > '3':
    long = int
    xrange = range


def _check_prec(prec):
    if isinstance(prec, (int, long)):
        return (prec, prec)
    elif (isinstance(prec, tuple) and len(prec) == 2 and
          all(isinstance(p, (int, long)) for p in prec)):
        return prec
    raise ValueError("invalid value for precision")


class mpc(object):
    """
    """
    def __init__(self, *args):
        nargs = len(args)
        # if nargs == 1 and isinstance(args[0], self.__class__):
        #     self._mpc = args[0]._mpc
        #     return

        if nargs == 0:
            self._mpc = ffi.gc(_new_mpc(), _del_mpc)
            gmp.mpc_set_ui(self._mpc, 0, gmp.MPC_RNDNN)
        elif isinstance(args[0], str):   # unicode?
            # First argument is a string
            if nargs == 1:
                prec, base = 0, 10
            elif nargs == 2:
                prec, base = args[1], 10
            elif nargs == 3:
                prec, base = args[1], args[2]
            else:
                raise TypeError("function takes at most 3 arguments (4 given)")

            prec = _check_prec(prec)

            self._mpc = ffi.gc(_new_mpc(prec), _del_mpc)
            _str_to_mpc(args[0], base, self._mpc)
        elif isinstance(args[0], (mpc, complex)):
            # First argument is complex
            if nargs == 1:
                prec = (0,  0)
            elif nargs == 2:
                prec = _check_prec(args[1])
            else:
                raise TypeError("function takes at most 2 arguments (3 given)")

            self._mpc = ffi.gc(_new_mpc(prec), _del_mpc)

            if isinstance(args[0], mpc):
                gmp.mpc_set(self._mpc, args[0]._mpc, gmp.MPC_RNDNN)
            elif isinstance(args[0], complex):
                gmp.mpc_set_d_d(
                    self._mpc, args[0].real, args[0].imag, gmp.MPC_RNDNN)
        elif isinstance(args[0], (mpfr, mpq, mpz, float, int, long)):
            # First argument is real

            if nargs <= 2:
                prec = (0, 0)
            elif nargs == 3:
                prec = _check_prec(args[2])
            else:
                raise TypeError("function takes at most 3 arguments (4 given)")

            self._mpc = ffi.gc(_new_mpc(prec), _del_mpc)
            realref = gmp.mpc_realref(self._mpc)
            imagref = gmp.mpc_imagref(self._mpc)

            if isinstance(args[0], mpfr):
                gmp.mpfr_set(realref, args[0]._mpfr, gmp.MPFR_RNDN)
            elif isinstance(args[0], mpz):
                gmp.mpfr_set_z(realref, args[0]._mpz, gmp.MPFR_RNDN)
            elif isinstance(args[0], mpq):
                gmp.mpfr_set_q(realref, args[0]._mpq, gmp.MPFR_RNDN)
            elif isinstance(args[0], float):
                gmp.mpfr_set_d(realref, args[0], gmp.MPFR_RNDN)
            elif isinstance(args[0], (int, long)):
               _pyint_to_mpfr(args[0], realref)

            if nargs >= 2:
                # Check if second argument is real
                if isinstance(args[1], mpfr):
                    gmp.mpfr_set(imagref, args[1]._mpfr, gmp.MPFR_RNDN)
                elif isinstance(args[1], mpz):
                    gmp.mpfr_set_z(imagref, args[1]._mpz, gmp.MPFR_RNDN)
                elif isinstance(args[1], mpq):
                    gmp.mpfr_set_q(imagref, args[1]._mpq, gmp.MPFR_RNDN)
                elif isinstance(args[1], float):
                    gmp.mpfr_set_d(imagref, args[1], gmp.MPFR_RNDN)
                elif isinstance(args[1], (int, long)):
                    _pyint_to_mpfr(args[1], imagref)
                else:
                    raise TypeError(
                        "invalid type for imaginary component in mpc()")
            else:
                gmp.mpfr_set_ui(imagref, 0, gmp.MPFR_RNDN)
        else:
            raise TypeError("mpc() requires numeric or string argument")

    @classmethod
    def _from_c_mpc(cls, mpc):
        inst = object.__new__(cls)
        inst._mpc = ffi.gc(mpc, _del_mpc)
        return inst

    @property
    def precision(self):
        rprec, iprec = ffi.new('mpfr_prec_t *'), ffi.new('mpfr_prec_t *')
        gmp.mpc_get_prec2(rprec, iprec, self._mpc)
        return int(rprec[0]), int(iprec[0])

    @property
    def real(self):
        return mpfr._from_c_mpfr(gmp.mpc_realref(self._mpc))

    @property
    def imag(self):
        return mpfr._from_c_mpfr(gmp.mpc_imagref(self._mpc))

    def __str__(self):
        return _mpc_to_str(self._mpc, 10)

    def __repr__(self):
        prec = self.precision
        if prec[0] == prec[1] == gmp.mpfr_get_default_prec():
            # return "mpc('" + self.__str__() + "')"
            return "mpc('{0}')".format(self)
        else:
            return "mpc('{0}',({1[0]},{1[1]}))".format(self, prec)

    def __eq__(self, other):
        # Complex Comparison
        if isinstance(other, mpc):
            return gmp.mpc_cmp(self._mpc, other._mpc) == 0
        elif isinstance(other, complex):
            return (
                gmp.mpfr_cmp_d(gmp.mpc_realref(self._mpc), other.real) == 0 and
                gmp.mpfr_cmp_d(gmp.mpc_imagref(self._mpc), other.imag) == 0)

        # Real Comparison
        realref = gmp.mpc_realref(self._mpc)
        if isinstance(other, mpfr):
            result = gmp.mpfr_cmp(realref, other._mpfr)
        elif isinstance(other, float):
            result = gmp.mpfr_cmp_d(realref, other)
        elif isinstance(other, (int, long)):
            if -sys.maxsize - 1 <= other < sys.maxsize:
                result = gmp.mpfr_cmp_ui(realref, other)
            elif 0 <= other <= MAX_UI:
                result = gmp.mpfr_cmp_ui(realref, other)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                result = gmp.mpfr_cmp_z(realref, tmp_mpz)
                _del_mpz(tmp_mpz)
                result = result
        elif isinstance(other, mpz):
            result = gmp.mpfr_cmp_z(realref, other._mpz)
        elif isinstance(other, mpq):
            result = gmp.mpfr_cmp_q(realref, other._mpq)
        else:
            return NotImplemented

        if not gmp.mpfr_zero_p(gmp.mpc_imagref(self._mpc)):
            return False
        return result == 0

    def __lt__(self, other):
        raise TypeError('no ordering relation is defined for complex numbers')

    def __gt__(self, other):
        raise TypeError('no ordering relation is defined for complex numbers')

    def __le__(self, other):
        raise TypeError('no ordering relation is defined for complex numbers')

    def __ge__(self, other):
        raise TypeError('no ordering relation is defined for complex numbers')

    def __hash__(self):
        return hash(complex(self))

    def __float__(self):
        raise TypeError("can't covert 'mpc' to 'float'")

    def __int__(self):
        raise TypeError("can't covert 'mpc' to 'int'")

    def __long__(self):
        raise TypeError("can't covert 'mpc' to 'long'")

    def __complex__(self):
        return complex(
            gmp.mpfr_get_d(gmp.mpc_realref(self._mpc), gmp.MPFR_RNDN),
            gmp.mpfr_get_d(gmp.mpc_imagref(self._mpc), gmp.MPFR_RNDN))

    def __add__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpc):
            gmp.mpc_add(res, self._mpc, other._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpfr):
            gmp.mpc_add_fr(res, self._mpc, other._mpfr, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpfr_add_q(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_add_z(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpz, gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpfr_add_d(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other.real, gmp.MPFR_RNDN)
            gmp.mpfr_add_d(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other.imag, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_add_d(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other, gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_add_ui(res, self._mpc, other, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpfr_add_si(gmp.mpc_realref(res),
                                gmp.mpc_realref(self._mpc), other,
                                gmp.MPFR_RNDN)
                gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                             gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpfr_add_z(gmp.mpc_realref(res),
                               gmp.mpc_realref(self._mpc), tmp_mpz,
                               gmp.MPFR_RNDN)
                gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    __radd__ = __add__

    def __sub__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpc):
            gmp.mpc_sub(res, self._mpc, other._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpfr):
            gmp.mpc_sub_fr(res, self._mpc, other._mpfr, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpfr_sub_q(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_sub_z(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpz, gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpfr_sub_d(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other.real, gmp.MPFR_RNDN)
            gmp.mpfr_sub_d(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other.imag, gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_sub_d(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other, gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_sub_ui(res, self._mpc, other, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpfr_sub_si(gmp.mpc_realref(res),
                                gmp.mpc_realref(self._mpc), other,
                                gmp.MPFR_RNDN)
                gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                             gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpfr_sub_z(gmp.mpc_realref(res),
                               gmp.mpc_realref(self._mpc), tmp_mpz,
                               gmp.MPFR_RNDN)
                gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    def __rsub__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpfr):
            gmp.mpc_fr_sub(res, other._mpfr, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpfr_sub_q(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_neg(gmp.mpc_realref(res), gmp.mpc_realref(res),
                         gmp.MPFR_RNDN)
            gmp.mpfr_set(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_z_sub(gmp.mpc_realref(res), other._mpz,
                           gmp.mpc_realref(self._mpc), gmp.MPFR_RNDN)
            gmp.mpfr_neg(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpfr_d_sub(gmp.mpc_realref(res), other.real,
                           gmp.mpc_realref(self._mpc), gmp.MPFR_RNDN)
            gmp.mpfr_d_sub(gmp.mpc_imagref(res), other.imag,
                           gmp.mpc_imagref(self._mpc), gmp.MPFR_RNDN)
        elif isinstance(other, float):
            gmp.mpfr_d_sub(gmp.mpc_realref(res), other,
                           gmp.mpc_realref(self._mpc), gmp.MPFR_RNDN)
            gmp.mpfr_neg(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_ui_sub(res, other, self._mpc, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpfr_si_sub(gmp.mpc_realref(res),
                                other, gmp.mpc_realref(self._mpc),
                                gmp.MPFR_RNDN)
                gmp.mpfr_neg(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                             gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpfr_z_sub(gmp.mpc_realref(res),
                               tmp_mpz, gmp.mpc_realref(self._mpc),
                               gmp.MPFR_RNDN)
                gmp.mpfr_neg(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                         gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    def __mul__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpc):
            gmp.mpc_mul(res, self._mpc, other._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpfr):
            gmp.mpc_mul_fr(res, self._mpc, other._mpfr, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpfr_mul_q(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpq, gmp.MPFR_RNDN)
            gmp.mpfr_mul_q(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other._mpq, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpfr_mul_z(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpz, gmp.MPFR_RNDN)
            gmp.mpfr_mul_z(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpc_set_d_d(res, other.real, other.imag, gmp.MPC_RNDNN)
            gmp.mpc_mul(res, self._mpc, res, gmp.MPC_RNDNN)
        elif isinstance(other, float):
            gmp.mpfr_mul_d(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other, gmp.MPFR_RNDN)
            gmp.mpfr_mul_d(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpc_mul_si(res, self._mpc, other, gmp.MPC_RNDNN)
            elif 0 <= other <= MAX_UI:
                gmp.mpc_mul_ui(res, self._mpc, other, gmp.MPC_RNDNN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpfr_mul_z(gmp.mpc_realref(res),
                               gmp.mpc_realref(self._mpc), tmp_mpz,
                               gmp.MPFR_RNDN)
                gmp.mpfr_mul_z(gmp.mpc_imagref(res),
                               gmp.mpc_imagref(self._mpc), tmp_mpz,
                               gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    __rmul__ = __mul__

    def __truediv__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpc):
            gmp.mpc_div(res, self._mpc, other._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpfr):
            gmp.mpc_div_fr(res, self._mpc, other._mpfr, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpc_set_q(res, other._mpq, gmp.MPC_RNDNN)
            gmp.mpc_div(res, self._mpc, res, gmp.MPC_RNDNN)
        elif isinstance(other, mpz):
            gmp.mpfr_div_z(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other._mpz, gmp.MPFR_RNDN)
            gmp.mpfr_div_z(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other._mpz, gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpc_set_d_d(res, other.real, other.imag, gmp.MPC_RNDNN)
            gmp.mpc_div(res, self._mpc, res, gmp.MPC_RNDNN)
        elif isinstance(other, float):
            gmp.mpfr_div_d(gmp.mpc_realref(res), gmp.mpc_realref(self._mpc),
                           other, gmp.MPFR_RNDN)
            gmp.mpfr_div_d(gmp.mpc_imagref(res), gmp.mpc_imagref(self._mpc),
                           other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_div_ui(res, self._mpc, other, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpfr_div_si(gmp.mpc_realref(res),
                                gmp.mpc_realref(self._mpc), other,
                                gmp.MPFR_RNDN)
                gmp.mpfr_div_si(gmp.mpc_imagref(res),
                                gmp.mpc_imagref(self._mpc), other,
                                gmp.MPFR_RNDN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpfr_div_z(gmp.mpc_realref(res),
                               gmp.mpc_realref(self._mpc), tmp_mpz,
                               gmp.MPFR_RNDN)
                gmp.mpfr_div_z(gmp.mpc_imagref(res),
                               gmp.mpc_imagref(self._mpc), tmp_mpz,
                               gmp.MPFR_RNDN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpfr):
            gmp.mpc_fr_div(res, other._mpfr, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpc_set_q(res, other._mpq, gmp.MPC_RNDNN)
            gmp.mpc_div(res, res, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpz):
            gmp.mpc_set_z(res, other._mpz, gmp.MPC_RNDNN)
            gmp.mpc_div(res, res, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, complex):
            gmp.mpc_set_d_d(res, other.real, other.imag, gmp.MPC_RNDNN)
            gmp.mpc_div(res, res, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, float):
            gmp.mpc_set_d(res, other.real, gmp.MPC_RNDNN)
            gmp.mpc_div(res, res, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_ui_div(res, other, self._mpc, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpc_set_si(res, other, gmp.MPC_RNDNN)
                gmp.mpc_div(res, res, self._mpc, gmp.MPC_RNDNN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpc_set_z(res, tmp_mpz, gmp.MPC_RNDNN)
                gmp.mpc_div(res, res, self._mpc, gmp.MPC_RNDNN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    __rdiv__ = __rtruediv__

    def __pow__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpc):
            gmp.mpc_pow(res, self._mpc, other._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, mpfr):
            gmp.mpc_pow_fr(res, self._mpc, other._mpfr, gmp.MPC_RNDNN)
        elif isinstance(other, mpq):
            gmp.mpc_set_q(res, other._mpq, gmp.MPFR_RNDN)
            gmp.mpc_pow(res, self._mpc, res, gmp.MPC_RNDNN)
        elif isinstance(other, mpz):
            gmp.mpc_pow_z(res, self._mpc, other._mpz,
                          gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpc_set_d_d(res, other.real, other.imag, gmp.MPC_RNDNN)
            gmp.mpc_pow(res, self._mpc, res, gmp.MPC_RNDNN)
        elif isinstance(other, float):
            gmp.mpc_pow_d(res, self._mpc, other, gmp.MPFR_RNDN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_pow_ui(res, self._mpc, other, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpc_pow_si(res, self._mpc, other, gmp.MPC_RNDNN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpc_pow_z(res, self._mpc, tmp_mpz, gmp.MPC_RNDNN)
                _del_mpz(tmp_mpz)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    def __rpow__(self, other):
        res = _new_mpc()    # TODO use context precision
        if isinstance(other, mpfr):
            gmp.mpc_set_fr(res, other._mpfr, gmp.MPFR_RNDN)
            gmp.mpc_pow(res, res, self._mpc, gmp.MPFR_RNDN)
        elif isinstance(other, mpq):
            gmp.mpc_set_q(res, other._mpq, gmp.MPFR_RNDN)
            gmp.mpc_pow(res, res, self._mpc, gmp.MPFR_RNDN)
        elif isinstance(other, mpz):
            gmp.mpc_set_z(res, other._mpz, gmp.MPC_RNDNN)
            gmp.mpc_pow(res, res, self._mpc, gmp.MPFR_RNDN)
        elif isinstance(other, complex):
            gmp.mpc_set_d_d(res, other.real, other.imag, gmp.MPC_RNDNN)
            gmp.mpc_pow(res, res, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, float):
            gmp.mpc_set_d(res, other, gmp.MPFR_RNDN)
            gmp.mpc_pow(res, res, self._mpc, gmp.MPC_RNDNN)
        elif isinstance(other, (int, long)):
            if 0 <= other <= MAX_UI:
                gmp.mpc_set_ui(res, other, gmp.MPC_RNDNN)
            elif -sys.maxsize-1 <= other <= sys.maxsize:
                gmp.mpc_set_si(res, other, gmp.MPC_RNDNN)
            else:
                tmp_mpz = _new_mpz()
                _pyint_to_mpz(other, tmp_mpz)
                gmp.mpc_set_z(res, tmp_mpz, gmp.MPC_RNDNN)
                _del_mpz(tmp_mpz)
            gmp.mpc_pow(res, res, self._mpc, gmp.MPC_RNDNN)
        else:
            return NotImplemented
        return mpc._from_c_mpc(res)

    def __pos__(self):
        return self

    def __neg__(self):
        res = _new_mpc()
        gmp.mpc_neg(res, self._mpc, gmp.MPC_RNDNN)
        return mpc._from_c_mpc(res)

    def __abs__(self):
        res = _new_mpfr()
        gmp.mpc_abs(res, self._mpc, gmp.MPC_RNDNN)
        return mpfr._from_c_mpfr(res)

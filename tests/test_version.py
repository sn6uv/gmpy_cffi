import re
import pytest

from gmpy_cffi import version, mp_version, mpfr_version, mpc_version


class TestVersion:
    def test_version(self):
        s = version()
        assert isinstance(s, str)
        assert re.match(r'\d\.\d\.\d', s)

    def test_mp_version(self):
        s = mp_version()
        assert isinstance(s, str)
        assert s.startswith('GMP ')

    def test_mpfr_version(self):
        s = mpfr_version()
        assert isinstance(s, str)
        assert s.startswith('MPFR ')

    @pytest.mark.xfail(reason="mpc not implemented")
    def test_mpc_version(self):
        s = mpc_version()
        assert isinstance(s, str)
        assert s.startswith('MPC ')

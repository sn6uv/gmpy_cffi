import pytest

from gmpy_cffi import set_cache, get_cache, mpz, mpq, mpfr, mpc


class TestCache(object):
    def test_get_set_cache(self):
        assert get_cache() == (100, 128)
        set_cache(101, 128)
        assert get_cache() == (101, 128)
        with pytest.raises(ValueError):
            set_cache(-1, 128)
        with pytest.raises(ValueError):
            set_cache(100, -1)
        with pytest.raises(ValueError):
            set_cache(10001, 128)
        with pytest.raises(ValueError):
            set_cache(10001, 16385)
        with pytest.raises(TypeError):
            set_cache(mpz(100), 128)
        with pytest.raises(TypeError):
            set_cache(100, mpz(128))

    def test_mpz_cache(self):
        x = [mpz(i) for i in range(100)]    # from the cache
        y = [mpz(i) for i in range(100)]    # new instances
        del(x)  # refills the cache
        z = [mpq(i) for i in range(100)]    # from the cache again

    def test_mpq_cache(self):
        x = [mpq(i) for i in range(100)]    # from the cache
        y = [mpq(i) for i in range(100)]    # new instances
        del(x)  # refills the cache
        z = [mpq(i) for i in range(100)]    # from the cache again

    def test_mpfr_cache1(self):
        x = [mpfr(i) for i in range(100)]    # from the cache
        y = [mpfr(i) for i in range(100)]    # new instances
        del(x)  # refills the cache
        z = [mpfr(i) for i in range(100)]    # from the cache again

    def test_mpfr_cache2(self):
        x = [mpfr(i, 128) for i in range(100)]    # from the cache
        y = [mpfr(i, 128) for i in range(100)]    # new instances

    def test_mpc_cache1(self):
        x = [mpc(i) for i in range(100)]    # from the cache
        y = [mpc(i) for i in range(100)]    # new instances
        del(x)  # refills the cache
        z = [mpc(i) for i in range(100)]    # from the cache again

    def test_mpc_cache2(self):
        x = [mpc(i, 128) for i in range(100)]    # from the cache
        y = [mpc(i, 128) for i in range(100)]    # new instances


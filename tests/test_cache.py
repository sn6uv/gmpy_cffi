import pytest

from gmpy_cffi import set_cache, get_cache, mpz, mpq, mpfr, mpc

def _cache(f):
    size, obsize = get_cache()

    # Smaller than obsize
    x = [f(i) for i in range(size)]      # from the cache
    y = [f(i) for i in range(size)]      # new instances
    del(x)                              # refil the cache
    z = [f(i) for i in range(size)]      # from the cache again

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
        # reset the cache paramaters for other tests
        set_cache(100, 128)

    def test_mpz_cache(self):
        _cache(lambda i : mpz(i))

    def test_mpq_cache(self):
        _cache(lambda i : mpq(i))

    def test_mpfr_cache(self):
        _cache(lambda i : mpfr(i))
        _cache(lambda i : mpfr(i, 50))

    def test_mpc_cache(self):
        _cache(lambda i : mpc(i))
        _cache(lambda i : mpc(complex(i), (0, 0)))
        _cache(lambda i : mpc(complex(i), (50, 50)))
        _cache(lambda i : mpc(complex(i), (0, 100)))
        _cache(lambda i : mpc(complex(i), (100, 0)))
        _cache(lambda i : mpc(complex(i), (50, 100)))
        _cache(lambda i : mpc(complex(i), (50000, 50000)))

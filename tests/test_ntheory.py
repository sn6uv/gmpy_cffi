import pytest

from gmpy_cffi import mpz, mpq, mpfr, is_prime, next_prime, gcd, gcdext, lcm, invert, jacobi, legendre, kronecker, fac, bincoef, fib, fib2


class Test_ntheory(object):
    def test_is_prime(self):
        assert is_prime(2)
        assert is_prime(-5)
        assert not is_prime(mpz(4))
        assert [x for x in range(901, 1000) if is_prime(x)] == [907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
        assert is_prime(4547337172376300111955330758342147474062293202868155909489)
        assert not is_prime(4547337172376300111955330758342147474062293202868155909393)
        assert is_prime(643808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153)
        assert not is_prime(743808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153)
        assert is_prime(1537381, 1) and not is_prime(1537381, 2)
        assert is_prime(18790021, 2) and not is_prime(18790021, 3)

        # invalid x
        with pytest.raises(TypeError):
            is_prime(3, mpq(2, 1))
        with pytest.raises(TypeError):
            is_prime(mpq(5, 1), 6)
        with pytest.raises(TypeError):
            is_prime(mpfr(1.5))

        # nonpositive n
        with pytest.raises(ValueError):
            is_prime(5, 0)
        with pytest.raises(ValueError):
            is_prime(5, -4)

    def test_next_prime(self):
        assert next_prime(3) == mpz(5)
        assert next_prime(mpz(10000)) == mpz(10007)
        assert next_prime(-4) == mpz(2)
        assert next_prime(453425342532454325324532453245) == mpz(453425342532454325324532453293)
        with pytest.raises(TypeError):
            next_prime(mpq(1, 4))

    def test_gcd(self):
        assert gcd(4, 6) == mpz(2)
        assert gcd(5, 0) == mpz(5)
        assert gcd(5, 0) == mpz(5)
        assert gcd(323, 340) == gcd(mpz(323), 340) == gcd(323, mpz(340)) == gcd(mpz(323), mpz(340)) == mpz(17)
        with pytest.raises(TypeError):
            gcd(mpq(1.5), 2)
        with pytest.raises(TypeError):
            gcd(3)

    def test_gcdext(self):
        assert gcdext(15, 25) == (mpz(5), mpz(2), mpz(-1))
        assert gcdext(323, 340) == gcdext(mpz(323), 340) == gcdext(323, mpz(340)) == gcdext(mpz(323), mpz(340)) == (mpz(17), mpz(-1), mpz(1))
        with pytest.raises(TypeError):
            gcdext(mpq(1.5), 2)
        with pytest.raises(TypeError):
            gcd(3)

    def test_lcm(self):
        assert lcm(3, 4) == mpz(12)
        assert lcm(mpz(6), 9) == mpz(18)
        assert lcm(6, mpz(4)) == mpz(12)
        assert lcm(mpz(0), mpz(2)) == mpz(0)
        with pytest.raises(TypeError):
            lcm(mpq(1.5), 2)
        with pytest.raises(TypeError):
            lcm(3)

    def test_invert(self):
        assert invert(4, 5) == mpz(4)
        assert invert(3, 10) == mpz(7)
        with pytest.raises(ZeroDivisionError):
            invert(4, 6)
        with pytest.raises(ZeroDivisionError):
            invert(4, 0)

    def test_jacobi(self):
        assert jacobi(7, 3) == 1
        assert jacobi(5, 3) == -1
        assert jacobi(0, 3) == 0
        with pytest.raises(ValueError):
            jacobi(3, -1)
        with pytest.raises(ValueError):
            jacobi(3, 2)

    def test_legendre(self):
        assert legendre(7, 3) == 1
        assert legendre(5, 3) == -1
        assert legendre(0, 3) == 0
        with pytest.raises(ValueError):
            legendre(3, -1)
        with pytest.raises(ValueError):
            legendre(3, 2)

    def test_kronecker(self):
        assert kronecker(7, 3) == 1
        assert kronecker(5, 3) == -1
        assert kronecker(0, 3) == 0
        assert kronecker(3, -1) == 1
        assert kronecker(3, 2) == -1

    def test_fac(self):
        assert fac(0) == 1
        assert fac(10) == mpz(3628800)
        with pytest.raises(ValueError):
            fac(-1)
        with pytest.raises(TypeError):
            fac(45894575342551390123)
        # GNU MP: Cannot allocate memory (size=429440431952)
        # fac(3435523455234)

    def test_bincoef(self):
        assert bincoef(1, 4) == mpz(0)
        assert bincoef(19, 3) == mpz(969)
        with pytest.raises(ValueError):
            bincoef(1, -3)
        with pytest.raises(TypeError):
            bincoef(1, 2534253426342543253426)

    def test_fib(self):
        assert fib(4) == mpz(3)
        with pytest.raises(ValueError):
            fib(-3)
        with pytest.raises(TypeError):
            fib(45894575342551390123)

    def test_fib2(self):
        assert fib2(4) == (mpz(3), mpz(2))
        with pytest.raises(ValueError):
            fib2(-3)
        with pytest.raises(TypeError):
            fib2(45894575342551390123)

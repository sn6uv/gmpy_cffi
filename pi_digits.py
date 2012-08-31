import sys
from _gmpy import *

def inc(a, b): gmp.mpz_add_ui(a, a, b)
def iadd(a, b): gmp.mpz_add(a, a, b)
def imul(a, b): gmp.mpz_mul(a, a, b)
def imul10(a): gmp.mpz_mul_ui(a, a, 10)
def mpz_to_str(a): return ffi.string(gmp.mpz_get_str(ffi.NULL, 10, a))

def main(N):
    i = 0
    k, ns = mpz(0), mpz(0)
    k1 = mpz(1)
    n, a, d, t, u = mpz(1), mpz(0), mpz(1), mpz(0), mpz(0)
    tmp = mpz(0)
    while True:
        inc(k, 1)
        gmp.mpz_mul_ui(t, n, 2)
        imul(n, k)
        iadd(a, t)
        inc(k1, 2)
        imul(a, k1)
        imul(d, k1)
        if gmp.mpz_cmp(a, n) >= 0:
            gmp.mpz_mul_ui(tmp, n, 3)
            iadd(tmp, a)
            gmp.mpz_fdiv_qr(t, u, tmp, d)
            iadd(u, n)
            if gmp.mpz_cmp(d, u) > 0:
                imul10(ns)
                iadd(ns, t)
                i += 1
                if i % 10 == 0:
#                    print ('%s\t:%d' % (mpz_to_str(ns).zfill(10), i))
                    ns = mpz(0)
                if i >= N:
                    break
                gmp.mpz_submul(a, d, t)
                imul10(a)
                imul10(n)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 100)

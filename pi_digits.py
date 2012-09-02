import sys
from _gmpy import mpz

def main(N):
    i = 0
    k, ns = mpz(0), mpz(0)
    k1 = mpz(1)
    n, a, d, t, u = mpz(1), mpz(0), mpz(1), mpz(0), mpz(0)
    while True:
        k += 1
        t = n << 1
        n *= k
        a += t
        k1 += 2
        a *= k1
        d *= k1
        if a >= n:
            t, u = divmod(n * 3 + a, d)
            u += n
            if d > u:
                ns = ns * 10 + t
                i += 1
                if i % 10 == 0:
#                    print ('%010d\t:%d' % (ns, i))
                    ns = mpz(0)
                if i >= N:
                    break
                a -= d * t
                a *= 10
                n *= 10

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 100)

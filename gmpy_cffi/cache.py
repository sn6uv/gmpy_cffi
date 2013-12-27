import sys


from gmpy_cffi.interface import ffi, gmp


if sys.version > '3':
    long = int
    xrange = range


cache_size = 100
cache_obsize = 128


def get_cache():
    """
    get_cache() -> (cache_size, object_size)

    Return the current cache size (number of objects) and maximum size
    per object (number of limbs) for all GMPY2 objects.
    """
    return cache_size, cache_obsize


def set_cache(size, obsize):
    """
    set_cache(cache_size, object_size)

    Set the current cache size (number of objects) and the maximum size
    per object (number of limbs). Raises ValueError if cache size exceeds
    1000 or object size exceeds 16384
    """
    global cache_size, cache_obsize
    if not isinstance(size, (int, long)):
        raise TypeError("integer argument expected, got %s" % type(size))
    if not isinstance(obsize, (int, long)):
        raise TypeError("integer argument expected, got %s" % type(obsize))
    if size < 0 or size > 1000:
        raise ValueError("cache size must between 0 and 1000")
    if obsize < 0 or obsize > 16384:
        raise ValueError("object size must between 0 and 16384")

    cache_size = size
    cache_obsize = obsize
    _init_mpz_cache()
    _init_mpq_cache()
    _init_mpfr_cache()


# MPZ
def _init_mpz_cache():
    global mpz_cache, in_mpz_cache
    mpz_cache = []
    in_mpz_cache = cache_size
    for _ in xrange(cache_size):
        mpz = ffi.new("mpz_t")
        gmp.mpz_init(mpz)
        mpz_cache.append(mpz)
_init_mpz_cache()


def _new_mpz():
    """Return an initialized mpz_t."""
    global in_mpz_cache

    if in_mpz_cache:
        in_mpz_cache -= 1
        return mpz_cache[in_mpz_cache]
    else:
        mpz = ffi.new("mpz_t")
        gmp.mpz_init(mpz)
        return mpz


def _del_mpz(mpz):
    global in_mpz_cache

    if in_mpz_cache < cache_size:
        if ffi.sizeof(mpz[0]) <= cache_obsize:
            mpz_cache[in_mpz_cache] = mpz
        else:
            mpz_cache[in_mpz_cache] = ffi.new('mpz_t')
        in_mpz_cache += 1
    else:
        gmp.mpz_clear(mpz)

# MPQ
def _init_mpq_cache():
    global mpq_cache, in_mpq_cache
    mpq_cache = []
    in_mpq_cache = cache_size
    for _ in xrange(cache_size):
        mpq = ffi.new("mpq_t")
        gmp.mpq_init(mpq)
        mpq_cache.append(mpq)
_init_mpq_cache()


def _new_mpq():
    """Return an initialized mpq_t."""
    global in_mpq_cache

    if in_mpq_cache:
        in_mpq_cache -= 1
        return mpq_cache[in_mpq_cache]
    else:
        mpq = ffi.new("mpq_t")
        gmp.mpq_init(mpq)
        return mpq


def _del_mpq(mpq):
    global in_mpq_cache

    if in_mpq_cache < cache_size:
        if ffi.sizeof(mpq[0]) <= cache_obsize:
            mpq_cache[in_mpq_cache] = mpq
        else:
            mpq_cache[in_mpq_cache] = ffi.new('mpq_t')
        in_mpq_cache += 1
    else:
        gmp.mpq_clear(mpq)


# MPFR
def _init_mpfr_cache():
    global mpfr_cache, in_mpfr_cache
    mpfr_cache = []
    in_mpfr_cache = cache_size
    for _ in xrange(cache_size):
        mpfr = ffi.new("mpfr_t")
        gmp.mpfr_init(mpfr)
        mpfr_cache.append(mpfr)
_init_mpfr_cache()


def _new_mpfr(prec=0):
    """Return an initialized mpfr_t."""
    global in_mpfr_cache

    if isinstance(prec, (int, long)):
        if not (prec == 0 or gmp.MPFR_PREC_MIN <= prec <= gmp.MPFR_PREC_MAX):
            raise ValueError("invalid prec %i (wanted %s <= prec <= %s)" % (
                prec, gmp.MPFR_PREC_MIN, gmp.MPFR_PREC_MAX))
    else:
        raise TypeError('an integer is required')

    if in_mpfr_cache:
        in_mpfr_cache -= 1
        # Set default precision
        if prec == 0:
            gmp.mpfr_set_prec(mpfr_cache[in_mpfr_cache], gmp.mpfr_get_default_prec())
        else:
            gmp.mpfr_set_prec(mpfr_cache[in_mpfr_cache], prec)
        return mpfr_cache[in_mpfr_cache]
    else:
        mpfr = ffi.new("mpfr_t")
        if prec == 0:
            gmp.mpfr_init(mpfr)
        else:
            gmp.mpfr_init2(mpfr, prec)
        return mpfr


def _del_mpfr(mpfr):
    global in_mpfr_cache

    if in_mpfr_cache < cache_size:
        if ffi.sizeof(mpfr[0]) <= cache_obsize:
            mpfr_cache[in_mpfr_cache] = mpfr
        else:
            mpfr_cache[in_mpfr_cache] = ffi.new('mpfr_t')
        in_mpfr_cache += 1
    else:
        gmp.mpfr_clear(mpfr)


# MPC
def _init_mpc_cache():
    global mpc_cache, in_mpc_cache
    mpc_cache = []
    in_mpc_cache = cache_size
    for _ in xrange(cache_size):
        mpc = ffi.new("mpc_t")
        gmp.mpc_init2(mpc, gmp.mpfr_get_default_prec())
        mpc_cache.append(mpc)
_init_mpc_cache()


def _new_mpc(prec=(0,0)):
    """Return an initialized mpc_t."""
    global in_mpc_cache

    # prec is assumed to be checked already
    rprec, iprec = prec

    if not all(p == 0 or gmp.MPFR_PREC_MIN <= p <= gmp.MPFR_PREC_MAX
               for p in prec):
            raise ValueError(
                "invalid prec (wanted prec == 0 or %s <= prec <= %s)" % (
                    gmp.MPFR_PREC_MIN, gmp.MPFR_PREC_MAX))

    if in_mpc_cache:
        in_mpc_cache -= 1
        # Set default precision
        if rprec == iprec:
            if rprec  == 0:
                gmp.mpc_set_prec(mpc_cache[in_mpc_cache], gmp.mpfr_get_default_prec())
            else:
                gmp.mpc_set_prec(mpc_cache[in_mpc_cache], rprec)
        else:
            if rprec == 0:
                rprec = gmp.mpfr_get_default_prec()
            if iprec == 0:
                iprec = gmp.mpfr_get_default_prec()
            gmp.mpc_clear(mpc_cache[in_mpc_cache])
            gmp.mpc_init3(mpc_cache[in_mpc_cache], rprec, iprec)
        return mpc_cache[in_mpc_cache]
    else:
        mpc = ffi.new("mpc_t")
        if rprec == 0:
            rprec = gmp.mpfr_get_default_prec()
        if iprec == 0:
            iprec = gmp.mpfr_get_default_prec()
        if rprec == iprec:
            gmp.mpc_init2(mpc, rprec)
        else:
            gmp.mpc_init3(mpc, rprec, iprec)
        return mpc


def _del_mpc(mpc):
    global in_mpc_cache

    if in_mpc_cache < cache_size:
        mpc_cache[in_mpc_cache] = mpc
        # FIXME This doesn't seem to be working properly
        if ffi.sizeof(mpc[0]) <= cache_obsize:
            mpc_cache[in_mpc_cache] = mpc
        else:
            mpc_cache[in_mpc_cache] = ffi.new('mpc_t')

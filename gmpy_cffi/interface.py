import cffi


__all__ = "ffi", "gmp", "mpz"

ffi = cffi.FFI()

ffi.cdef("""
    // MPZ
    typedef struct { ...; } __mpz_struct;
    typedef __mpz_struct *mpz_t;
    typedef unsigned long mp_bitcnt_t;

    void mpz_init (mpz_t x);
    void mpz_clear (mpz_t x);

    void mpz_set_ui (mpz_t rop, unsigned long int op);
    void mpz_set_si (mpz_t rop, signed long int op);
    void mpz_set_d (mpz_t rop, double op);
    int mpz_set_str (mpz_t rop, char *str, int base);

    unsigned long int mpz_get_ui (mpz_t op);
    signed long int mpz_get_si (mpz_t op);
    double mpz_get_d (mpz_t op);
    char * mpz_get_str (char *str, int base, mpz_t op);
    void mpz_import (mpz_t rop, size_t count, int order, size_t size, int endian, size_t nails, const void *op);
    void * mpz_export (void *rop, size_t *countp, int order, size_t size, int endian, size_t nails, mpz_t op);

    void mpz_add (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_add_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_sub (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_sub_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_ui_sub (mpz_t rop, unsigned long int op1, mpz_t op2);
    void mpz_mul (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_mul_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_submul (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_mul_2exp (mpz_t rop, mpz_t op1, mp_bitcnt_t op2);
    void mpz_neg (mpz_t rop, mpz_t op);
    void mpz_abs (mpz_t rop, mpz_t op);

    void mpz_fdiv_q (mpz_t q, mpz_t n, mpz_t d);
    void mpz_fdiv_q_ui (mpz_t q, mpz_t n, unsigned long int d);
    void mpz_fdiv_r (mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_r_ui (mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_qr (mpz_t q, mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_qr_ui (mpz_t q, mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_q_2exp (mpz_t q, mpz_t n, mp_bitcnt_t b);
//    int mpz_divisible_ui_p (mpz_t n, unsigned long int d);

    void mpz_powm (mpz_t rop, mpz_t base, mpz_t exp, mpz_t mod);
    void mpz_powm_ui (mpz_t rop, mpz_t base, unsigned long int exp, mpz_t mod);
    void mpz_pow_ui (mpz_t rop, mpz_t base, unsigned long int exp);
    void mpz_ui_pow_ui (mpz_t rop, unsigned long int base, unsigned long int exp);

    int mpz_cmp (mpz_t op1, mpz_t op2);
    int mpz_cmp_ui (mpz_t op1, unsigned long int op2);
    int mpz_sgn (mpz_t op);

    void mpz_and (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_ior (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_xor (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_com (mpz_t rop, mpz_t op);

    int mpz_fits_ulong_p (mpz_t op);
    int mpz_fits_slong_p (mpz_t op);
    size_t mpz_sizeinbase (mpz_t op, int base);

//    void mpz_bin_ui (mpz_t rop, mpz_t n, unsigned long int k);
//    void mpz_bin_uiui (mpz_t rop, unsigned long int n, unsigned long int k);
""")

gmp = ffi.verify("#include <gmp.h>", libraries=['gmp', 'm'])

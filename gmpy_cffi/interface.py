import cffi


__all__ = "ffi", "gmp", "mpz"

ffi = cffi.FFI()

ffi.cdef("""
    const char * const gmp_version;

    // MPZ
    typedef struct { ...; } __mpz_struct;
    typedef __mpz_struct *mpz_t;
    typedef unsigned long mp_bitcnt_t;

    void mpz_init (mpz_t x);
    void mpz_clear (mpz_t x);

    void mpz_set (mpz_t rop, const mpz_t op);
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
    void mpz_mul_si (mpz_t rop, mpz_t op1, long int op2);
    void mpz_mul_ui (mpz_t rop, mpz_t op1, unsigned long int op2);
    void mpz_submul (mpz_t rop, mpz_t op1, mpz_t op2);
    void mpz_mul_2exp (mpz_t rop, mpz_t op1, mp_bitcnt_t op2);
    void mpz_neg (mpz_t rop, mpz_t op);
    void mpz_abs (mpz_t rop, mpz_t op);

    void mpz_cdiv_q (mpz_t q, mpz_t n, mpz_t d);

    void mpz_fdiv_q (mpz_t q, mpz_t n, mpz_t d);
    void mpz_fdiv_q_ui (mpz_t q, mpz_t n, unsigned long int d);
    void mpz_fdiv_r (mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_r_ui (mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_qr (mpz_t q, mpz_t r, mpz_t n, mpz_t d);
    void mpz_fdiv_qr_ui (mpz_t q, mpz_t r, mpz_t n, unsigned long int d);
    void mpz_fdiv_q_2exp (mpz_t q, mpz_t n, mp_bitcnt_t b);
//    int mpz_divisible_ui_p (mpz_t n, unsigned long int d);

    void mpz_tdiv_q (mpz_t q, const mpz_t n, const mpz_t d);

    void mpz_powm (mpz_t rop, mpz_t base, mpz_t exp, mpz_t mod);
    void mpz_powm_ui (mpz_t rop, mpz_t base, unsigned long int exp, mpz_t mod);
    void mpz_pow_ui (mpz_t rop, mpz_t base, unsigned long int exp);
    void mpz_ui_pow_ui (mpz_t rop, unsigned long int base, unsigned long int exp);

    int mpz_cmp (mpz_t op1, mpz_t op2);
    int mpz_cmp_d (const mpz_t op1, double op2);
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

    // Number Theoretic Functions
    int mpz_probab_prime_p (const mpz_t n, int reps);
    void mpz_nextprime (mpz_t rop, const mpz_t op);
    void mpz_gcd (mpz_t rop, const mpz_t op1, const mpz_t op2);
    // unsigned long int mpz_gcd_ui (mpz_t rop, const mpz_t op1, unsigned long int op2);
    void mpz_gcdext (mpz_t g, mpz_t s, mpz_t t, const mpz_t a, const mpz_t b);
    void mpz_lcm (mpz_t rop, const mpz_t op1, const mpz_t op2);
    // void mpz_lcm_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
    int mpz_invert (mpz_t rop, const mpz_t op1, const mpz_t op2);
    int mpz_jacobi (const mpz_t a, const mpz_t b);
    int mpz_legendre (const mpz_t a, const mpz_t p);
    int mpz_kronecker (const mpz_t a, const mpz_t b);
    // int mpz_kronecker_si (const mpz_t a, long b);
    // int mpz_kronecker_ui (const mpz_t a, unsigned long b);
    // int mpz_si_kronecker (long a, const mpz_t b);
    // int mpz_ui_kronecker (unsigned long a, const mpz_t b);
    void mpz_fac_ui (mpz_t rop, unsigned long int n);
    // void mpz_2fac_ui (mpz_t rop, unsigned long int n);
    // void mpz_mfac_uiui (mpz_t rop, unsigned long int n, unsigned long int m);
    // void mpz_primorial_ui (mpz_t rop, unsigned long int n);
    void mpz_bin_ui (mpz_t rop, const mpz_t n, unsigned long int k);
    void mpz_bin_uiui (mpz_t rop, unsigned long int n, unsigned long int k);
    void mpz_fib_ui (mpz_t fn, unsigned long int n);
    void mpz_fib2_ui (mpz_t fn, mpz_t fnsub1, unsigned long int n);
    void mpz_lucnum_ui (mpz_t ln, unsigned long int n);
    void mpz_lucnum2_ui (mpz_t ln, mpz_t lnsub1, unsigned long int n);

    // MPQ
    typedef struct { ...; } __mpq_struct;
    typedef __mpq_struct *mpq_t;

    void mpq_init (mpq_t x);
    void mpq_clear (mpq_t x);

    void mpq_canonicalize (mpq_t op);

    void mpq_set (mpq_t rop, const mpq_t op);
    void mpq_set_z (mpq_t rop, const mpz_t op);
    void mpq_set_ui (mpq_t rop, unsigned long int op1, unsigned long int op2);
    void mpq_set_si (mpq_t rop, signed long int op1, unsigned long int op2);
    int mpq_set_str (mpq_t rop, const char *str, int base);

    void mpq_set_d (mpq_t rop, double op);
    double mpq_get_d (mpq_t op);

    mpz_t mpq_numref (const mpq_t op);
    mpz_t mpq_denref (const mpq_t op);
    void mpq_get_num (mpz_t numerator, const mpq_t rational);
    void mpq_get_den (mpz_t denominator, const mpq_t rational);
    void mpq_set_num (mpq_t rational, const mpz_t numerator);
    void mpq_set_den (mpq_t rational, const mpz_t denominator);

    char * mpq_get_str (char *str, int base, const mpq_t op);

    void mpq_add (mpq_t sum, const mpq_t addend1, const mpq_t addend2);
    void mpq_sub (mpq_t difference, const mpq_t minuend, const mpq_t subtrahend);
    void mpq_mul (mpq_t product, const mpq_t multiplier, const mpq_t multiplicand);
    void mpq_mul_2exp (mpq_t rop, const mpq_t op1, mp_bitcnt_t op2);
    void mpq_div (mpq_t quotient, const mpq_t dividend, const mpq_t divisor);
    void mpq_div_2exp (mpq_t rop, const mpq_t op1, mp_bitcnt_t op2);
    void mpq_neg (mpq_t negated_operand, const mpq_t operand);
    void mpq_abs (mpq_t rop, const mpq_t op);
    void mpq_inv (mpq_t inverted_number, const mpq_t number);

    int mpq_cmp (const mpq_t op1, const mpq_t op2);
    int mpq_cmp_ui (const mpq_t op1, unsigned long int num2, unsigned long int den2);
    int mpq_cmp_si (const mpq_t op1, long int num2, unsigned long int den2);
    int mpq_sgn (const mpq_t op);
    int mpq_equal (const mpq_t op1, const mpq_t op2);

    // MPFR
    const char * mpfr_get_version (void);

    typedef struct { ...; } __mpfr_struct;
    typedef __mpfr_struct *mpfr_t;

    // FIXME - actual type depends on_MPFR_PREC_FORMAT
    typedef long int mpfr_prec_t;
    // FIXME - actual type depends on _MPFR_EXP_FORMAT
    typedef long int mpfr_exp_t;

    typedef enum {
      MPFR_RNDN=0,  /* round to nearest, with ties to even */
      MPFR_RNDZ,    /* round toward zero */
      MPFR_RNDU,    /* round toward +Inf */
      MPFR_RNDD,    /* round toward -Inf */
      MPFR_RNDA,    /* round away from zero */
      MPFR_RNDF,    /* faithful rounding (not implemented yet) */
      MPFR_RNDNA=-1 /* round to nearest, with ties away from zero (mpfr_round) */
    } mpfr_rnd_t;

    void mpfr_init (mpfr_t x);
    void mpfr_init2 (mpfr_t x, mpfr_prec_t prec);
    void mpfr_clear (mpfr_t x);
    void mpfr_set_default_prec (mpfr_prec_t prec);
    mpfr_prec_t mpfr_get_default_prec (void);

    void mpfr_set_prec (mpfr_t x, mpfr_prec_t prec);
    mpfr_prec_t mpfr_get_prec (mpfr_t x);
    int mpfr_sprintf (char *buf, const char *template, ...);
    int mpfr_printf (const char *template, ...);
    int mpfr_asprintf (char **str, const char *template, ...);

    int mpfr_set (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_set_ui (mpfr_t rop, unsigned long int op, mpfr_rnd_t rnd);
    int mpfr_set_si (mpfr_t rop, long int op, mpfr_rnd_t rnd);
    // int mpfr_set_uj (mpfr_t rop, uintmax_t op, mpfr_rnd_t rnd);
    // int mpfr_set_sj (mpfr_t rop, intmax_t op, mpfr_rnd_t rnd);
    // int mpfr_set_flt (mpfr_t rop, float op, mpfr_rnd_t rnd);
    int mpfr_set_d (mpfr_t rop, double op, mpfr_rnd_t rnd);
    // int mpfr_set_ld (mpfr_t rop, long double op, mpfr_rnd_t rnd);
    // int mpfr_set_decimal64 (mpfr_t rop, _Decimal64 op, mpfr_rnd_t rnd);
    int mpfr_set_z (mpfr_t rop, mpz_t op, mpfr_rnd_t rnd);
    int mpfr_set_q (mpfr_t rop, mpq_t op, mpfr_rnd_t rnd);
    // int mpfr_set_f (mpfr_t rop, mpf_t op, mpfr_rnd_t rnd);
    // int mpfr_set_ui_2exp (mpfr_t rop, unsigned long int op, mpfr_exp_t e, mpfr_rnd_t rnd);
    // int mpfr_set_si_2exp (mpfr_t rop, long int op, mpfr_exp_t e, mpfr_rnd_t rnd);
    // int mpfr_set_uj_2exp (mpfr_t rop, uintmax_t op, intmax_t e, mpfr_rnd_t rnd);
    // int mpfr_set_sj_2exp (mpfr_t rop, intmax_t op, intmax_t e, mpfr_rnd_t rnd);
    // int mpfr_set_z_2exp (mpfr_t rop, mpz_t op, mpfr_exp_t e, mpfr_rnd_t rnd);
    int mpfr_set_str (mpfr_t rop, const char *s, int base, mpfr_rnd_t rnd);
    // int mpfr_strtofr (mpfr_t rop, const char *nptr, char **endptr, int base, mpfr_rnd_t rnd);
    // void mpfr_set_nan (mpfr_t x);
    // void mpfr_set_inf (mpfr_t x, int sign);
    void mpfr_set_zero (mpfr_t x, int sign);
    // void mpfr_swap (mpfr_t x, mpfr_t y);

    // float mpfr_get_flt (mpfr_t op, mpfr_rnd_t rnd);
    double mpfr_get_d (mpfr_t op, mpfr_rnd_t rnd);
    // long double mpfr_get_ld (mpfr_t op, mpfr_rnd_t rnd);
    // _Decimal64 mpfr_get_decimal64 (mpfr_t op, mpfr_rnd_t rnd);
    long mpfr_get_si (mpfr_t op, mpfr_rnd_t rnd);
    unsigned long mpfr_get_ui (mpfr_t op, mpfr_rnd_t rnd);
    // intmax_t mpfr_get_sj (mpfr_t op, mpfr_rnd_t rnd);
    // uintmax_t mpfr_get_uj (mpfr_t op, mpfr_rnd_t rnd);
    // double mpfr_get_d_2exp (long *exp, mpfr_t op, mpfr_rnd_t rnd);
    // long double mpfr_get_ld_2exp (long *exp, mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_frexp (mpfr_exp_t *exp, mpfr_t y, mpfr_t x, mpfr_rnd_t rnd);
    // mpfr_exp_t mpfr_get_z_2exp (mpz_t rop, mpfr_t op);
    int mpfr_get_z (mpz_t rop, mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_get_f (mpf_t rop, mpfr_t op, mpfr_rnd_t rnd);
    char * mpfr_get_str (char *str, mpfr_exp_t *expptr, int b, size_t n, mpfr_t op, mpfr_rnd_t rnd);
    void mpfr_free_str (char *str);
    int mpfr_fits_ulong_p (mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_fits_slong_p (mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_fits_uint_p (mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_fits_sint_p (mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_fits_ushort_p (mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_fits_sshort_p (mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_fits_uintmax_p (mpfr_t op, mpfr_rnd_t rnd);
    // int mpfr_fits_intmax_p (mpfr_t op, mpfr_rnd_t rnd);

    /* Comparison functions */
    int mpfr_cmp (mpfr_t op1, mpfr_t op2);
    int mpfr_cmp_ui (mpfr_t op1, unsigned long int op2);
    int mpfr_cmp_si (mpfr_t op1, long int op2);
    int mpfr_cmp_d (mpfr_t op1, double op2);
    // int mpfr_cmp_ld (mpfr_t op1, long double op2);
    int mpfr_cmp_z (mpfr_t op1, mpz_t op2);
    int mpfr_cmp_q (mpfr_t op1, mpq_t op2);
    // int mpfr_cmp_f (mpfr_t op1, mpf_t op2);
    // int mpfr_cmp_ui_2exp (mpfr_t op1, unsigned long int op2, mpfr_exp_t e);
    // int mpfr_cmp_si_2exp (mpfr_t op1, long int op2, mpfr_exp_t e);
    // int mpfr_cmpabs (mpfr_t op1, mpfr_t op2);
    int mpfr_nan_p (mpfr_t op);
    int mpfr_inf_p (mpfr_t op);
    int mpfr_number_p (mpfr_t op);
    int mpfr_zero_p (mpfr_t op);
    int mpfr_regular_p (mpfr_t op);
    // int mpfr_sgn (mpfr_t op);
    // int mpfr_greater_p (mpfr_t op1, mpfr_t op2);
    // int mpfr_greaterequal_p (mpfr_t op1, mpfr_t op2);
    // int mpfr_less_p (mpfr_t op1, mpfr_t op2);
    // int mpfr_lessequal_p (mpfr_t op1, mpfr_t op2);
    // int mpfr_equal_p (mpfr_t op1, mpfr_t op2);
    // int mpfr_unordered_p (mpfr_t op1, mpfr_t op2);
    // int mpfr_lessgreater_p (mpfr_t op1, mpfr_t op2);

    int mpfr_signbit (mpfr_t op);

    // void mpfr_set_default_rounding_mode (mpfr_rnd_t rnd);
    // mpfr_rnd_t mpfr_get_default_rounding_mode (void);
    int mpfr_prec_round (mpfr_t x, mpfr_prec_t prec, mpfr_rnd_t rnd);
    // mpfr_can_round (mpfr_t b, mpfr_exp_t err, mpfr_rnd_t rnd1, mpfr_rnd_t rnd2, mpfr_prec_t prec);
    mpfr_prec_t mpfr_min_prec (mpfr_t x);
    // char * mpfr_print_rnd_mode (mpfr_rnd_t rnd);

    #define MPFR_PREC_MIN ...
    #define MPFR_PREC_MAX ...

    /* Math functions */
    int mpfr_add (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_add_ui (mpfr_t rop, mpfr_t op1, unsigned long int op2, mpfr_rnd_t rnd);
    int mpfr_add_si (mpfr_t rop, mpfr_t op1, long int op2, mpfr_rnd_t rnd);
    int mpfr_add_d (mpfr_t rop, mpfr_t op1, double op2, mpfr_rnd_t rnd);
    int mpfr_add_z (mpfr_t rop, mpfr_t op1, mpz_t op2, mpfr_rnd_t rnd);
    int mpfr_add_q (mpfr_t rop, mpfr_t op1, mpq_t op2, mpfr_rnd_t rnd);
    int mpfr_sub (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_sub_ui (mpfr_t rop, mpfr_t op1, unsigned long int op2, mpfr_rnd_t rnd);
    int mpfr_sub_si (mpfr_t rop, mpfr_t op1, long int op2, mpfr_rnd_t rnd);
    int mpfr_sub_d (mpfr_t rop, mpfr_t op1, double op2, mpfr_rnd_t rnd);
    int mpfr_sub_z (mpfr_t rop, mpfr_t op1, mpz_t op2, mpfr_rnd_t rnd);
    int mpfr_sub_q (mpfr_t rop, mpfr_t op1, mpq_t op2, mpfr_rnd_t rnd);
    int mpfr_ui_sub(mpfr_t rop, unsigned long int op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_si_sub(mpfr_t rop, long int op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_d_sub (mpfr_t rop, double op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_z_sub (mpfr_t rop, mpz_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_neg (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_abs (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_mul (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_mul_ui (mpfr_t rop, mpfr_t op1, unsigned long int op2, mpfr_rnd_t rnd);
    int mpfr_mul_si (mpfr_t rop, mpfr_t op1, long int op2, mpfr_rnd_t rnd);
    int mpfr_mul_d (mpfr_t rop, mpfr_t op1, double op2, mpfr_rnd_t rnd);
    int mpfr_mul_z (mpfr_t rop, mpfr_t op1, mpz_t op2, mpfr_rnd_t rnd);
    int mpfr_mul_q (mpfr_t rop, mpfr_t op1, mpq_t op2, mpfr_rnd_t rnd);
    int mpfr_div (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_div_ui (mpfr_t rop, mpfr_t op1, unsigned long int op2, mpfr_rnd_t rnd);
    int mpfr_div_si (mpfr_t rop, mpfr_t op1, long int op2, mpfr_rnd_t rnd);
    int mpfr_div_d (mpfr_t rop, mpfr_t op1, double op2, mpfr_rnd_t rnd);
    int mpfr_div_z (mpfr_t rop, mpfr_t op1, mpz_t op2, mpfr_rnd_t rnd);
    int mpfr_div_q (mpfr_t rop, mpfr_t op1, mpq_t op2, mpfr_rnd_t rnd);
    int mpfr_ui_div (mpfr_t rop, unsigned long int op2, mpfr_t op1, mpfr_rnd_t rnd);
    int mpfr_si_div (mpfr_t rop, long int op2, mpfr_t op1, mpfr_rnd_t rnd);
    int mpfr_d_div (mpfr_t rop, double op2, mpfr_t op1, mpfr_rnd_t rnd);
    int mpfr_pow (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_pow_ui (mpfr_t rop, mpfr_t op1, unsigned long int op2, mpfr_rnd_t rnd);
    int mpfr_pow_si (mpfr_t rop, mpfr_t op1, long int op2, mpfr_rnd_t rnd);
    int mpfr_pow_z (mpfr_t rop, mpfr_t op1, mpz_t op2, mpfr_rnd_t rnd);

    int mpfr_floor(mpfr_t rop, mpfr_t op);
    int mpfr_ceil(mpfr_t rop, mpfr_t op);
    int mpfr_trunc(mpfr_t rop, mpfr_t op);
    // int mpfr_round(mpfr_t rop, mpfr_t op);

    /* Special functions */
    int mpfr_log (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_log2 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_log10 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_exp (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_exp2 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_exp10 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_cos (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_sin (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_tan (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_sin_cos (mpfr_t sop, mpfr_t cop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_sec (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_csc (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_cot (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_acos (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_asin (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_atan (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_atan2 (mpfr_t rop, mpfr_t y, mpfr_t x, mpfr_rnd_t rnd);
    int mpfr_cosh (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_sinh (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_tanh (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_sinh_cosh (mpfr_t sop, mpfr_t cop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_sech (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_csch (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_coth (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_acosh (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_asinh (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_atanh (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_fac_ui (mpfr_t rop, unsigned long int op, mpfr_rnd_t rnd);
    int mpfr_log1p (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_expm1 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_eint (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_li2 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_gamma (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_lngamma (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_lgamma (mpfr_t rop, int *signp, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_digamma (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_zeta (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_zeta_ui (mpfr_t rop, unsigned long op, mpfr_rnd_t rnd);
    int mpfr_erf (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_erfc (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_j0 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_j1 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_jn (mpfr_t rop, long n, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_y0 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_y1 (mpfr_t rop, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_yn (mpfr_t rop, long n, mpfr_t op, mpfr_rnd_t rnd);
    int mpfr_fma (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_t op3, mpfr_rnd_t rnd);
    int mpfr_fms (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_t op3, mpfr_rnd_t rnd);
    int mpfr_agm (mpfr_t rop, mpfr_t op1, mpfr_t op2, mpfr_rnd_t rnd);
    int mpfr_hypot (mpfr_t rop, mpfr_t x, mpfr_t y, mpfr_rnd_t rnd);
    int mpfr_ai (mpfr_t rop, mpfr_t x, mpfr_rnd_t rnd);
    int mpfr_const_log2 (mpfr_t rop, mpfr_rnd_t rnd);
    int mpfr_const_pi (mpfr_t rop, mpfr_rnd_t rnd);
    int mpfr_const_euler (mpfr_t rop, mpfr_rnd_t rnd);
    int mpfr_const_catalan (mpfr_t rop, mpfr_rnd_t rnd);
    // void mpfr_free_cache (void);
    // int mpfr_sum (mpfr_t rop, mpfr_ptr const tab[], unsigned long int n, mpfr_rnd_t rnd);

    // MPC
    const char * mpc_get_version (void);

    typedef struct { ...; } __mpc_struct;
    typedef __mpc_struct *mpc_t;

    typedef int mpc_rnd_t;

    #define MPC_RNDNN ...
    #define MPC_RNDNZ ...
    #define MPC_RNDNU ...
    #define MPC_RNDND ...
    #define MPC_RNDZN ...
    #define MPC_RNDZZ ...
    #define MPC_RNDZU ...
    #define MPC_RNDZD ...
    #define MPC_RNDUN ...
    #define MPC_RNDUZ ...
    #define MPC_RNDUU ...
    #define MPC_RNDUD ...
    #define MPC_RNDDN ...
    #define MPC_RNDDZ ...
    #define MPC_RNDDU ...
    #define MPC_RNDDD ...

    void mpc_init2 (mpc_t z, mpfr_prec_t prec);
    void mpc_init3 (mpc_t z, mpfr_prec_t prec_r, mpfr_prec_t prec_i);
    void mpc_clear (mpc_t z);
    void mpc_set_prec (mpc_t x, mpfr_prec_t prec);
    // mpfr_prec_t mpc_get_prec (mpc_t x);
    void mpc_get_prec2 (mpfr_prec_t* pr, mpfr_prec_t* pi, mpc_t x);

    int mpc_set (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_set_ui (mpc_t rop, unsigned long int op, mpc_rnd_t rnd);
    int mpc_set_si (mpc_t rop, long int op, mpc_rnd_t rnd);
    // int mpc_set_uj (mpc_t rop, uintmax_t op, mpc_rnd_t rnd);
    // int mpc_set_sj (mpc_t rop, intmax_t op, mpc_rnd_t rnd);
    int mpc_set_d (mpc_t rop, double op, mpc_rnd_t rnd);
    // int mpc_set_ld (mpc_t rop, long double op, mpc_rnd_t rnd);
    // int mpc_set_dc (mpc_t rop, double _Complex op, mpc_rnd_t rnd);
    // int mpc_set_ldc (mpc_t rop, long double _Complex op, mpc_rnd_t rnd);
    int mpc_set_z (mpc_t rop, mpz_t op, mpc_rnd_t rnd);
    int mpc_set_q (mpc_t rop, mpq_t op, mpc_rnd_t rnd);
    // int mpc_set_f (mpc_t rop, mpf_t op, mpc_rnd_t rnd);
    int mpc_set_fr (mpc_t rop, mpfr_t op, mpc_rnd_t rnd);

    // int mpc_set_ui_ui (mpc_t rop, unsigned long int op1, unsigned long int op2, mpc_rnd_t rnd);
    // int mpc_set_si_si (mpc_t rop, long int op1, long int op2, mpc_rnd_t rnd);
    // int mpc_set_uj_uj (mpc_t rop, uintmax_t op1, uintmax_t op2, mpc_rnd_t rnd);
    // int mpc_set_sj_sj (mpc_t rop, intmax_t op1, intmax_t op2, mpc_rnd_t rnd)
    int mpc_set_d_d (mpc_t rop, double op1, double op2, mpc_rnd_t rnd);
    // int mpc_set_ld_ld (mpc_t rop, long double op1, long double op2, mpc_rnd_t rnd);
    // int mpc_set_z_z (mpc_t rop, mpz_t op1, mpz_t op2, mpc_rnd_t rnd);
    // int mpc_set_q_q (mpc_t rop, mpq_t op1, mpq_t op2, mpc_rnd_t rnd);
    // int mpc_set_f_f (mpc_t rop, mpf_t op1, mpf_t op2, mpc_rnd_t rnd);
    // int mpc_set_fr_fr (mpc_t rop, mpfr_t op1, mpfr_t op2, mpc_rnd_t rnd);
    // void mpc_set_nan (mpc_t rop);
    // void mpc_swap (mpc_t op1, mpc_t op2);

    // double _Complex mpc_get_dc (mpc_t op, mpc_rnd_t rnd);
    // long double _Complex mpc_get_ldc (mpc_t op, mpc_rnd_t rnd);

    // int mpc_strtoc (mpc_t rop, const char *nptr, char **endptr, int base, mpc_rnd_t rnd);
    int mpc_set_str (mpc_t rop, const char *s, int base, mpc_rnd_t rnd);
    char * mpc_get_str (int b, size_t n, mpc_t op, mpc_rnd_t rnd);
    void mpc_free_str (char *str);
    // int mpc_inp_str (mpc_t rop, FILE *stream, size_t *read, int base, mpc_rnd_t rnd);
    // size_t mpc_out_str (FILE *stream, int base, size_t n_digits, mpc_t op, mpc_rnd_t rnd);

    mpfr_t mpc_realref (mpc_t op);
    mpfr_t mpc_imagref (mpc_t op);

    int mpc_cmp (mpc_t op1, mpc_t op2);
    // int mpc_cmp_si_si (mpc_t op1, long int op2r , long int op2i);
    // int mpc_cmp_si (mpc_t op1 , long int op2);

    int mpc_add (mpc_t rop, mpc_t op1, mpc_t op2 , mpc_rnd_t rnd);
    int mpc_add_ui (mpc_t rop, mpc_t op1, unsigned long int op2, mpc_rnd_t rnd);
    int mpc_add_fr (mpc_t rop, mpc_t op1, mpfr_t op2, mpc_rnd_t rnd);
    int mpc_sub (mpc_t rop , mpc_t op1 , mpc_t op2 , mpc_rnd_t rnd);
    int mpc_sub_fr (mpc_t rop , mpc_t op1 , mpfr_t op2 , mpc_rnd_t rnd);
    int mpc_fr_sub (mpc_t rop , mpfr_t op1 , mpc_t op2 , mpc_rnd_t rnd);
    int mpc_sub_ui (mpc_t rop , mpc_t op1 , unsigned long int op2 , mpc_rnd_t rnd);
    int mpc_ui_sub (mpc_t rop , unsigned long int op1 , mpc_t op2 , mpc_rnd_t rnd);
    int mpc_mul (mpc_t rop, mpc_t op1, mpc_t op2, mpc_rnd_t rnd);
    int mpc_mul_ui (mpc_t rop, mpc_t op1, unsigned long int op2, mpc_rnd_t rnd);
    int mpc_mul_si (mpc_t rop, mpc_t op1, long int op2, mpc_rnd_t rnd);
    int mpc_mul_fr (mpc_t rop, mpc_t op1, mpfr_t op2, mpc_rnd_t rnd);

    int mpc_div (mpc_t rop, mpc_t op1, mpc_t op2, mpc_rnd_t rnd);
    int mpc_div_ui (mpc_t rop, mpc_t op1, unsigned long int op2, mpc_rnd_t rnd);
    int mpc_div_fr (mpc_t rop, mpc_t op1, mpfr_t op2, mpc_rnd_t rnd);
    int mpc_ui_div (mpc_t rop, unsigned long int op1, mpc_t op2, mpc_rnd_t rnd);
    int mpc_fr_div (mpc_t rop, mpfr_t op1, mpc_t op2, mpc_rnd_t rnd);

    int mpc_pow (mpc_t rop , mpc_t op1 , mpc_t op2 , mpc_rnd_t rnd);
    int mpc_pow_d (mpc_t rop , mpc_t op1 , double op2 , mpc_rnd_t rnd);
    int mpc_pow_ld (mpc_t rop , mpc_t op1 , long double op2 , mpc_rnd_t rnd);
    int mpc_pow_si (mpc_t rop , mpc_t op1 , long op2 , mpc_rnd_t rnd);
    int mpc_pow_ui (mpc_t rop , mpc_t op1 , unsigned long op2 , mpc_rnd_t rnd);
    int mpc_pow_z (mpc_t rop , mpc_t op1 , mpz_t op2 , mpc_rnd_t rnd);
    int mpc_pow_fr (mpc_t rop , mpc_t op1 , mpfr_t op2 , mpc_rnd_t rnd);
    int mpc_abs (mpfr_t rop , mpc_t op , mpfr_rnd_t rnd);
    int mpc_neg (mpc_t rop , mpc_t op , mpc_rnd_t rnd);

    int mpc_fma (mpc_t rop, mpc_t op1, mpc_t op2, mpc_t op3, mpc_rnd_t rnd);
    int mpc_exp (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_log (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    // Requires mpc >= 1.0.1
    // int mpc_log10 (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_sin (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_cos (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_sin_cos (mpc_t rop_sin, mpc_t rop_cos, mpc_t op, mpc_rnd_t rnd_sin, mpc_rnd_t rnd_cos);
    int mpc_tan (mpc_t rop, mpc_t op, mpc_rnd_t rnd);

    int mpc_sinh (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_cosh (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_tanh (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_asin (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_acos (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_atan (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_asinh (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_acosh (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
    int mpc_atanh (mpc_t rop, mpc_t op, mpc_rnd_t rnd);
""")

gmp = ffi.verify("""
    #include <gmp.h>
    #include <mpfr.h>
    #include <mpc.h>
""", libraries=['gmp', 'mpfr', 'mpc'])

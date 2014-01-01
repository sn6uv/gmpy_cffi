GMPY_CFFI
=========

GMPY_CFFI is a python wrapper of the GNU Multiple Precision Arithmetic Library.
It aims to be a PyPy compatible alternative to gmpy2.
Consequently we use the python cffi library to wrap:

-  GMP for integer and rational arithmetic.
-  MPFR for correctly rounded floating-point arithmetic.
-  MPC for correctly rounded complex floating-point arithmetic.

Installation
------------

To install gmpy_cffi, simply run::

    $ pip install gmpy_cffi

|Travis|_

.. |Travis| image:: https://travis-ci.org/sn6uv/gmpy_cffi.png?branch=master

.. _Travis: https://travis-ci.org/sn6uv/gmpy_cffi

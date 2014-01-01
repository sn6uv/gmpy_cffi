from setuptools import setup

import gmpy_cffi.interface

setup(
    name='gmpy_cffi',
    version='0.1',
    author="Angus Griffith",
    author_email="16sn6uv@gmail.com",
    license="3-clause BSD",
    description="GMP CFFI wrapper",
    url="https://github.com/sn6uv/gmpy_cffi",
    download_url="https://github.com/sn6uv/gmpy_cffi/tarball/0.1",
    keywords=["PyPy", "gmp"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['gmpy_cffi'],
    zip_safe=False,
    ext_modules=[gmpy_cffi.interface.ffi.verifier.get_extension()],
)

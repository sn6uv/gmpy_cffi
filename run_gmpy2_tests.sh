if [[ ! -d gmpy2 ]]; then
    svn export -q http://gmpy.googlecode.com/svn/trunk/ gmpy2/
fi
find gmpy2/{test,test2,test3} -type f -print0 | xargs -0 sed -i 's/import gmpy2 as /import gmpy_cffi as /'
find gmpy2/{test,test2,test3} -type f -print0 | xargs -0 sed -i 's/from gmpy2 import /from gmpy_cffi import /'
find gmpy2/{test,test2,test3} -type f -print0 | xargs -0 sed -i 's/import gmpy2/import gmpy_cffi as gmpy2/'
python gmpy2/test/runtests.py

# distutils: language = c
# cython: language_level=3

from cython.parallel cimport prange

cdef long long soma_divisores_proprios(long long n) nogil:
    cdef long long i, s, outro
    if n <= 1:
        return 0
    s = 1
    i = 2
    while i <= n // i:
        if n % i == 0:
            s += i
            outro = n // i
            if outro != i:
                s += outro
        i += 1
    return s


cpdef long long contar(long long limite, int threads):
    cdef long long total = 0
    cdef long long n
    for n in prange(1, limite + 1, nogil=True, schedule="static", chunksize=1, num_threads=threads):
        if soma_divisores_proprios(n) > n:
            total += 1
    return total

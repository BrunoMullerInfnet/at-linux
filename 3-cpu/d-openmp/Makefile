CC = gcc
CFLAGS = -O2

all: libdivisores.so openmp

libdivisores.so: divisores.c divisores.h
	$(CC) $(CFLAGS) -shared -fPIC -o libdivisores.so divisores.c

openmp: openmp.c divisores.c divisores.h
	$(CC) $(CFLAGS) -fopenmp -o openmp openmp.c divisores.c

clean:
	rm -f libdivisores.so openmp

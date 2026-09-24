#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#include "divisores.h"

int main(int argc, char **argv) {
    long long limite, total = 0;
    int pedidos;
    double t0, t1;

    if (argc < 3) {
        fprintf(stderr, "uso: openmp LIMITE THREADS\n");
        return 1;
    }

    limite = atoll(argv[1]);
    pedidos = atoi(argv[2]);
    omp_set_num_threads(pedidos);

    t0 = omp_get_wtime();
    #pragma omp parallel reduction(+:total)
    {
        int id = omp_get_thread_num();
        int p = omp_get_num_threads();
        /* thread id pega 1, 2, 3... e pula de p em p */
        total += conta_abundantes(id + 1, p, limite);
    }
    t1 = omp_get_wtime();

    printf("Numeros abundantes encontrados: %lld\n", total);
    printf("Tempo com %d threads no OpenMP: %.6f segundos\n", pedidos, t1 - t0);
    return 0;
}

#include "divisores.h"

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

long long soma_divisores_proprios(long long n) {
    long long i, s, outro;

    if (n <= 1) {
        return 0;
    }
    s = 1;
    for (i = 2; i <= n / i; i++) {
        if (n % i == 0) {
            s += i;
            outro = n / i;
            if (outro != i) {
                s += outro;
            }
        }
    }
    return s;
}

API long long conta_faixa(long long inicio, long long fim) {
    long long n, total = 0;

    for (n = inicio; n < fim; n++) {
        if (soma_divisores_proprios(n) > n) {
            total++;
        }
    }
    return total;
}

API long long conta_abundantes(long long inicio, long long passo, long long limite) {
    long long n, total = 0;

    for (n = inicio; n <= limite; n += passo) {
        if (soma_divisores_proprios(n) > n) {
            total++;
        }
    }
    return total;
}

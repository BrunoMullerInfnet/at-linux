# numero abundante: soma dos divisores proprios maior que o proprio numero
import ajuste

ajuste.pedir_desempenho()


def soma_divisores_proprios(n):
    if n <= 1:
        return 0
    s = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            s += i
            outro = n // i
            if outro != i:
                s += outro
        i += 1
    return s


def conta_abundantes(inicio, passo, limite):
    total = 0
    n = inicio
    while n <= limite:
        if soma_divisores_proprios(n) > n:
            total += 1
        n += passo
    return total


if __name__ == "__main__":
    # ate 100 existem 22 abundantes; serve de conferencia
    print(f"Numeros abundantes de 1 ate 100: {conta_abundantes(1, 1, 100)}")

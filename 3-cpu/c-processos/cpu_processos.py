import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from abundante import conta_abundantes


def trabalho(args):
    inicio, passo, limite = args
    return conta_abundantes(inicio, passo, limite)


def main():
    limite = int(sys.argv[1])
    p = int(sys.argv[2])
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=p) as ex:
        fatias = [(i, p, limite) for i in range(1, p + 1)]
        total = sum(ex.map(trabalho, fatias))
    dt = time.perf_counter() - t0
    print(f"Numeros abundantes encontrados: {total}")
    print(f"Tempo com {p} processos: {dt:.6f} segundos")


if __name__ == "__main__":
    main()

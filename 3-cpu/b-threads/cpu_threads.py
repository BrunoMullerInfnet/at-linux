import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from abundante import conta_abundantes


def main():
    limite = int(sys.argv[1])
    p = int(sys.argv[2])
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=p) as ex:
        partes = [ex.submit(conta_abundantes, i, p, limite) for i in range(1, p + 1)]
        total = sum(item.result() for item in partes)
    dt = time.perf_counter() - t0
    print(f"Numeros abundantes encontrados: {total}")
    print(f"Tempo com {p} threads e GIL ativo: {dt:.6f} segundos")


if __name__ == "__main__":
    main()

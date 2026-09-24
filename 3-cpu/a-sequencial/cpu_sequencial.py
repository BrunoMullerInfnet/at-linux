import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from abundante import conta_abundantes


def main():
    limite = int(sys.argv[1])
    t0 = time.perf_counter()
    total = conta_abundantes(1, 1, limite)
    dt = time.perf_counter() - t0
    print(f"Numeros abundantes encontrados: {total}")
    print(f"Tempo da versao sequencial: {dt:.6f} segundos")


if __name__ == "__main__":
    main()

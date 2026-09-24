import ctypes
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ajuste

ajuste.pedir_desempenho()

pasta = Path(__file__).resolve().parent.parent / "d-openmp"
nome = "divisores.dll" if sys.platform == "win32" else "libdivisores.so"
lib = ctypes.CDLL(str(pasta / nome))
lib.conta_abundantes.argtypes = [ctypes.c_longlong, ctypes.c_longlong, ctypes.c_longlong]
lib.conta_abundantes.restype = ctypes.c_longlong


def parcial(inicio, passo, limite):
    # o ctypes solta o GIL enquanto a funcao em C roda
    return lib.conta_abundantes(inicio, passo, limite)


def main():
    limite = int(sys.argv[1])
    p = int(sys.argv[2])
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=p) as ex:
        partes = [ex.submit(parcial, i, p, limite) for i in range(1, p + 1)]
        total = sum(item.result() for item in partes)
    dt = time.perf_counter() - t0
    print(f"Numeros abundantes encontrados: {total}")
    print(f"Tempo com {p} threads e GIL solto: {dt:.6f} segundos")


if __name__ == "__main__":
    main()

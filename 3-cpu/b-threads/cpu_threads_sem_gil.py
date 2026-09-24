import ctypes
import os
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ajuste

ajuste.pedir_desempenho()

pasta = Path(__file__).resolve().parent.parent / "d-openmp"
nome = "divisores.dll" if sys.platform == "win32" else "libdivisores.so"
lib = ctypes.CDLL(str(pasta / nome))
lib.conta_faixa.argtypes = [ctypes.c_longlong, ctypes.c_longlong]
lib.conta_faixa.restype = ctypes.c_longlong

LIMITE = 500_000
NUM_THREADS = 4


def contar(inicio, fim, resultados):
    # o ctypes solta o GIL enquanto a funcao em C roda
    resultados.append(lib.conta_faixa(inicio, fim))


def criar_intervalos():
    tamanho = LIMITE // NUM_THREADS
    intervalos = []
    for i in range(NUM_THREADS):
        inicio = i * tamanho + 1
        if i == NUM_THREADS - 1:
            fim = LIMITE + 1
        else:
            fim = inicio + tamanho
        intervalos.append((inicio, fim))
    return intervalos


if __name__ == "__main__":
    print("Python:", sys.version)
    print("GIL está habilitado: " + str(sys._is_gil_enabled()))
    print("CPUs disponíveis:", os.cpu_count())
    print("Num. threads:", NUM_THREADS)

    intervalos = criar_intervalos()
    print(intervalos)

    resultados = []
    threads = []
    inicio_tempo = time.perf_counter()
    for i in range(NUM_THREADS):
        thread = threading.Thread(
            target=contar,
            args=(intervalos[i][0], intervalos[i][1], resultados),
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    fim_tempo = time.perf_counter()

    quantidade = 0
    for parte in resultados:
        quantidade += parte
    print(f"Numeros abundantes encontrados: {quantidade}")
    print(f"Tempo com {NUM_THREADS} threads e GIL solto: {fim_tempo - inicio_tempo:.6f} segundos")

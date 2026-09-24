import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from urls import URLS


def baixa(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "at-linux"})
    with urllib.request.urlopen(pedido, timeout=60) as resp:
        return len(resp.read())


def main():
    t0 = time.perf_counter()
    total = 0
    for url in URLS:
        total += baixa(url)
    dt = time.perf_counter() - t0
    print(f"Total de bytes lidos: {total}")
    print(f"Tempo da versao sequencial: {dt:.6f} segundos")


if __name__ == "__main__":
    main()

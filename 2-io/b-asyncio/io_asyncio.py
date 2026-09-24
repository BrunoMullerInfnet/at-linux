import asyncio
import sys
import time
from pathlib import Path

import aiohttp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from urls import URLS


async def baixa(session, url):
    async with session.get(url) as resp:
        dados = await resp.read()
        return len(dados)


async def main():
    timeout = aiohttp.ClientTimeout(total=60)
    t0 = time.perf_counter()
    async with aiohttp.ClientSession(headers={"User-Agent": "at-linux"}, timeout=timeout) as session:
        tamanhos = await asyncio.gather(*(baixa(session, url) for url in URLS))
    dt = time.perf_counter() - t0
    print(f"Total de bytes lidos: {sum(tamanhos)}")
    print(f"Tempo da versao com asyncio: {dt:.6f} segundos")


if __name__ == "__main__":
    asyncio.run(main())

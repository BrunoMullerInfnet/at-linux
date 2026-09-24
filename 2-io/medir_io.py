import re
import subprocess
import sys
from pathlib import Path

pasta = Path(__file__).resolve().parent
saida = pasta / "resultados"
saida.mkdir(exist_ok=True)


def roda(script):
    proc = subprocess.run(
        [sys.executable, str(pasta / script)],
        cwd=pasta,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr)
        raise SystemExit(f"falhou: {script}")
    bytes_lidos = tempo = None
    for linha in proc.stdout.splitlines():
        if linha.startswith("Total de bytes lidos:"):
            bytes_lidos = int(re.search(r"\d+", linha).group())
        elif linha.startswith("Tempo"):
            tempo = float(re.search(r"\d+\.\d+", linha).group())
    if bytes_lidos is None or tempo is None:
        raise SystemExit(proc.stdout)
    return bytes_lidos, tempo


def main():
    seq_b, seq_t = roda("a-sequencial/io_sequencial.py")
    aio_b, aio_t = roda("b-asyncio/io_asyncio.py")
    ganho = seq_t / aio_t if aio_t else 0

    linhas = [
        "versao;bytes;tempo_s",
        f"sequencial;{seq_b};{seq_t:.4f}".replace(".", ","),
        f"asyncio;{aio_b};{aio_t:.4f}".replace(".", ","),
        f"ganho_seq_sobre_asyncio;;{ganho:.2f}".replace(".", ","),
    ]
    texto = "\n".join(linhas) + "\n"
    (saida / "io.csv").write_text(texto, encoding="utf-8")
    print(f"sequencial  bytes={seq_b}  tempo={seq_t:.3f}s")
    print(f"asyncio     bytes={aio_b}  tempo={aio_t:.3f}s")
    print(f"ganho       {ganho:.2f}x")
    print(f"csv em {saida / 'io.csv'}")


if __name__ == "__main__":
    main()

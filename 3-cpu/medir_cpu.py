import os
import re
import subprocess
import sys
import time
from pathlib import Path

import ajuste

ajuste.pedir_desempenho()

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent
saida = pasta / "resultados"
saida.mkdir(exist_ok=True)

limite = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
trabalhadores = [1, 2, 4, 8, 12]
gcc_bin = Path(r"C:\Users\bruno\w64devkit\w64devkit\bin")

env = os.environ.copy()
if gcc_bin.exists():
    env["PATH"] = str(gcc_bin) + os.pathsep + env.get("PATH", "")

py = sys.executable
openmp = pasta / "d-openmp" / ("openmp.exe" if os.name == "nt" else "openmp")
seq = pasta / "a-sequencial" / "cpu_sequencial.py"
threads_gil = pasta / "b-threads" / "cpu_threads.py"
threads_sem = pasta / "b-threads" / "cpu_threads_sem_gil.py"
processos = pasta / "c-processos" / "cpu_processos.py"


def mediana(valores):
    valores = sorted(valores)
    return valores[len(valores) // 2]


def rodar(cmd, reps):
    tempos = []
    resultado = None
    for _ in range(reps):
        flags = getattr(subprocess, "ABOVE_NORMAL_PRIORITY_CLASS", 0)
        proc = subprocess.run(
            cmd,
            cwd=pasta,
            capture_output=True,
            text=True,
            env=env,
            creationflags=flags,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout)
            sys.stderr.write(proc.stderr)
            raise SystemExit(f"falhou: {' '.join(map(str, cmd))}")
        valor = tempo = nthreads = None
        for linha in proc.stdout.splitlines():
            if linha.startswith("Numeros abundantes encontrados:"):
                valor = int(re.search(r"\d+", linha).group())
            elif linha.startswith("Num. threads:"):
                nthreads = int(re.search(r"\d+", linha).group())
            elif linha.startswith("Tempo"):
                tempo = float(re.search(r"\d+\.\d+", linha).group())
        if valor is None or tempo is None:
            raise SystemExit(proc.stdout)
        if resultado is None:
            resultado = valor
        elif valor != resultado:
            raise SystemExit(f"resultado diferente: {valor} != {resultado}")
        tempos.append(tempo)
    return resultado, mediana(tempos), nthreads


def num(valor, casas):
    return f"{valor:.{casas}f}".replace(".", ",")


def main():
    esperado, _, _ = rodar([py, str(seq), "100"], 1)
    if esperado != 22:
        raise SystemExit(f"conferencia ate 100 deu {esperado}, esperava 22")

    medidas = []

    def guarda(nome, p, resultado, tempo, base):
        if resultado != referencia:
            raise SystemExit(f"{nome} devolveu {resultado}, sequencial devolveu {referencia}")
        medidas.append(
            {
                "impl": nome,
                "p": p,
                "tempo": tempo,
                "speedup": base / tempo,
                "eficiencia": (base / tempo) / p,
                "resultado": resultado,
            }
        )
        print(f"{nome:20} p={p:<2}  {tempo:.3f}s", flush=True)

    print(f"limite = {limite}", flush=True)
    # aquece o turbo antes de cronometrar
    subprocess.run([str(openmp), "100000", "4"], cwd=pasta, env=env, capture_output=True)

    referencia, t_seq, _ = rodar([py, str(seq), str(limite)], 1)
    guarda("sequencial", 1, referencia, t_seq, t_seq)

    # GIL por ultimo: ele esquenta a maquina e atrapalha as outras medicoes
    grupos = [
        ("OpenMP", [str(openmp)], 5, True),
        ("threads sem GIL", [py, str(threads_sem)], 1, False),
        ("multiprocessing", [py, str(processos)], 1, True),
        ("threads com GIL", [py, str(threads_gil)], 1, False),
    ]

    for nome, prefixo, reps, varia_p in grupos:
        if nome == "threads com GIL":
            print("pausa para o processador esfriar", flush=True)
            time.sleep(20)
        base = None
        lista_p = trabalhadores if varia_p else [None]
        for p in lista_p:
            cmd = prefixo + [str(limite), str(p)] if varia_p else prefixo
            resultado, tempo, p_lido = rodar(cmd, reps)
            if p is None:
                p = p_lido
            if base is None:
                base = tempo
            guarda(nome, p, resultado, tempo, base)

    linhas = ["implementacao;trabalhadores;tempo_s;speedup;eficiencia;resultado"]
    for item in medidas:
        linhas.append(
            ";".join(
                [
                    item["impl"],
                    str(item["p"]),
                    num(item["tempo"], 4),
                    num(item["speedup"], 3),
                    num(item["eficiencia"], 3),
                    str(item["resultado"]),
                ]
            )
        )
    (saida / "cpu.csv").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    series = {}
    for item in medidas:
        series.setdefault(item["impl"], []).append(item)

    def grafico(campo, ylabel, arquivo, com_sequencial):
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for nome, pontos in series.items():
            if nome == "sequencial":
                if com_sequencial:
                    ax.axhline(pontos[0][campo], color="gray", linestyle="--", label="sequencial")
                continue
            ax.plot(
                [p["p"] for p in pontos],
                [p[campo] for p in pontos],
                marker="o",
                label=nome,
            )
        ax.set_xlabel("threads ou processos")
        ax.set_ylabel(ylabel)
        ax.set_title(f"abundantes ate {limite}")
        ax.set_xticks(trabalhadores)
        if campo in ("speedup", "eficiencia"):
            ax.axhline(1, color="black", linewidth=0.8)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(saida / arquivo, dpi=120)
        plt.close(fig)

    grafico("tempo", "tempo (s)", "tempo.png", True)
    grafico("speedup", "speedup", "speedup.png", False)
    grafico("eficiencia", "eficiencia", "eficiencia.png", False)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for nome in ("OpenMP", "threads sem GIL"):
        pontos = series[nome]
        ax.plot([p["p"] for p in pontos], [p["tempo"] for p in pontos], marker="o", label=nome)
    ax.set_xlabel("threads")
    ax.set_ylabel("tempo (s)")
    ax.set_title(f"versoes em C, ate {limite}")
    ax.set_xticks(trabalhadores)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(saida / "tempo_c.png", dpi=120)
    plt.close(fig)
    print(f"csv e graficos em {saida}")


if __name__ == "__main__":
    main()

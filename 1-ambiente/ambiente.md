# Questão 1 — ambiente de desenvolvimento

Os tempos foram medidos neste notebook, direto no Windows.

| item | valor |
|---|---|
| máquina | Lenovo, modelo 21NQ |
| processador | Intel Core i5-13420H (13ª geração) |
| núcleos físicos | 8 (4 de desempenho e 4 de eficiência) |
| processadores lógicos | 12 |
| frequência | base de 2,1 GHz; turbo até 4,6 GHz nos núcleos de desempenho |
| cache | 12 MB (L3) |
| memória principal | 16 GB (o Windows enxerga cerca de 15,5 GiB) |
| sistema operacional | Windows 11 Pro, 64 bits, versão 10.0.26200 |
| Python | 3.13.9, com GIL ativo |
| compilador C | GCC 16.2.0, com -O2 e OpenMP |
| máquina virtual | os testes rodaram no Windows, no próprio notebook |

Os 4 núcleos de desempenho têm hyper-thread, então cada um aparece como dois processadores lógicos. Os outros 4 são núcleos de eficiência, mais fracos. A conta é 4 x 2 + 4 = 12. Por isso o tempo melhora bem até 8 threads e quase para em 12.

Há um Ubuntu 24.04.3 no WSL2 (máquina virtual leve da Microsoft). Lá dentro aparecem 12 CPUs e 7,5 GiB de memória. Esse Ubuntu não entrou nos tempos: não tinha gcc instalado. O Makefile em `3-cpu/d-openmp` serve para compilar o C nesse Linux, se precisar.

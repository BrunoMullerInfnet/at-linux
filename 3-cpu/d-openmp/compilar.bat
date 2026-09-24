@echo off
gcc -O2 -shared -o divisores.dll divisores.c
if errorlevel 1 exit /b 1
gcc -O2 -fopenmp -o openmp.exe openmp.c divisores.c

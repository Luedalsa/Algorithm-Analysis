import random
import time

from AlgorithmComparation.ordenamiento import (
    bubble_sort_brute_force,
    selection_sort,
)


def ejecutar_pruebas(n_inicio, n_final, intervalo):
    tamanios = list(range(n_inicio, n_final + 1, intervalo))

    tiempos_selection = []
    tiempos_bubble = []

    for n in tamanios:
        numeros = [random.randint(1, 1_000_000) for _ in range(n)]

        copia = numeros.copy()
        inicio = time.perf_counter()
        selection_sort(copia)
        tiempo_selection = time.perf_counter() - inicio
        tiempos_selection.append(tiempo_selection)

        copia = numeros.copy()
        inicio = time.perf_counter()
        bubble_sort_brute_force(copia)
        tiempo_bubble = time.perf_counter() - inicio
        tiempos_bubble.append(tiempo_bubble)

        print(f"n = {n}")
        print(f"Selection Sort: {tiempo_selection:.6f} segundos")
        print(f"Bubble Sort:    {tiempo_bubble:.6f} segundos")
        print("-" * 40)

    return tamanios, tiempos_selection, tiempos_bubble
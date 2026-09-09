import random
import time

from AlgorithmComparation.ordenamiento import (
    bubble_sort_brute_force,
    exchange_sort,
    gnome_sort,
    insertion_sort,
    selection_sort,
    stooge_sort,
)


def ejecutar_pruebas(n_inicio, n_final, intervalo):
    tamanios = list(range(n_inicio, n_final + 1, intervalo))
    algoritmos = {
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort_brute_force,
        "Insertion Sort": insertion_sort,
        "Gnome Sort": gnome_sort,
        "Exchange Sort": exchange_sort,
        "Stooge Sort": stooge_sort,
    }
    tiempos = {nombre: [] for nombre in algoritmos}

    for n in tamanios:
        numeros = [random.randint(1, 1_000_000) for _ in range(n)]

        print(f"n = {n}")
        for nombre, algoritmo in algoritmos.items():
            inicio = time.perf_counter()
            algoritmo(numeros.copy())
            tiempo = time.perf_counter() - inicio
            tiempos[nombre].append(tiempo)
            print(f"{nombre}: {tiempo:.6f} segundos")
        print("-" * 40)

    return tamanios, tiempos
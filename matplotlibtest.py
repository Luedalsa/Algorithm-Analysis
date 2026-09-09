
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
import threading

def selection_sort(arr):
    n = len(arr)

    for i in range(n - 1):
        min_idx = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


def bubble_sort_brute_force(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

def ejecutar_pruebas(n_inicio, n_final, intervalo):

    tamanios = list(range(n_inicio, n_final + 1, intervalo))

    tiempos_selection = []
    tiempos_bubble = []

    for n in tamanios:

        # Generar números aleatorios
        numeros = [
            random.randint(1, 1_000_000)
            for _ in range(n)
        ]

        # Selection Sort

        copia = numeros.copy()

        inicio = time.perf_counter()
        selection_sort(copia)
        fin = time.perf_counter()

        tiempo_selection = fin - inicio
        tiempos_selection.append(tiempo_selection)

        # Bubble Sort

        copia = numeros.copy()

        inicio = time.perf_counter()
        bubble_sort_brute_force(copia)
        fin = time.perf_counter()

        tiempo_bubble = fin - inicio
        tiempos_bubble.append(tiempo_bubble)

        print(f"n = {n}")
        print(f"Selection Sort: {tiempo_selection:.6f} segundos")
        print(f"Bubble Sort:    {tiempo_bubble:.6f} segundos")
        print("-" * 40)

    return tamanios, tiempos_selection, tiempos_bubble

def mostrar_grafica(tamanios, tiempos_selection, tiempos_bubble):

    # Eliminar gráfica anterior si existe
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    figura, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        tamanios,
        tiempos_selection,
        marker="o",
        label="Selection Sort"
    )

    ax.plot(
        tamanios,
        tiempos_bubble,
        marker="o",
        label="Bubble Sort"
    )

    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo de ejecución (segundos)")
    ax.set_title("Comparación: Selection Sort vs Bubble Sort")

    ax.legend()
    ax.grid(True)

    figura.tight_layout()

    # Insertar Matplotlib dentro de Tkinter
    canvas = FigureCanvasTkAgg(
        figura,
        master=frame_grafica
    )

    canvas.draw()
    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True
    )

def ejecutar_en_hilo(n_inicio, n_final, intervalo):

    try:

        tamanios, tiempos_selection, tiempos_bubble = ejecutar_pruebas(
            n_inicio,
            n_final,
            intervalo
        )

        ventana.after(
            0,
            lambda: mostrar_grafica(
                tamanios,
                tiempos_selection,
                tiempos_bubble
            )
        )

        ventana.after(
            0,
            lambda: boton_ejecutar.config(
                state=tk.NORMAL
            )
        )

        ventana.after(
            0,
            lambda: etiqueta_estado.config(
                text="Pruebas terminadas."
            )
        )

    except Exception as error:

        ventana.after(
            0,
            lambda: messagebox.showerror(
                "Error",
                str(error)
            )
        )

        ventana.after(
            0,
            lambda: boton_ejecutar.config(
                state=tk.NORMAL
            )
        )


# ==========================================================
# VALIDAR Y COMENZAR
# ==========================================================

def comenzar():

    try:
        n_inicio = int(entry_inicio.get())
        n_final = int(entry_final.get())
        intervalo = int(entry_intervalo.get())

        boton_ejecutar.config(state=tk.DISABLED)

        etiqueta_estado.config(
            text="Ejecutando pruebas..."
        )

        # Ejecutar en segundo plano
        hilo = threading.Thread(
            target=ejecutar_en_hilo,
            args=(n_inicio, n_final, intervalo),
            daemon=True
        )

        hilo.start()

    except ValueError as error:

        messagebox.showerror(
            "Datos incorrectos",
            str(error)
        )

ventana = tk.Tk()

ventana.title(
    "Comparación de algoritmos de ordenamiento"
)

ventana.geometry("1000x700")

ventana.minsize(800, 600)

frame_controles = ttk.Frame(
    ventana,
    padding=15
)

frame_controles.pack(
    fill=tk.X
)


titulo = ttk.Label(
    frame_controles,
    text="Comparación de Selection Sort y Bubble Sort",
)

titulo.grid(
    row=0,
    column=0,
    columnspan=6,
    pady=(0, 15)
)

ttk.Label(
    frame_controles,
    text="N inicial:"
).grid(
    row=1,
    column=0,
    padx=5
)

entry_inicio = ttk.Entry(
    frame_controles,
    width=12
)

entry_inicio.grid(
    row=1,
    column=1,
    padx=5
)

entry_inicio.insert(
    0,
    "10"
)


# N final
ttk.Label(
    frame_controles,
    text="N final:"
).grid(
    row=1,
    column=2,
    padx=5
)

entry_final = ttk.Entry(
    frame_controles,
    width=12
)

entry_final.grid(
    row=1,
    column=3,
    padx=5
)

entry_final.insert(
    0,
    "5000"
)


# Intervalo
ttk.Label(
    frame_controles,
    text="Intervalo:"
).grid(
    row=1,
    column=4,
    padx=5
)

entry_intervalo = ttk.Entry(
    frame_controles,
    width=12
)

entry_intervalo.grid(
    row=1,
    column=5,
    padx=5
)

entry_intervalo.insert(
    0,
    "500"
)


# Botón ejecutar
boton_ejecutar = ttk.Button(
    frame_controles,
    text="Ejecutar",
    command=comenzar
)

boton_ejecutar.grid(
    row=2,
    column=0,
    columnspan=6,
    pady=15
)


# Estado
etiqueta_estado = ttk.Label(
    frame_controles,
    text="Introduce los valores y pulsa Ejecutar."
)

etiqueta_estado.grid(
    row=3,
    column=0,
    columnspan=6
)

frame_grafica = ttk.Frame(
    ventana,
    padding=10,
    relief=tk.SUNKEN
)

frame_grafica.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=(0, 10)
)

ventana.mainloop()


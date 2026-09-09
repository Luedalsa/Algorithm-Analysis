import threading
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from AlgorithmComparation.benchmark import ejecutar_pruebas


def mostrar_grafica(frame_grafica, tamanios, tiempos_selection, tiempos_bubble):
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    figura, ax = plt.subplots(figsize=(9, 5))
    ax.plot(tamanios, tiempos_selection, marker="o", label="Selection Sort")
    ax.plot(tamanios, tiempos_bubble, marker="o", label="Bubble Sort")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo de ejecución (segundos)")
    ax.set_title("Comparación: Selection Sort vs Bubble Sort")
    ax.legend()
    ax.grid(True)
    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def ejecutar_en_hilo(
    ventana,
    frame_grafica,
    boton_ejecutar,
    etiqueta_estado,
    n_inicio,
    n_final,
    intervalo,
):
    try:
        resultados = ejecutar_pruebas(n_inicio, n_final, intervalo)
        ventana.after(
            0,
            lambda: mostrar_grafica(frame_grafica, *resultados),
        )
        ventana.after(0, lambda: boton_ejecutar.config(state=tk.NORMAL))
        ventana.after(0, lambda: etiqueta_estado.config(text="Pruebas terminadas."))
    except Exception as error:
        ventana.after(0, lambda: messagebox.showerror("Error", str(error)))
        ventana.after(0, lambda: boton_ejecutar.config(state=tk.NORMAL))


def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Comparación de algoritmos de ordenamiento")
    ventana.geometry("1000x700")
    ventana.minsize(800, 600)

    frame_controles = ttk.Frame(ventana, padding=15)
    frame_controles.pack(fill=tk.X)

    titulo = ttk.Label(
        frame_controles,
        text="Comparación de Selection Sort y Bubble Sort",
    )
    titulo.grid(row=0, column=0, columnspan=6, pady=(0, 15))

    ttk.Label(frame_controles, text="N inicial:").grid(row=1, column=0, padx=5)
    entry_inicio = ttk.Entry(frame_controles, width=12)
    entry_inicio.grid(row=1, column=1, padx=5)
    entry_inicio.insert(0, "10")

    ttk.Label(frame_controles, text="N final:").grid(row=1, column=2, padx=5)
    entry_final = ttk.Entry(frame_controles, width=12)
    entry_final.grid(row=1, column=3, padx=5)
    entry_final.insert(0, "5000")

    ttk.Label(frame_controles, text="Intervalo:").grid(row=1, column=4, padx=5)
    entry_intervalo = ttk.Entry(frame_controles, width=12)
    entry_intervalo.grid(row=1, column=5, padx=5)
    entry_intervalo.insert(0, "500")

    etiqueta_estado = ttk.Label(
        frame_controles,
        text="Introduce los valores y pulsa Ejecutar.",
    )
    etiqueta_estado.grid(row=3, column=0, columnspan=6)

    frame_grafica = ttk.Frame(
        ventana,
        padding=10,
        relief=tk.SUNKEN,
    )
    frame_grafica.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=(0, 10),
    )

    def comenzar():
        try:
            n_inicio = int(entry_inicio.get())
            n_final = int(entry_final.get())
            intervalo = int(entry_intervalo.get())

            boton_ejecutar.config(state=tk.DISABLED)
            etiqueta_estado.config(text="Ejecutando pruebas...")

            hilo = threading.Thread(
                target=ejecutar_en_hilo,
                args=(
                    ventana,
                    frame_grafica,
                    boton_ejecutar,
                    etiqueta_estado,
                    n_inicio,
                    n_final,
                    intervalo,
                ),
                daemon=True,
            )
            hilo.start()
        except ValueError as error:
            messagebox.showerror("Datos incorrectos", str(error))

    boton_ejecutar = ttk.Button(
        frame_controles,
        text="Ejecutar",
        command=comenzar,
    )
    boton_ejecutar.grid(row=2, column=0, columnspan=6, pady=15)

    return ventana


def main():
    ventana = crear_ventana()
    ventana.mainloop()


if __name__ == "__main__":
    main()
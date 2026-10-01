import threading
import time
import tracemalloc

try:
    from .fibonacci import fib, fibdyn
except ImportError:
    from fibonacci import fib, fibdyn


def medir_tiempo(funcion, n):
    inicio = time.perf_counter()
    funcion(n)
    return time.perf_counter() - inicio


def medir_tiempo_y_espacio(funcion, n):
    tracemalloc.start()
    inicio = time.perf_counter()
    funcion(n)
    tiempo = time.perf_counter() - inicio
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return tiempo, memoria_pico / 1024


def ejecutar_pruebas(n_inicio, n_final, intervalo):
    if n_inicio < 0:
        raise ValueError("N inicial debe ser mayor o igual que cero.")
    if n_final < n_inicio:
        raise ValueError("N final debe ser mayor o igual que N inicial.")
    if intervalo <= 0:
        raise ValueError("El intervalo debe ser mayor que cero.")
    if n_final > 40:
        raise ValueError("Para evitar tiempos excesivos, N final no puede superar 40.")

    tamanios = list(range(n_inicio, n_final + 1, intervalo))
    tiempos_fib = []
    tiempos_fibdyn = []
    espacios_fibdyn = []

    for n in tamanios:
        tiempo_dinamico, espacio_dinamico = medir_tiempo_y_espacio(fibdyn, n)
        tiempos_fibdyn.append(tiempo_dinamico)
        espacios_fibdyn.append(espacio_dinamico)
        tiempos_fib.append(medir_tiempo(fib, n))

    return tamanios, tiempos_fib, tiempos_fibdyn, espacios_fibdyn


def mostrar_graficas(frame_graficas, resultados):
    import tkinter as tk

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    for widget in frame_graficas.winfo_children():
        widget.destroy()

    tamanios, tiempos_fib, tiempos_fibdyn, espacios_fibdyn = resultados
    figura, (ax_recursivo, ax_dinamico) = plt.subplots(1, 2, figsize=(12, 5))

    ax_espacio = ax_dinamico.twinx()
    linea_tiempo, = ax_dinamico.plot(
        tamanios,
        tiempos_fibdyn,
        marker="o",
        color="tab:blue",
        label="Tiempo de fibdyn",
    )
    linea_espacio, = ax_espacio.plot(
        tamanios,
        espacios_fibdyn,
        marker="s",
        color="tab:orange",
        label="Espacio de fibdyn",
    )
    ax_dinamico.set_xlabel("n")
    ax_dinamico.set_ylabel("Tiempo (segundos)", color="tab:blue")
    ax_espacio.set_ylabel("Memoria pico (KiB)", color="tab:orange")
    ax_dinamico.set_title("fibdyn: tiempo y espacio")
    ax_dinamico.grid(True)
    ax_dinamico.legend(
        [linea_tiempo, linea_espacio],
        [linea_tiempo.get_label(), linea_espacio.get_label()],
        loc="upper left",
    )

    ax_recursivo.plot(tamanios, tiempos_fib, marker="o", label="fib recursivo")
    ax_recursivo.plot(tamanios, tiempos_fibdyn, marker="o", label="fibdyn")
    ax_recursivo.set_xlabel("n")
    ax_recursivo.set_ylabel("Tiempo (segundos)")
    ax_recursivo.set_title("Comparación entre n y tiempo")
    ax_recursivo.legend()
    ax_recursivo.grid(True)

    figura.tight_layout()
    canvas = FigureCanvasTkAgg(figura, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def ejecutar_en_hilo(
    ventana,
    frame_graficas,
    boton_ejecutar,
    etiqueta_estado,
    n_inicio,
    n_final,
    intervalo,
):
    try:
        from tkinter import messagebox

        resultados = ejecutar_pruebas(n_inicio, n_final, intervalo)
        ventana.after(0, lambda: mostrar_graficas(frame_graficas, resultados))
        ventana.after(0, lambda: boton_ejecutar.config(state="normal"))
        ventana.after(0, lambda: etiqueta_estado.config(text="Pruebas terminadas."))
    except Exception as error:
        ventana.after(0, lambda: messagebox.showerror("Error", str(error)))
        ventana.after(0, lambda: boton_ejecutar.config(state="normal"))


def crear_ventana():
    import tkinter as tk
    from tkinter import messagebox, ttk

    ventana = tk.Tk()
    ventana.title("Análisis de Fibonacci")
    ventana.geometry("1200x700")
    ventana.minsize(900, 600)

    controles = ttk.Frame(ventana, padding=15)
    controles.pack(fill=tk.X)
    ttk.Label(
        controles,
        text="Comparación de Fibonacci recursivo y dinámico",
    ).grid(row=0, column=0, columnspan=6, pady=(0, 15))

    ttk.Label(controles, text="N inicial:").grid(row=1, column=0, padx=5)
    entrada_inicio = ttk.Entry(controles, width=12)
    entrada_inicio.grid(row=1, column=1, padx=5)
    entrada_inicio.insert(0, "5")

    ttk.Label(controles, text="N final:").grid(row=1, column=2, padx=5)
    entrada_final = ttk.Entry(controles, width=12)
    entrada_final.grid(row=1, column=3, padx=5)
    entrada_final.insert(0, "30")

    ttk.Label(controles, text="Intervalo:").grid(row=1, column=4, padx=5)
    entrada_intervalo = ttk.Entry(controles, width=12)
    entrada_intervalo.grid(row=1, column=5, padx=5)
    entrada_intervalo.insert(0, "1")

    etiqueta_estado = ttk.Label(
        controles,
        text="Introduce los valores y pulsa Ejecutar.",
    )
    etiqueta_estado.grid(row=3, column=0, columnspan=6)

    frame_graficas = ttk.Frame(ventana, padding=10, relief=tk.SUNKEN)
    frame_graficas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def comenzar():
        try:
            n_inicio = int(entrada_inicio.get())
            n_final = int(entrada_final.get())
            intervalo = int(entrada_intervalo.get())
            boton_ejecutar.config(state=tk.DISABLED)
            etiqueta_estado.config(text="Ejecutando pruebas...")
            threading.Thread(
                target=ejecutar_en_hilo,
                args=(
                    ventana,
                    frame_graficas,
                    boton_ejecutar,
                    etiqueta_estado,
                    n_inicio,
                    n_final,
                    intervalo,
                ),
                daemon=True,
            ).start()
        except ValueError as error:
            messagebox.showerror("Datos incorrectos", str(error))

    boton_ejecutar = ttk.Button(controles, text="Ejecutar", command=comenzar)
    boton_ejecutar.grid(row=2, column=0, columnspan=6, pady=15)
    return ventana


def main():
    crear_ventana().mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk

def mostrar_saludo():
    nombre = entrada.get()

    if not nombre:
        nombre = "mundo"

    print(f"Hola {nombre}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Saludo")
ventana.geometry("400x200")

# Texto
etiqueta = tk.Label(ventana, text="Escribe tu nombre:")
etiqueta.pack(pady=10)

# Entry
entrada = tk.Entry(ventana, width=30)
entrada.pack()

# Botón
boton = tk.Button(ventana, text="Saludar", command=mostrar_saludo)
boton.pack(pady=10)

# Ejecutar ventana
ventana.mainloop()

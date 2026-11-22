import tkinter as tk
from tkinter import messagebox
from persistencia import cargar_biblioteca, guardar_datos
from interfazTkinter import BibliotecaUI


def main():
    root = tk.Tk()
    try:
        biblioteca = cargar_biblioteca()
    except Exception as error:
        messagebox.showerror("Carga de datos", str(error))
        root.destroy()
        return
    BibliotecaUI(root, biblioteca)

    def cerrar():
        try:
            guardar_datos(biblioteca)
        except OSError as error:
            messagebox.showerror("Error al guardar", str(error))
            return
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", cerrar)
    root.mainloop()


if __name__ == "__main__":
    main()

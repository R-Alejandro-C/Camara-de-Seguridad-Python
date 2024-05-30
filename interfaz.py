import tkinter as tk
import subprocess

def camaraSeguridad():
    subprocess.Popen(['python', 'camaraSeguridad.py'])

def guardarNuevoRostro():
    nombreCarpeta = inputName.get()
    if nombreCarpeta:
        subprocess.Popen(["python", "almacenRostros.py", nombreCarpeta])
    else:
        print("Ingresa un nombre")

def close_app():
    root.destroy()

root = tk.Tk()
root.title("Interfaz de Usuario")
root.geometry("400x400")  

root.columnconfigure(0, weight=1)
root.rowconfigure([0, 1, 2, 3, 4], weight=1)

lblName = tk.Label(root, text="Nombre:")
lblName.grid(row=0, column=0, pady=10)

inputName = tk.Entry(root)
inputName.grid(row=1, column=0, pady=10)

btnInciarCamara = tk.Button(root, text="INICIAR CAMARA", command=camaraSeguridad)
btnInciarCamara.grid(row=2, column=0, pady=10)

btnGuardarRostro = tk.Button(root, text="GUARDAR NUEVO ROSTRO", command=guardarNuevoRostro)
btnGuardarRostro.grid(row=3, column=0, pady=10)

btnCerrar = tk.Button(root, text="Cerrar", command=close_app)
btnCerrar.grid(row=4, column=0, pady=10)

root.mainloop()

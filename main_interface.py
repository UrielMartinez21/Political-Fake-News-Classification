# -----------------------| Bibliotecas |-----------------------
import tkinter
from PIL import ImageTk, Image

# -----------------------| Inicio de interfaz |-----------------------

# --> Configuracion de ventana
ventana = tkinter.Tk()
ventana.geometry("800x700")
ventana.title("Detector de noticias falsas")
ventana.iconbitmap("diseño/logo/logo.ico")
ventana.config(bg="white")

# --> Contenido de ventana

# Icono en pantalla
imagen_logo = ImageTk.PhotoImage(Image.open("diseño/logo/logo.ico"))
label_imagen = tkinter.Label(image=imagen_logo)
label_imagen.place(relx=0.25, rely=0.05, relwidth=0.50, relheight=0.32)

# Label para indicar al usuario
label_instruccion = tkinter.Label(text="Ingresa tu información:")
label_instruccion.place(relx=0.2, rely=0.4)

# Input para que el usuario ingrese información
input_usuario = tkinter.Entry()
input_usuario.place(relx=0.35, rely=0.4, relwidth=0.3)

# --> Ejecutar ventana
ventana.mainloop()
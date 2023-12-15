# -----------------------| Bibliotecas |-----------------------
import tkinter
from PIL import ImageTk, Image

# -----------------------| Ejecutar al inicio |-----------------------

# -----------------------| Funciones |-----------------------

# -----------------------| Inicio de interfaz |-----------------------

# --> Configuracion de ventana
ventana = tkinter.Tk()
ventana.geometry("700x700")
ventana.title("Detector de noticias falsas")
ventana.iconbitmap("diseño/logo/logo.ico")
ventana.config(bg="white")

# --> Contenido de ventana

# Icono en pantalla
imagen_logo = ImageTk.PhotoImage(Image.open("diseño/logo/logo.ico"))        # Se abre la imagen
label_imagen = tkinter.Label(image=imagen_logo)                             # Se crea un label para la imagen
label_imagen.place(relx=0.20, rely=0.05, relwidth=0.60, relheight=0.3)     # Se coloca el label en la ventana

# Label de titulo
label_titulo = tkinter.Label(text="Título: ", bg="white", font="Arial 12 bold", fg="black")
label_titulo.place(relx=0.2, rely=0.4, relwidth=0.15, relheight=0.05)

# Input para titulo
input_titulo = tkinter.Entry()
input_titulo.place(relx=0.4, rely=0.4, relwidth=0.4, relheight=0.05)

# Label para descrpcion
label_descripcion = tkinter.Label(text="Descripción: ", bg="white", font="Arial 12 bold", fg="black")
label_descripcion.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.05)    

# Input para descripcion
input_descripcion = tkinter.Entry()
input_descripcion.place(relx=0.4, rely=0.5, relwidth=0.4, relheight=0.05)

# Label para fecha
label_fecha = tkinter.Label(text="Fecha: ", bg="white", font="Arial 14 bold", fg="black")
label_fecha.place(relx=0.2, rely=0.6, relwidth=0.15, relheight=0.05)

# Input para fecha
input_fecha = tkinter.Entry()
input_fecha.place(relx=0.4, rely=0.6, relwidth=0.4, relheight=0.05)

# Boton para ejecutar el programa
boton_detectar = tkinter.Button(text="Detectar", bg="white", font="Arial 14 bold", fg="black")
boton_detectar.place(relx=0.45, rely=0.7, relwidth=0.2, relheight=0.05)


# --> Ejecutar ventana
ventana.mainloop()
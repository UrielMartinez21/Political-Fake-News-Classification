# -----------------------| Bibliotecas |-----------------------
import tkinter
from PIL import ImageTk, Image
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, matthews_corrcoef
import random
import numpy as np

# -----------------------| Ejecutar al inicio |-----------------------
# Configurar semilla
seed = 26
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

# Rutas para el model entrenado y el tokenizador
model_path = "modelo/"
tokenizer_path = "modelo/"

# Cargar modelo entrenado y tokenizador
model = RobertaForSequenceClassification.from_pretrained(model_path, num_labels=2)
tokenizer = RobertaTokenizer.from_pretrained(tokenizer_path)

# Configuracion de batch
batch_size = 16

# Use GPU if available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# -----------------------| Funciones |-----------------------
def detectar_noticia():
    """
    Identificar si la noticia es falsa o verdadera
    """
    # --> Obtener datos
    titulo = input_titulo.get()
    descripcion = input_descripcion.get()
    fecha = input_fecha.get()

    # Tokeniza el nuevo ejemplo
    nuevos_encodings = tokenizer(
        titulo,
        descripcion,
        fecha,
        padding="max_length",
        truncation='only_second',
        max_length=128,
        return_tensors="pt"
    )

    # Obtiene los input_ids y attention_masks del nuevo ejemplo
    nuevos_input_ids = nuevos_encodings["input_ids"]
    nuevas_attention_masks = nuevos_encodings["attention_mask"]

    # Mueve los datos a la GPU si está disponible
    nuevos_input_ids = nuevos_input_ids.to(device)
    nuevas_attention_masks = nuevas_attention_masks.to(device)

    # Realiza la predicción
    with torch.no_grad():
        logits = model(nuevos_input_ids, attention_mask=nuevas_attention_masks).logits
        _, predicted_label = torch.max(logits, 1)

    # Convierte el resultado a una etiqueta legible
    etiqueta_predicha = "falsa" if predicted_label.item() == 0 else "verdadera"

    # Imprime la etiqueta predicha
    print(f"[+]La noticia es: {etiqueta_predicha}")


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
label_fecha = tkinter.Label(text="Fecha: ", bg="white", font="Arial 12 bold", fg="black")
label_fecha.place(relx=0.2, rely=0.6, relwidth=0.15, relheight=0.05)

# Input para fecha
input_fecha = tkinter.Entry()
input_fecha.place(relx=0.4, rely=0.6, relwidth=0.4, relheight=0.05)

# Boton para ejecutar el programa
boton_detectar = tkinter.Button(text="Detectar", bg="white", font="Arial 12 bold", fg="black", command=detectar_noticia)
boton_detectar.place(relx=0.45, rely=0.7, relwidth=0.2, relheight=0.05)


# --> Ejecutar ventana
ventana.mainloop()
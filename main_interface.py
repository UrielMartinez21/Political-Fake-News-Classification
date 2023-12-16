# -----------------------| Bibliotecas |-----------------------
# --> Bibliotecas para interfaz
import tkinter
from PIL import ImageTk, Image
# --> Bibliotecas para el modelo
import torch
import random
import numpy as np
from transformers import RobertaTokenizer, RobertaForSequenceClassification
# --> Bibliotecas para PDF
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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
def validar_campos_llenos():
    """
    Verifica si los campos obligatorios están llenos
    """
    return bool(input_titulo.get() and input_descripcion.get() and input_fecha.get())


def detectar_noticia():
    """
    Identificar si la noticia es falsa o verdadera
    """
    # Validar si los campos están llenos
    if not validar_campos_llenos():
        resultado_label.config(text="Por favor, completa todos los campos.", bg="red", fg="white")
        return

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

    # Actualiza la interfaz gráfica
    if etiqueta_predicha == "falsa":
        resultado_label.config(text="La noticia es FALSA", bg="red", fg="white")
    else:
        resultado_label.config(text="La noticia es VERDADERA", bg="green", fg="white")
    
    # Genera un PDF con la información
    generar_pdf(titulo, descripcion, fecha, etiqueta_predicha)


def generar_pdf(titulo, descripcion, fecha, etiqueta):
    """
    Genera un PDF con la información de la noticia
    """
    # Crear el nombre del archivo PDF con la fecha actual
    fecha_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    pdf_filename = f"noticia_{fecha_actual}.pdf"


    # Crear el documento PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    width, height = letter

    # Lista para almacenar los elementos del PDF
    story = []

    # Establecer estilos de texto
    styles = getSampleStyleSheet()

    # Encabezado
    encabezado_texto = "<b>Detector de noticias falsas</b>"
    story.append(Paragraph(encabezado_texto, styles["Normal"]))

    # Linea de separación
    story.append(Paragraph("<br/><br/>"))

    # Título
    titulo_texto = "<b>Título:</b><br/>" + titulo
    story.append(Paragraph(titulo_texto, styles["Normal"]))

    # Linea de separación
    story.append(Paragraph("<br/><br/>"))

    # Descripción
    descripcion_texto = "<b>Descripción:</b><br/>" + descripcion
    story.append(Paragraph(descripcion_texto, styles["Normal"]))

    # Linea de separación
    story.append(Paragraph("<br/><br/>"))

    # Fecha
    fecha_texto = "<b>Fecha:</b><br/>" + fecha
    story.append(Paragraph(fecha_texto, styles["Normal"]))

    # Linea de separación
    story.append(Paragraph("<br/><br/>"))

    # Etiqueta
    etiqueta_texto = "<b>La noticia es:</b>" + etiqueta
    story.append(Paragraph(etiqueta_texto, styles["Normal"]))

    # Construir el PDF
    doc.build(story)

    print(f"Se ha generado el PDF: {pdf_filename}")


# Boton para limpiar los inputs
def limpiar_inputs():
    input_titulo.delete(0, 'end')
    input_descripcion.delete(0, 'end')
    input_fecha.delete(0, 'end')
    resultado_label.config(text="", bg="#2F3131", fg="black")


# -----------------------| Inicio de interfaz |-----------------------

# --> Configuracion de ventana
ventana = tkinter.Tk()
ventana.geometry("700x700")
ventana.title("Detector de noticias falsas")
ventana.iconbitmap("diseño/logo/logo.ico")
ventana.config(bg="#2F3131")

# --> Contenido de ventana

# Icono en pantalla
imagen_logo = ImageTk.PhotoImage(Image.open("diseño/logo/logo.ico"))
label_imagen = tkinter.Label(image=imagen_logo, bg="#2F3131")
label_imagen.place(relx=0.20, rely=0.05, relwidth=0.60, relheight=0.3)

# Label de título
label_titulo = tkinter.Label(text="Título: ", bg="#F9BA32", font="Arial 12 bold", fg="#2F3131") 
label_titulo.place(relx=0.2, rely=0.4, relwidth=0.15, relheight=0.05)

# Input para título
input_titulo = tkinter.Entry(bg="#F9BA32", font="Arial 12")
input_titulo.place(relx=0.4, rely=0.4, relwidth=0.4, relheight=0.05)

# Label para descripción
label_descripcion = tkinter.Label(text="Descripción: ", bg="#F9BA32", font="Arial 12 bold", fg="#2F3131")
label_descripcion.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.05)

# Input para descripción
input_descripcion = tkinter.Entry(bg="#F9BA32", font="Arial 12")
input_descripcion.place(relx=0.4, rely=0.5, relwidth=0.4, relheight=0.05)

# Label para fecha
label_fecha = tkinter.Label(text="Fecha: ", bg="#F9BA32", font="Arial 12 bold", fg="#2F3131")
label_fecha.place(relx=0.2, rely=0.6, relwidth=0.15, relheight=0.05)

# Input para fecha
input_fecha = tkinter.Entry(bg="#F9BA32", font="Arial 12")
input_fecha.place(relx=0.4, rely=0.6, relwidth=0.4, relheight=0.05)

# Label para mostrar resultados
resultado_label = tkinter.Label(ventana, text="", bg="#2F3131", font="Arial 12 bold", fg="#F8F1E5")
resultado_label.place(relx=0.25, rely=0.8, relwidth=0.5, relheight=0.05)

# Botón para ejecutar el programa
boton_detectar = tkinter.Button(text="Detectar", bg="#F9BA32", font="Arial 12 bold", fg="#2F3131", command=detectar_noticia)
boton_detectar.place(relx=0.60, rely=0.7, relwidth=0.2, relheight=0.05)

# Botón para limpiar los inputs
boton_limpiar = tkinter.Button(text="Limpiar", bg="#426E86", font="Arial 12 bold", fg="#2F3131", command=limpiar_inputs)
boton_limpiar.place(relx=0.30, rely=0.7, relwidth=0.2, relheight=0.05)

# --> Ejecutar ventana
ventana.mainloop()

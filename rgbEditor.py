import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

imagen_original = None

def cargar_imagen():
    global imagen_original
    ruta_imagen = filedialog.askopenfilename(filetypes=(("Archivos de imagen", ".jpg;.png;.jpeg"), ("Todos los archivos", ".*")))
    if ruta_imagen:
        global imagen_original
        imagen_original = Image.open(ruta_imagen)
        imagen_original.thumbnail((400, 400))
        imagen_tk = ImageTk.PhotoImage(imagen_original)
        label_imagen_original.configure(image=imagen_tk)
        label_imagen_original.image = imagen_tk
        cargar_valores_rgb(imagen_original)
        generar_histogramas(imagen_original)
        establecer_sliders_a_uno()  # Establecer los sliders en 1.0

def establecer_sliders_a_uno():
    scale_r.set(1.0)
    scale_g.set(1.0)
    scale_b.set(1.0)

def establecer_valores_por_defecto():
    establecer_sliders_a_uno()

def cargar_valores_rgb(imagen):
    r, g, b = imagen.split()
    valor_r = r.getextrema()[1]
    valor_g = g.getextrema()[1]
    valor_b = b.getextrema()[1]
    scale_r.set(valor_r)
    scale_g.set(valor_g)
    scale_b.set(valor_b)

def generar_histogramas(imagen):
    r, g, b = imagen.split()
    histograma_r = r.histogram()
    histograma_g = g.histogram()
    histograma_b = b.histogram()
    mostrar_histograma(histograma_r, canvas_histograma_r)
    mostrar_histograma(histograma_g, canvas_histograma_g)
    mostrar_histograma(histograma_b, canvas_histograma_b)

def mostrar_histograma(histograma, canvas):
    canvas.delete("all")
    max_valor = max(histograma)
    ancho = 300  # Ajustado para que coincida con el nuevo tamaño del canvas
    altura = 150  # Ajustado para que coincida con el nuevo tamaño del canvas
    # Dibujar ejes
    canvas.create_line(30, altura-10, 30, 10, fill="black")  # Eje Y
    canvas.create_line(30, altura-10, ancho-10, altura-10, fill="black")  # Eje X
    for i, valor in enumerate(histograma):
        x = 30 + i * (ancho-40) / len(histograma)  # Ajustar la posición x para que empiece en el eje Y
        y = altura - 10  # Posición y en el eje X
        height = int(valor * (altura-20) / max_valor)  # Ajustar la altura para que no toque los ejes
        canvas.create_line(x, y, x, y - height, fill="black")
    canvas.pack()


def ajustar_contraste(imagen_canal, factor_contraste):
    return imagen_canal.point(lambda x: 128 + factor_contraste * (x - 128))

def modificar_imagen(*args):
    global imagen_original
    if imagen_original is not None:
        factor_r = scale_r.get()
        factor_g = scale_g.get()
        factor_b = scale_b.get()

        imagen_modificada = imagen_original.copy()
        r, g, b = imagen_modificada.split()

        # Multiplicar los valores de cada canal
        r = r.point(lambda x: min(255, int(x * factor_r)))
        g = g.point(lambda x: min(255, int(x * factor_g)))
        b = b.point(lambda x: min(255, int(x * factor_b)))

        imagen_modificada = Image.merge("RGB", (r, g, b))
        imagen_modificada.thumbnail((400, 400))
        imagen_tk = ImageTk.PhotoImage(imagen_modificada)

        label_imagen_modificada.configure(image=imagen_tk)
        label_imagen_modificada.image = imagen_tk

        mostrar_imagenes_rgb(r, g, b)
        generar_histogramas(imagen_modificada)
    else:
        print("Por favor, carga una imagen.")

def mostrar_imagenes_rgb(imagen_r, imagen_g, imagen_b):
    tamaño_miniatura_canal = (275, 275)
    imagen_r.thumbnail(tamaño_miniatura_canal)
    imagen_g.thumbnail(tamaño_miniatura_canal)
    imagen_b.thumbnail(tamaño_miniatura_canal)
    imagen_tk_r = ImageTk.PhotoImage(imagen_r)
    imagen_tk_g = ImageTk.PhotoImage(imagen_g)
    imagen_tk_b = ImageTk.PhotoImage(imagen_b)
    label_imagen_r.configure(image=imagen_tk_r)
    label_imagen_g.configure(image=imagen_tk_g)
    label_imagen_b.configure(image=imagen_tk_b)
    label_imagen_r.image = imagen_tk_r
    label_imagen_g.image = imagen_tk_g
    label_imagen_b.image = imagen_tk_b

def establecer_valores_por_defecto():
    establecer_sliders_a_uno()

# Crear ventana
ventana = tk.Tk()
ventana.title("Editor de Imágenes")

# Frame para la imagen original y modificada
frame_superior = tk.Frame(ventana)
frame_superior.pack(side=tk.TOP, fill=tk.X)

# Frame para la imagen original con su etiqueta
frame_imagen_original = tk.Frame(frame_superior, bd=2, relief=tk.RIDGE)
frame_imagen_original.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

label_titulo_original = tk.Label(frame_imagen_original, text="Imagen Original", font=("Arial", 12, "bold"))
label_titulo_original.pack()

label_imagen_original = tk.Label(frame_imagen_original)
label_imagen_original.pack()

# Frame para la imagen modificada con su etiqueta
frame_imagen_modificada = tk.Frame(frame_superior, bd=2, relief=tk.RIDGE)
frame_imagen_modificada.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.BOTH, expand=True)

label_titulo_modificada = tk.Label(frame_imagen_modificada, text="Imagen Modificada", font=("Arial", 12, "bold"))
label_titulo_modificada.pack()

label_imagen_modificada = tk.Label(frame_imagen_modificada)
label_imagen_modificada.pack()

# Frame para los canales y controles
frame_inferior = tk.Frame(ventana)
frame_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Función para crear un canal con histograma y slider
def crear_canal(frame, texto, color):
    frame_canal = tk.Frame(frame)
    frame_canal.pack(side=tk.LEFT, padx=15, fill=tk.BOTH, expand=True)

    label_titulo_canal = tk.Label(frame_canal, text=f"Canal {texto}", font=("Arial", 12, "bold"))
    label_titulo_canal.pack()

    label_imagen_canal = tk.Label(frame_canal)
    label_imagen_canal.pack(pady=5)

    # Aumentar el tamaño del canvas del histograma
    canvas_histograma = tk.Canvas(frame_canal, width=300, height=150)  # Nuevo tamaño para el histograma
    canvas_histograma.pack(pady=5)

    # Aumentar el tamaño del slider
    scale = tk.Scale(frame_canal, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, command=modificar_imagen, length=300)
    scale.set(1)
    scale.pack(pady=5)

    return label_imagen_canal, canvas_histograma, scale

# Crear canales RGB con histogramas y sliders
label_imagen_r, canvas_histograma_r, scale_r = crear_canal(frame_inferior, "Rojo", "red")
label_imagen_g, canvas_histograma_g, scale_g = crear_canal(frame_inferior, "Verde", "green")
label_imagen_b, canvas_histograma_b, scale_b = crear_canal(frame_inferior, "Azul", "blue")

# Botón para cargar imagen
boton_cargar = tk.Button(frame_superior, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(side=tk.BOTTOM, pady=10)

# Botón para establecer valores por defecto
boton_valores_por_defecto = tk.Button(frame_superior, text="Estado Inicial", command=establecer_valores_por_defecto)
boton_valores_por_defecto.pack(side=tk.BOTTOM, pady=5)

# Ejecutar la aplicación
ventana.mainloop()
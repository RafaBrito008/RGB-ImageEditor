import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        self.imagen_original = None
        self.tamaño_miniatura_canal = (275, 275)
        self.setup_ui()

    def setup_ui(self):
        self.setup_frames()
        self.setup_controls()
        self.setup_canvas_histogramas()

    def setup_frames(self):
        self.frame_superior = tk.Frame(self.root)
        self.frame_superior.pack(side=tk.TOP, fill=tk.X)

        self.frame_imagen_original, self.label_imagen_original = self.create_image_frame(self.frame_superior, "Imagen Original")
        self.frame_imagen_modificada, self.label_imagen_modificada = self.create_image_frame(self.frame_superior, "Imagen Modificada")

        self.frame_inferior = tk.Frame(self.root)
        self.frame_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def setup_controls(self):
        self.boton_cargar = tk.Button(self.frame_superior, text="Cargar Imagen", command=self.cargar_imagen)
        self.boton_cargar.pack(side=tk.BOTTOM, pady=10)

        self.boton_valores_por_defecto = tk.Button(self.frame_superior, text="Estado Inicial", command=self.establecer_sliders_a_uno)
        self.boton_valores_por_defecto.pack(side=tk.BOTTOM, pady=5)

    def setup_canvas_histogramas(self):
        self.label_imagen_r, self.canvas_histograma_r, self.scale_r = self.crear_canal(self.frame_inferior, "Rojo", "red")
        self.label_imagen_g, self.canvas_histograma_g, self.scale_g = self.crear_canal(self.frame_inferior, "Verde", "green")
        self.label_imagen_b, self.canvas_histograma_b, self.scale_b = self.crear_canal(self.frame_inferior, "Azul", "blue")

    def create_image_frame(self, parent, title):
        frame = tk.Frame(parent, bd=2, relief=tk.RIDGE)
        frame.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

        label_title = tk.Label(frame, text=title, font=("Arial", 12, "bold"))
        label_title.pack()

        label_image = tk.Label(frame)
        label_image.pack()

        return frame, label_image

    def crear_canal(self, frame, texto, color):
        frame_canal = tk.Frame(frame)
        frame_canal.pack(side=tk.LEFT, padx=15, fill=tk.BOTH, expand=True)

        label_titulo_canal = tk.Label(frame_canal, text=f"Canal {texto}", font=("Arial", 12, "bold"))
        label_titulo_canal.pack()

        label_imagen_canal = tk.Label(frame_canal)
        label_imagen_canal.pack(pady=5)

        canvas_histograma = tk.Canvas(frame_canal, width=300, height=150)
        canvas_histograma.pack(pady=5)

        scale = tk.Scale(frame_canal, from_=0.5, to=1.5, resolution=0.01, orient=tk.HORIZONTAL, command=self.modificar_imagen, length=300)
        scale.set(1)
        scale.pack(pady=5)

        return label_imagen_canal, canvas_histograma, scale

    def cargar_imagen(self):
        ruta_imagen = filedialog.askopenfilename(
            filetypes=(
                ("Archivos de imagen", ".jpg;.png;.jpeg"),
                ("Todos los archivos", ".*"),
            )
        )
        if ruta_imagen:
            self.imagen_original = Image.open(ruta_imagen)
            self.imagen_original.thumbnail((400, 400))
            imagen_tk = ImageTk.PhotoImage(self.imagen_original)
            self.label_imagen_original.configure(image=imagen_tk)
            self.label_imagen_original.image = imagen_tk
            self.cargar_valores_rgb(self.imagen_original)
            self.generar_histogramas(self.imagen_original)
            self.establecer_sliders_a_uno()

    def cargar_valores_rgb(self, imagen):
        r, g, b = imagen.split()
        self.scale_r.set(r.getextrema()[1])
        self.scale_g.set(g.getextrema()[1])
        self.scale_b.set(b.getextrema()[1])

    def generar_histogramas(self, imagen):
        r, g, b = imagen.split()
        self.mostrar_histograma(r.histogram(), self.canvas_histograma_r)
        self.mostrar_histograma(g.histogram(), self.canvas_histograma_g)
        self.mostrar_histograma(b.histogram(), self.canvas_histograma_b)

    def mostrar_histograma(self, histograma, canvas):
        canvas.delete("all")
        max_valor = max(histograma)
        ancho, altura = 300, 150
        canvas.create_line(30, altura - 10, 30, 10, fill="black")
        canvas.create_line(30, altura - 10, ancho - 10, altura - 10, fill="black")
        for i, valor in enumerate(histograma):
            x = 30 + i * (ancho - 40) / len(histograma)
            y = altura - 10
            height = int(valor * (altura - 20) / max_valor)
            canvas.create_line(x, y, x, y - height, fill="black")
        canvas.pack()

    def ajustar_contraste(self, imagen_canal, factor_contraste):
        return imagen_canal.point(lambda x: 128 + factor_contraste * (x - 128))

    def modificar_imagen(self, *args):
        if self.imagen_original is not None:
            factor_contraste_r = self.scale_r.get()
            factor_contraste_g = self.scale_g.get()
            factor_contraste_b = self.scale_b.get()

            imagen_modificada = self.imagen_original.copy()
            r, g, b = imagen_modificada.split()

            r = self.ajustar_contraste(r, factor_contraste_r)
            g = self.ajustar_contraste(g, factor_contraste_g)
            b = self.ajustar_contraste(b, factor_contraste_b)

            imagen_modificada = Image.merge("RGB", (r, g, b))
            imagen_modificada.thumbnail((400, 400))
            imagen_tk = ImageTk.PhotoImage(imagen_modificada)

            self.frame_imagen_modificada.configure(image=imagen_tk)
            self.frame_imagen_modificada.image = imagen_tk

            self.mostrar_imagenes_rgb(r, g, b)
            self.generar_histogramas(imagen_modificada)
        else:
            print("Por favor, carga una imagen.")

    def mostrar_imagenes_rgb(self, imagen_r, imagen_g, imagen_b):
        imagen_r.thumbnail(self.tamaño_miniatura_canal)
        imagen_g.thumbnail(self.tamaño_miniatura_canal)
        imagen_b.thumbnail(self.tamaño_miniatura_canal)

        imagen_tk_r = ImageTk.PhotoImage(imagen_r)
        imagen_tk_g = ImageTk.PhotoImage(imagen_g)
        imagen_tk_b = ImageTk.PhotoImage(imagen_b)

        self.label_imagen_r.configure(image=imagen_tk_r)
        self.label_imagen_g.configure(image=imagen_tk_g)
        self.label_imagen_b.configure(image=imagen_tk_b)

        self.label_imagen_r.image = imagen_tk_r
        self.label_imagen_g.image = imagen_tk_g
        self.label_imagen_b.image = imagen_tk_b

    def establecer_sliders_a_uno(self):
        self.scale_r.set(1.0)
        self.scale_g.set(1.0)
        self.scale_b.set(1.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
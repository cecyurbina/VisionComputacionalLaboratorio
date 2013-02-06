#!/usr/bin/python
#import Tkinter
#import time

from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import sys

class Aplicacion:
    """clase que dibuja los botones
    """
    def __init__(self, master, imagen_path):
        self.nombre_imagen = imagen_path
        self.imagen_original = self.abrir_imagen_original()
        self.imagen_actual = self.imagen_original
        self.x, self.y = self.imagen_original.size
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        #se posicionan los botones
        self.gris = Button(self.frame, text="gris", fg="blue",
                           command=self.hacer_gris)
        self.umbral = Button(self.frame, text="umbral", fg="blue",
                             command=self.umbral)
        self.invertido = Button(self.frame, text="invertir", fg="blue",
                                command=self.invertir)
        self.promedio = Button(self.frame, text="promedio", fg="blue",
                               command=self.hacer_difusa)
        self.espejo = Button(self.frame, text="espejo", fg="blue",
                            command=self.espejo)
        self.reset = Button(self.frame, text="reset", fg="blue",
                            command=self.reiniciar)
        self.guarda = Button(self.frame, text="guardar", fg="blue",
                            command=self.guardar)
        self.gris.grid(row=0, column=0,padx=15, pady=15)
        self.umbral.grid(row=0, column=1,padx=15, pady=15)
        self.invertido.grid(row=0, column=2,padx=15, pady=15)
        self.promedio.grid(row=0, column=3,padx=15, pady=15)
        self.espejo.grid(row=0, column=4,padx=15, pady=15)
        self.reset.grid(row=0, column=5,padx=15, pady=15)
        self.guarda.grid(row=0, column=6,padx=15, pady=15)
        #se abre la imagen                     
        foto = Image.open(imagen_path)
        foto = ImageTk.PhotoImage(foto)
        self.picture = Label(self.frame, image=foto)
        self.picture.image = foto
        self.picture.grid(row=1, column=0, columnspan=7,sticky=W+E+N+S, padx=5, pady=5)

    def abrir_imagen_original(self):
        """funcion que se manda llamar para
        poder usar la imagen que se selecciono
        al inicio
        """
        imagen = Image.open(self.nombre_imagen)
        imagen = imagen.convert('RGB')
        return imagen

    def reiniciar(self):
        """
        funcion que regresa la foto al estado inicial
        """
        self.imagen_actual = self.imagen_original
        self.actualizar_imagen()
    
    def guardar(self):
        """guarda la imagen con el nombre
        imagen_nueva.png
        """
        self.imagen_actual.save("imagen_nueva.png")

    def actualizar_imagen(self):
        """redibuja la foto en la ventana
        """
        foto  = ImageTk.PhotoImage(self.imagen_actual)
        self.picture = Label(self.frame, image=foto)
        self.picture.image = foto
        self.picture.grid(row=1, column=0, columnspan=7,sticky=W+E+N+S, padx=5, pady=5)        

    def espejo(self):
        """cambia el sentido de la imagen
        """
        imagen_espejo = Image.new("RGB", (self.x, self.y))
        pixeles = []
        for a in range(self.y):
            renglon = []
            for b in range(self.x):
                pixel = self.imagen_actual.getpixel((b, a))[0]
                data = (pixel, pixel, pixel)
                renglon.append(data)
            renglon.reverse()
            pixeles = pixeles + renglon
        imagen_espejo.putdata(pixeles)
        #se actualiza la imagen actual y se redibuja
        self.imagen_actual = imagen_espejo
        self.actualizar_imagen()
        return imagen_espejo

    def hacer_gris(self):
        """pone la foto en escala de grises
        toma el valor maximo del rgb de cada pixel
        """
        imagen_gris = Image.new("RGB", (self.x, self.y))
        pixeles = []
        for a in range(self.y):
            for b in range(self.x):
                r, g, b = self.imagen_actual.getpixel((b, a))
                rgb = (r, g, b)
                #se elige el valor mas grande
                maximo = max(rgb)
                data = (maximo, maximo, maximo)
                pixeles.append(data)
        imagen_gris.putdata(pixeles)
        #se actualiza la imagen actual y se redibuja
        self.imagen_actual = imagen_gris
        self.actualizar_imagen()
        return imagen_gris

    def umbral(self):
        """binariza la imagen si el valor del pixel es de color menor a 
        150 se pone 0 en el pixel, si es mayo se pone 255 en el pixel
        """
        imagen_umbral = Image.new("RGB", (self.x, self.y))
        pixeles = []
        for a in range(self.y):
            for b in range(self.x):
                color = self.imagen_actual.getpixel((b,a))[0]
                if color > 150:
                    color = 255
                else:
                    color = 0
                data = (color, color, color)
                pixeles.append(data)
        imagen_umbral.putdata(pixeles)
        self.imagen_actual = imagen_umbral
        self.actualizar_imagen()
        return imagen_umbral

    def invertir(self):
        """cambia los colores de la imagen a su contrario
        restando 255 a cada pixel
        """
        imagen_invertida = Image.new("RGB", (self.x, self.y))
        pixeles = []
        for a in range(self.y):
            for b in range(self.x):
                color = self.imagen_actual.getpixel((b,a))[0]
                color = 255 - color
                data = (color, color, color)
                pixeles.append(data)
        imagen_invertida.putdata(pixeles)
        #se actualiza la imagen actual y se redibuja
        self.imagen_actual = imagen_invertida
        self.actualizar_imagen()
        return imagen_invertida

    def hacer_difusa(self):
        """funcion que se encarga de tomar de cada pixel los pixeles 
        de izq, derecha, arriba, abajo y el mismo y los promedia, y ese
        promedio es el valor de los nuevos pixeles
        """
        imagen_difusa = Image.new("RGB", (self.x, self.y))
        pixeles = []
        #temp sirve para obtener el promedio de los
        #pixeles contiguos 
        temp = []
        for a in range(self.y):
            for b in range(self.x):
                actual = self.imagen_actual.getpixel((b, a))[0]
                if b>0 and b<(self.x-1) and a>0 and a<(self.y-1):
                    #en esta condicion entran todos los pixeles que no estan
                    #en el margen de la imagen, es decir casi todos
                    pix_izq = self.imagen_actual.getpixel((b-1, a))[0]
                    pix_der = self.imagen_actual.getpixel((b+1, a))[0]
                    pix_arriba = self.imagen_actual.getpixel((b, a+1))[0]
                    pix_abajo = self.imagen_actual.getpixel((b, a-1))[0]
                    temp.append(pix_izq)
                    temp.append(pix_der)
                    temp.append(pix_arriba)
                    temp.append(pix_abajo)
                else:
                    #aqui entran todos los pixeles de la orilla
                    try:
                        pix_abajo = self.imagen_actual.getpixel((b, a-1))[0]
                        temp.append(pix_abajo)
                    except:
                        pass
                    try:
                        pix_der = self.imagen_actual.getpixel((b+1, a))[0]
                        temp.append(pix_der)
                    except:
                        pass
                    try:                
                        pix_izq = self.imagen_actual.getpixel((b-1, a))[0]
                        temp.append(pix_izq)
                    except:
                        pass
                    try:
                        pix_arriba = self.imagen_actual.getpixel((b, a+1))[0]
                        temp.append(pix_arriba)
                    except:
                        pass
                temp.append(actual)
                #se obtiene el promedio para cambiar el pixel
                prom = sum(temp)/len(temp)
                temp = []
                pixeles.append((prom, prom, prom))
        imagen_difusa.putdata(pixeles)
        #se actualiza la imagen actual y se redibuja
        self.imagen_actual = imagen_difusa
        self.actualizar_imagen()
        return imagen_difusa

def main():
    """funcion principal
    """
    try:
        imagen_path = sys.argv[1]
        print imagen_path
    except:
        print "No seleccionaste una imagen"
        return
    root = Tk()
    App = Aplicacion(root, imagen_path)
    root.title("Imagenes")
    root.mainloop()

if __name__ == "__main__":
    main()

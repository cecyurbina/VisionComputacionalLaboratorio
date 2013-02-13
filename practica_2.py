#!/usr/bin/python
#import Tkinter
#import time
from Tkinter import *
from PIL import Image, ImageTk
from math import floor
import sys
import filtros
import random

class Aplicacion:
    """clase que dibuja los botones
    """
    def __init__(self, master, imagen_path):
        self.nombre_imagen = imagen_path
        self.imagen_original = filtros.abrir_imagen(self.nombre_imagen)
        self.imagen_actual = filtros.hacer_gris(self.imagen_original)
        self.x, self.y = self.imagen_original.size
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        #se posicionan los botones
        self.sal_pim = Button(self.frame, text="Sal y pimienta", fg="blue", command=self.sal_pimienta)
        self.limpia = Button(self.frame, text="limpia", fg="blue", command=self.limpiar)
        self.diferencia = Button(self.frame, text="diferencia", fg="blue", command=self.diferencia)
        self.normaliza = Button(self.frame, text="normaliza", fg="blue", command=self.normalizar)
        self.reset = Button(self.frame, text="reset", fg="blue", command=self.reiniciar)
        self.guarda = Button(self.frame, text="guardar", fg="blue", command=self.guardar)
        self.sal_pim.grid(row=0, column=0,padx=15, pady=15)
        self.limpia.grid(row=0, column=1,padx=15, pady=15)
        self.diferencia.grid(row=0, column=2,padx=15, pady=15)
        self.normaliza.grid(row=0, column=3,padx=15, pady=15)
        self.reset.grid(row=0, column=4,padx=15, pady=15)
        self.guarda.grid(row=0, column=5,padx=15, pady=15)
        #se abre la imagen                     
        foto = Image.open(imagen_path)
        foto = ImageTk.PhotoImage(foto)
        self.picture = Label(self.frame, image=foto)
        self.picture.image = foto
        self.picture.grid(row=1, column=0, columnspan=6,sticky=W+E+N+S, padx=5, pady=5)

    def sal_pimienta(self):
        """agrega ruido a la imagen con pixeles blancos y negros
        en posiciones aleatorias
        """
        imagen_perturbada = Image.new("RGB", (self.x,self.y))
        total_pixeles = self.x * self.y
        pixeles_cambiar = total_pixeles/60
        pixeles_perturbados = []
        for i in xrange(pixeles_cambiar):
            elegido = random.randint(0, total_pixeles-1)
            pixeles_perturbados.append(elegido)
        pixeles = []
        contador = 0
        for a in xrange(self.y):
            for b in xrange(self.x):
                color = self.imagen_actual.getpixel((b,a))[0]
                if contador in pixeles_perturbados:
                    nuevo_color = random.randint(0,1)
                    color = 255 if nuevo_color == 0 else 0
                contador = contador + 1
                data = (color, color, color)
                pixeles.append(data)
        imagen_perturbada.putdata(pixeles)
        imagen_perturbada.save("imagen_perturbada.png")
        self.imagen_actual = imagen_perturbada
        self.actualizar_imagen()
        return imagen_perturbada

    def limpiar(self):
        """elimina sal y pimienta
        """
        temp = []
        pixeles = []
        imagen_limpia = Image.new("RGB", (self.x,self.y))
        for a in xrange(self.y):
            for b in xrange(self.x):
                color = self.imagen_actual.getpixel((b,a))[0]
                if color == 255 or color == 0:
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
                    temp.sort()
                    if len(temp) % 2 == 0:
                        n = len(temp)                                                   
                        mediana = (temp[n/2-1]+ temp[n/2] )/2                 
                    else:
                        mediana =temp[len(temp)/2]
                    temp = []
                    color = mediana
                data = (color, color, color)
                pixeles.append(data)
        imagen_limpia.putdata(pixeles)
        imagen_limpia.save("imagen_limpia.png")
        self.imagen_actual = imagen_limpia
        self.actualizar_imagen()
        return imagen_limpia

    def diferencia(self):
        """resta los pixeles de la imagen gris a una imagen gris que se
        le haya aplicado el filtro del promedio
        """
        imagen_nueva = Image.new("RGB", (self.x, self.y))
        difusa = filtros.hacer_difusa(self.imagen_original)
        pixeles = []
        for a in range(self.y):
            for b in range(self.x):
                dif = self.imagen_original.getpixel((b, a))[0] - difusa.getpixel((b, a))[0]
                if dif > 255:
                    dif = 255
                if dif < 0:
                    dif = 0
                pixeles.append((dif, dif, dif))
        imagen_nueva.putdata(pixeles)
        imagen_nueva.save("diferencia.png")
        self.imagen_actual = imagen_nueva
        self.actualizar_imagen()
        return imagen_nueva

    def normalizar(self):
        imagen_normalizada = Image.new("RGB", (self.x, self.y))
        imagen_normalizada = filtros.normalizar(self.imagen_actual)
        imagen_normalizada.save("normalizada.png")
        self.imagen_actual = imagen_normalizada
        self.actualizar_imagen()
        return imagen_normalizada
                                          
    def actualizar_imagen(self):
        """redibuja la foto en la ventana
        """
        foto  = ImageTk.PhotoImage(self.imagen_actual)
        self.picture = Label(self.frame, image=foto)
        self.picture.image = foto
        self.picture.grid(row=1, column=0, columnspan=6,sticky=W+E+N+S, padx=5, pady=5)

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



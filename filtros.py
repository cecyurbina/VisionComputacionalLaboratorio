#!/usr/bin/python
from PIL import Image, ImageTk
import math
import sys

def abrir_imagen(nombre_imagen):
    """
    """
    imagen = Image.open(nombre_imagen)
    imagen = imagen.convert('RGB')
    return imagen

def convolucion(imagen_original, mascara):
    """
    """
    x, y = imagen_original.size
    pos = imagen_original.load()
    nueva_imagen = Image.new("RGB", (x,y))
    pos_nueva = nueva_imagen.load() 
    for i in range(x):
        for j in range(y):
            total = 0
            for n in range(i-1, i+2):
                for m in range(j-1, j+2):
                    if n >= 0 and m >= 0 and n < x and m < y:
                        total += mascara[n - (i - 1)][ m - (j - 1)] * pos[n, m][0]
            pos_nueva[i, j] = (total, total, total)
    nueva_imagen.save("mascara.png")
    return nueva_imagen

def umbral(imagen_original):
    """
    """
    x, y = imagen_original.size
    imagen_umbral = Image.new("RGB", (x, y))
    pixeles = []
    for a in range(y):
        for b in range(x):
            color = imagen_original.getpixel((b,a))[0]
            if color > 80:
                color = 255
            else:
                color = 0
            data = (color, color, color)
            pixeles.append(data)
    imagen_umbral.putdata(pixeles)
    imagen_umbral.save("imagen_umbral.png", quality=100)
    return imagen_umbral

def normalizar(imagen_original):
    """
    """
    x, y = imagen_original.size
    imagen_normalizada = Image.new("RGB", (x, y))
    pixeles = []
    for a in range(y):
        for b in range(x):
            pix = imagen_original.getpixel((b, a))[0]
            pixeles.append(pix)
    maximo = max(pixeles) 
    minimo = min(pixeles)
    print maximo
    print minimo
    l = 256.0/(maximo - minimo)
    pixeles = []
    for a in range(y):
        for b in range(x):
            pix = imagen_original.getpixel((b, a))[0]
            nuevo_pix = int(math.floor((pix-minimo)*l))
            pixeles.append((nuevo_pix, nuevo_pix, nuevo_pix))
    imagen_normalizada.putdata(pixeles)
    imagen_normalizada.save("imagen_normalizada.png")
    return imagen_normalizada

def hacer_difusa(imagen_original):
    """funcion que se encarga de tomar de cada pixel los pixeles 
    de izq, derecha, arriba, abajo y el mismo y los promedia, y ese
    promedio es el valor de los nuevos pixeles
    """
    x, y = imagen_original.size
    imagen_difusa = Image.new("RGB", (x, y))
    pixeles = []
    #temp sirve para obtener el promedio de los
    #pixeles contiguos 
    temp = []
    for a in range(y):
        for b in range(x):
            actual = imagen_original.getpixel((b, a))[0]
            if b>0 and b<(x-1) and a>0 and a<(y-1):
                    #en esta condicion entran todos los pixeles que no estan
                    #en el margen de la imagen, es decir casi todos
                pix_izq = imagen_original.getpixel((b-1, a))[0]
                pix_der = imagen_original.getpixel((b+1, a))[0]
                pix_arriba = imagen_original.getpixel((b, a+1))[0]
                pix_abajo = imagen_original.getpixel((b, a-1))[0]
                temp.append(pix_izq)
                temp.append(pix_der)
                temp.append(pix_arriba)
                temp.append(pix_abajo)
            else:
                #aqui entran todos los pixeles de la orilla
                try:
                    pix_abajo = imagen_original.getpixel((b, a-1))[0]
                    temp.append(pix_abajo)
                except:
                    pass
                try:
                    pix_der = imagen_original.getpixel((b+1, a))[0]
                    temp.append(pix_der)
                except:
                    pass
                try:                
                    pix_izq = imagen_original.getpixel((b-1, a))[0]
                    temp.append(pix_izq)
                except:
                    pass
                try:
                    pix_arriba = imagen_original.getpixel((b, a+1))[0]
                    temp.append(pix_arriba)
                except:
                    pass
            temp.append(actual)
                #se obtiene el promedio para cambiar el pixel
            prom = sum(temp)/len(temp)
            temp = []
            pixeles.append((prom, prom, prom))
    imagen_difusa.putdata(pixeles)
    imagen_difusa.save("imagen_difusa.png")
    return imagen_difusa

def hacer_gris(imagen_original):
    """pone la foto en escala de grises
    toma el valor maximo del rgb de cada pixel
    """
    x, y = imagen_original.size
    imagen_gris = Image.new("RGB", (x,y))
    pixeles = []
    for a in range(y):
        for b in range(x):
            r, g, b = imagen_original.getpixel((b, a))
            rgb = (r, g, b)
                #se elige el valor mas grande
            maximo = max(rgb)
            data = (maximo, maximo, maximo)
            pixeles.append(data)
    imagen_gris.putdata(pixeles)
    imagen_gris.save("imagen_gris.png")
    return imagen_gris

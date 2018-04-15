#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conecta4.py.py
------------

El juego de conecta 4

Este juego contiene una parte de la tarea 5, y otra parte
es la implementación desde 0 del juego de Otello.

"""
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from random import shuffle
import tkinter as tk

__author__ = 'juliowaissman'

class ConectaCuatro(JuegoSumaCeros2T):
    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:

                        35  36  37  38  39  40  41
                        28  29  30  31  32  33  34
                        21  22  23  24  25  26  27
                        14  15  16  17  18  19  20
                         7   8   9  10  11  12  13
                         0   1   2   3   4   5   6
        """
        super().__init__(tuple([0 for _ in range(6 * 7)]))

    def jugadas_legales(self):
        """
        Las jugadas legales son las columnas donde se puede
        poner una ficha (0, ..., 6), si no está llena.
        """
        return (j for j in range(7) if self.x[35 + j] == 0)

    def terminal(self):
        x = self.x
        # Primero checamos filas y diagonales
        if any((xj != 0 for xj in x[21:28])):
            # Filas
            for i in range(7):
                if x[i + 21] == 0 or x[i + 14] != x[i + 21]:
                    continue
                if ((x[i] == x[i + 7] == x[i + 14]) or
                    (x[i + 7] == x[i + 14] == x[i + 28]) or
                    (x[i + 14] == x[i + 28] == x[i + 35])):
                    return x[i + 14]
            # Diagonales
            for j in (0, 7, 14):
                for i in (0, 1, 2, 3):
                    # Hacia arriba
                    if (x[i + j + 24] != 0 and
                        x[i + j + 24] == x[i + j + 16] and
                        x[i + j + 16] == x[i + j + 8] and
                        x[i + j + 8] == x[i + j]):
                        return x[i + j]
                    # Hacia abajo
                    if (x[i + j + 21] != 0 and
                        x[i + j + 21] == x[i + j + 15] and
                        x[i + j + 15] == x[i + j + 9] and
                        x[i + j + 9] == x[i + j + 3]):
                        return x[i + j + 3]
        # Ahora checamos renglones
        for i in range(0, 41, 7):
            if x[i + 3] == 0:
                break
            for j in range(4):
                if (x[i + j] == x[i + j + 1] == x[i + j + 2] == x[i + j + 3]):
                    return x[i + 3]
        # Ahora checamos si no se lleno el tabero
        if 0 not in x:
            return 0
        return None

    def hacer_jugada(self, jugada):
        for i in range(0, 41, 7):
            if self.x[i + jugada] == 0:
                self.x[i + jugada] = self.jugador
                self.historial.append(jugada)
                self.jugador *= -1
                return None

    def deshacer_jugada(self):
        pos = self.historial.pop()
        for i in (35, 28, 21, 14, 7, 0):
            if self.x[i + pos] != 0:
                self.x[i + pos] = 0
                self.jugador *= -1
                return None


def utilidad_c4(x):
    """
    Calcula la utilidad de una posición del juego conecta 4
    para el jugador max (las fichas rojas, o el que empieza)

    @param x: Una lista con el estado del tablero

    @return: Un número entre -1 y 1 con la ganancia esperada

    Para probar solo busque el número de conecciones de las
    bolitas de mas arriba con su alrededor
    """
    cum = 0
    for i in range(7):
        for j in (35, 28, 21, 14, 7, 0):
            if x[i] != 0:
                if 0 < i < 6:
                    biases = (-6, -7, -8, -1, 1, 6, 8)
                elif i == 0:
                    biases = (-7, -8, 1, 8)
                else:
                    biases = (-6, -7, -1, 6)
                con = sum(x[i] for bias in biases
                            if i + bias >= 0 and x[i] == x[i + bias])
                cum += con / len(biases)
                break

    return cum / 42

def utilidad_c4_2(x):
    """
    Calcula la utilidad de una posición del juego conecta 4
    para el jugador max (las fichas rojas, o el que empieza)

    @param x: Una lista con el estado del tablero

    @return: Un número con la ganancia esperada
    """
    utilidad = 0
    # horizontales
    for i in range(0, 36, 7):
        # checa areas de 4 casillas si hay 3 de algun jugador
        for j in range(4):
            area = x[j:j+4]
            suma = sum(area) 
            if sum in (3, -3) and 0 in area:
                if suma == 3:
                    return 1
                else:
                    utilidad = -1               
    # verticales
    for i in range(7):
        # checa si hay 3 de algun jugador y el siguiente no hay nada
        for j in range(3):
            indice = i+7*j
            if x[indice] != 0 and x[indice] == x[indice+7] == x[indice+14] and x[indice+21] == 0:
                if suma == 3:
                    return 1
                else:
                    utilidad = -1
    # diagonales derechas
    for i in range(4):
        # si no hay vacios en el rango no se revisa
        if 0 not in x[i:i+4]:
            for j in range(0, 15, 7):
                indice = i+j
                area = ( x[indice+k] for k in range(0, 25, 8) ) # area de la diagonal
                suma = sum( area )
                if suma in (3, -3) and 0 in area:
                    indice_cero = indice + area.index(0) * 8
                    # si abajo de donde se puede ganar no hay nada, pues no se gana xd
                    if (indice_cero > 7 and x[indice_cero-7] == 0):
                        continue
                    if suma == 3:
                        return 1
                    else:
                        utilidad = -1
    # diagonales izquierdas
    for i in range(2, 7):
        # si no hay vacios en el rango no se revisa
        if 0 not in x[i:i+4]:
            for j in range(0, 15, 7):
                indice = i+j
                area = ( x[indice+k] for k in range(0, 19, 6) ) # area de la diagonal
                suma = sum( area )
                if suma in (3, -3) and 0 in area:
                    indice_cero = indice + area.index(0) * 6
                    # si abajo de donde se puede ganar no hay nada, pues no se gana xd
                    if (indice_cero > 7 and x[indice_cero-7] == 0):
                        continue
                    return 1 if suma == 3 else -1
                            
    return utilidad

def ordena_jugadas(juego):
    """
    Ordena las jugadas de acuerdo al jugador actual, en función
    de las más prometedoras.

    Para que funcione le puse simplemente las jugadas aleatorias
    pero es un criterio bastante inaceptable

    """
    jugadas = list(juego.jugadas_legales())
    shuffle(jugadas)
    return jugadas

def ordena_jugadas_2(juego):
    """
    Ordena las jugadas de acuerdo al jugador actual, en función
    de las más prometedoras.

    Devuelve primero las jugadas del centro, ya que son las que pueden
    generar mas conexiones
    """
    jugadas = list(juego.jugadas_legales())
    jugadas_ordenadas = []
    for jugada in jugadas:
        if 5 > jugada > 1:
            jugadas_ordenadas.insert(0, jugada)
        else:
            jugadas_ordenadas.append(jugada) 

    return jugadas_ordenadas

class Conecta4GUI:
    def __init__(self, tmax=10, escala=1):

        # La tabla de transposición
        self.tr_ta = {}

        # Máximo tiempo de búsqueda
        self.tmax = tmax

        self.app = app = tk.Tk()
        self.app.title("Conecta Cuatro")
        self.L = L = int(escala) * 50

        tmpstr = "Escoge color, rojas empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=7*L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonR = tk.Button(barra, command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con rojas', width=22)
        botonR.grid(column=0, row=0)
        botonN = tk.Button(barra, command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con negras', width=22)
        botonN.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()

        self.sel_j = tk.IntVar(self.anuncio.master, -1, 'sel_j')

        def boton_f(fila):
            self.sel_j.set(fila)

        self.flecha = tk.PhotoImage(file='flecha2.gif')
        self.botones = [None for _ in range(7)]
        for i in range(7):
            self.botones[i] = tk.Button(ctn, image=self.flecha,
                                        command=lambda fila=i: boton_f(fila),
                                        width=L, height=L,
                                        state=tk.DISABLED)
            self.botones[i].grid(column=i, row=0)

        self.can = [None for _ in range(6 * 7)]
        self.cuadritos = [None for _ in range(6 * 7)]
        for i in range(6 * 7):
            self.can[i] = tk.Canvas(ctn, height=L, width=L,
                                    bg='light grey', borderwidth=0)
            self.can[i].grid(row=((41 - i) // 7) + 1, column=i % 7)
            self.cuadritos[i] = self.can[i].create_oval(5, 5, L, L,
                                                        fill='white', width=2)
            self.can[i].val = 0

    def jugar(self, primero):

        juego = ConectaCuatro()

        for i in range(42):
            if self.can[i].val != 0:
                self.can[i].itemconfigure(self.cuadritos[i], fill='white')
                self.can[i].val = 0
        color, color_p = 'red', 'black'

        if not primero:
            color, color_p = 'black', 'red'
            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            for i in range(7):
                self.botones[i]['state'] = tk.DISABLED

            jugada = minimax(juego, dmax=6, utilidad=utilidad_c4_2,
                             ordena_jugadas=ordena_jugadas_2,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color_p)

        for _ in range(43):
            self.anuncio['text'] = "Te toca jugar"
            self.anuncio.update()
            for i in juego.jugadas_legales():
                self.botones[i]['state'] = tk.NORMAL

            self.anuncio.master.wait_variable('sel_j')
            jugada = self.sel_j.get()
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color)

            ganancia = juego.terminal()
            if ganancia is not None:
                break

            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            for i in range(7):
                self.botones[i]['state'] = tk.DISABLED
                self.botones[i].update()

            jugada = minimax(juego, dmax=6, utilidad=utilidad_c4_2,
                             ordena_jugadas=ordena_jugadas_2,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color_p)

            ganancia = juego.terminal()
            if ganancia is not None:
                break

        for i in range(7):
            self.botones[i]['state'] = tk.DISABLED

        str_fin = ("Ganaron las rojas" if ganancia > 0 else
                   "Ganaron las negars" if ganancia < 0 else
                   "Un asqueroso empate")
        self.anuncio['text'] = str_fin

    def actualiza_tablero(self, fila, color):
        for i in range(0, 41, 7):
            if self.can[i + fila].val == 0:
                self.can[i + fila].itemconfigure(self.cuadritos[i + fila],
                                                 fill=color)
                self.can[i + fila].val = 1 if color is 'red' else -1
                self.can[i + fila].update()
                break

    def arranca(self):
        self.app.mainloop()

if __name__ == '__main__':
    Conecta4GUI(tmax=10).arranca()

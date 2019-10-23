#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Xavier Paredes'

# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from random import shuffle
import tkinter as tk
from collections import deque

class Othello:
    def __init__(self):
        """
        00 01 02 03 04 05 06 07
        08 09 10 11 12 13 14 15
        16 17 18 19 20 21 22 23
        24 25 26 27 28 29 30 31
        32 33 34 35 36 37 38 39
        40 41 42 43 44 45 46 47
        48 49 50 51 52 53 54 55
        56 57 58 59 60 61 62 63
        """
        self.x = [0 for _ in range(64)]
        self.jugador = 1
        self.x[27], self.x[36] = -1, -1
        self.x[28], self.x[35] = 1, 1
        self.historial = deque()

    #Busco si hay adyacente enemigo en una posicion pos para el jugador j.
    #Pienso que esto hara las cosas mucho mas rapidas en los primeros turnos.
    @staticmethod
    def adyacentes(x, pos, j):
        # El jugador de interes es el adversario
        j = -1 * j
        orilla_izq = [8 * x for x in range(8)]
        orilla_der = [8 * x -1 for x in range(1,9)]
        orilla_sup = [i for i in range(8)]
        orilla_inf = [i for i in range(56,64)]
        direcciones = []

        #Este primer if lo agregue porque cuando no esta en las orillas
        #(que es la mayoria de los casos) no busque uno por uno las demas
        # orillas
        if pos not in (orilla_der + orilla_inf + orilla_izq + orilla_sup):
            for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
                if x[pos + i] == j:
                    direcciones.append(i)
            return direcciones

        if pos not in orilla_izq:
            if x[pos - 1] == j:
                direcciones.append(- 1)
        if pos not in orilla_der:
            if x[pos + 1] == j:
                direcciones.append(1)
        if pos not in orilla_sup:
            if x[pos - 8] == j:
                direcciones.append(-8)
        if pos not in orilla_inf:
            if x[pos + 8] == j:
                direcciones.append(8)
        if pos not in (orilla_inf + orilla_der):
            if x[pos + 9] == j:
                direcciones.append(9)
        if pos not in (orilla_inf + orilla_izq):
            if x[pos + 7] == j:
                direcciones.append(7)
        if pos not in (orilla_sup + orilla_der):
            if x[pos - 7] == j:
                direcciones.append(-7)
        if pos not in (orilla_sup + orilla_izq):
            if x[pos - 9] == j:
                direcciones.append(-9)
        return direcciones

    def jugadas_legales(self):
        jugadas = []
        for i in range(64):
            ady = self.adyacentes(self.x, i, self.jugador)
            if (self.x[i] == 0 and len(ady) != 0):
                if len(self.buscar_lugar(i, ady)) != 0:
                    jugadas.append(i)
        return jugadas

    def hacer_jugada(self, jugada):
        self.historial.append(self.x[:])
        for x in self.buscar_lugar(jugada, self.adyacentes(self.x, jugada, self.jugador)):
            aux = x + jugada
            while self.x[aux] == -1 * self.jugador:
                self.x[aux] = self.jugador
                aux+=x
        self.x[jugada] = self.jugador
        self.jugador *= -1

    def deshacer_jugada(self):
        self.x = self.historial.pop()
        self.jugador *= -1

    """
    Buscar lugar es un metodo que apartir de cierta jugada regresara
    las direcciones en las que se encuentran fichas capturables
    @param jugada: la jugada de interes. es un entero
    @param direcciones: lista con las direcciones en las que se encuentran
    fichas adyacentes del enemigo. en funcion a estas buscamos si podemos
    capturar en esa direccion
    @return captura: una lista con todas las direcciones en las que si se puede
    hacer la captura.
    """
    def buscar_lugar(self, jugada, direcciones):
        captura = []
        orilla_izq = [8 * x for x in range(8)]
        orilla_der = [8 * x -1 for x in range(1,9)]
        orilla_sup = [i for i in range(8)]
        orilla_inf = [i for i in range(56,64)]
        for x in direcciones:
            aux = jugada + x
            while aux < 64 and aux >= 0 and self.x[aux] == -1 * self.jugador:
                if x in [-9, -1, 7] and aux not in orilla_izq:
                    aux+= x
                elif x in [9, 1, -7] and aux not in orilla_der:
                    aux+= x
                elif x in [8, -8]:
                    aux+=x
                else:
                    break
            if aux < 64 and aux >= 0 and self.x[aux] == self.jugador:
                captura.append(x)
        return captura


    def terminal(self):
        if len(self.jugadas_legales()) == 0:
            self.jugador = self.jugador * -1
            if len(self.jugadas_legales()) == 0:
                if sum(1 for i in self.x if i==1) > sum(1 for i in self.x if i == -1):
                    return 1
                else:
                    return -1
            self.jugador = -1 * self.jugador

def orillas(x):
    or_sup = 0
    or_inf = 0
    or_iz = 0
    or_der = 0
    for i in range(1,7):
        or_iz += x[8*i]
        or_sup += x[i]
    for i in range(2,8):
        or_der += x[8 * i -1]
    for i in range(57,63):
        or_inf += x[i]

    if x[0] != 0:
        or_sup += 2*x[0]
        or_iz += 2*x[0]
    if x[7] != 0:
        or_sup += 2*x[7]
        or_der += 2*x[7]
    if x[56] != 0:
        or_inf += 2*x[56]
        or_iz += 2*x[56]
    if x[63] != 0:
        or_inf += 2*x[63]
        or_der += 2*x[63]

    return or_der + or_iz + or_sup + or_inf

def utilidad_ot(juego):
    #quien tiene mas fichas?
    x = juego.x
    p1 = sum(1 for i in x if x[i] == 1) + sum(-1 for i in x if x[i] == -1)
    #quien tiene mas en las orillas?
    p2 = orillas(x)
    return p1 + p2

class OthelloTK:
    def __init__(self, escala=1):

        self.app = app = tk.Tk()
        self.app.title("Othello")
        self.L = L = int(escala) * 50

        tmpstr = "Escoge, negras empiezan."
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=3 * L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonX = tk.Button(barra,
                           command=lambda x=1: self.jugar(x),
                           text='(re)iniciar con Negras')
        botonX.grid(column=0, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=-1: self.jugar(x),
                           text='(re)iniciar con Blancas')
        botonO.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.9 * L), 'bold')

        tablero = tk.Frame(ctn, bg='black', borderwidth=0)
        tablero.grid(row=0, column=0)

        negro = True
        for ind in range(64):
            if negro :
                self.tablero[ind] = tk.Canvas(
                    tablero, height=L, width=L,
                    bg='dark green', borderwidth=0
                )
            else:
                self.tablero[ind] = tk.Canvas(
                    tablero, height=L, width=L,
                    bg='pale green', borderwidth=0
                )
            self.tablero[ind].grid(row=ind//8, column=ind % 8)
            self.textos[ind] = self.tablero[ind].create_text(
                L // 2, L // 2, font=letra, text=' '
            )
            self.tablero[ind].val = 0
            self.tablero[ind].pos = ind
            if ind in [7,15,23,31,39,47,55]:
                continue
            negro = not negro

    def jugar(self, primero):
        juego = Othello()
        self.actualiza_tablero(juego.x)
        self.anuncio['text'] = "A ver de que cuero salen más correas"
        while juego.terminal() is None:
            self.actualiza_tablero(juego.x)
            if len(juego.jugadas_legales()) != 0:
                if juego.jugador == primero:
                    jugada = self.escoge_jugada(juego)
                else:
                    #Con dmax = 2 me metio una putiza a mi y a la ia
                    # de othelloonline.org, lo dejo 49-0 lol
                    # pero si te consideras pro y te gustan los retos, subele
                    # a dmax 3
                    jugada = minimax(juego, dmax=2, utilidad=utilidad_ot)

                juego.hacer_jugada(jugada)
            else:
                juego.jugador *= -1
        self.actualiza_tablero(juego.x)
        u = juego.terminal()
        if u == 0:
            fin = "UN ASQUEROSO EMPATE"
        elif (primero < 0 and u > 0) or (primero > 0 and u < 0):
            fin ="¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?"
        else:
            fin ="Ganaste, bye."

        self.anuncio['text'] = fin
        self.anuncio.update()

    def escoge_jugada(self, juego):
        jugadas_posibles = juego.jugadas_legales()
        if len(jugadas_posibles) == 1:
            return jugadas_posibles[0]

        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')

        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'grey'

        def salida(evento):
            evento.widget['bg'] = evento.widget.color_original

        def presiona_raton(evento):
            evento.widget['bg'] = evento.widget.color_original
            seleccion.set(evento.widget.pos)

        for i in jugadas_posibles:
            self.tablero[i].bind('<Enter>', entrada)
            self.tablero[i].bind('<Leave>', salida)
            self.tablero[i].bind('<Button-1>', presiona_raton)

        self.tablero[0].master.wait_variable('seleccion')

        for i in jugadas_posibles:
            self.tablero[i].unbind('<Enter>')
            self.tablero[i].unbind('<Leave>')
            self.tablero[i].unbind('<Button-1>')
        return seleccion.get()

    def actualiza_tablero(self, x):
        for i in range(64):
            if self.tablero[i].val != x[i] and x[i] == -1:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text='\u26AB', fill = "white")
                self.tablero[i].val = -1
                self.tablero[i].update()
            elif self.tablero[i].val != x[i] and x[i] == 1:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text='\u26AB', fill = "black")
                self.tablero[i].val = 1
                self.tablero[i].update()

            elif self.tablero[i].val != x[i] and x[i] == 0:
                self.tablero[i].itemconfigure(self.textos[i], text=' ')
                self.tablero[i].val = 0
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    OthelloTK().arranca()
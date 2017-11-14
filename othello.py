#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
import tkinter as tk
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from random import shuffle
import numpy as np

__author__ = 'Abraham Moreno'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class Othello(JuegoSumaCeros2T):
    """docstring for Othello."""
    def __init__(self):
        x = [0 for _ in range(64)]
        x[27] = 1
        x[28] = -1
        x[35] = -1
        x[36] = 1
        super().__init__(tuple(x))
        self.historial.append(x)


    def buscar_vecinos(self, x, i, jugador):
        contra = jugador * -1
        vecinos = [1, 7, 8, 9, -1, -7, -8, -9]
        if i // 8 == 0:
            vecinos.remove(-7)
            vecinos.remove(-8)
            vecinos.remove(-9)
        if i // 8 == 7:
            vecinos.remove(7)
            vecinos.remove(8)
            vecinos.remove(9)
        if i % 8 == 7:
            vecinos.remove(1)
            if -7 in vecinos:
                vecinos.remove(-7)
            if 9 in vecinos:
                vecinos.remove(9)
        if i % 8 == 0:
            vecinos.remove(-1)
            if 7 in vecinos:
                vecinos.remove(7)
            if -9 in vecinos:
                vecinos.remove(-9)

        return tuple([v for v in vecinos if x[i+v] == contra])

    def hay_ficha(self, x, i, v, jugador):
        b = i + v
        while b%8 != 0 or b%8 != 7 or b//8 != 0 or b//8 != 7:
            if b > 63 or b < 0:
                break #por si acaso 
            if x[b] == 0:
                return None
            elif x[b] == jugador:
                return b
            b += v
        return None

    def jugadas_legales(self):
        x = self.x[:]
        jugador = self.jugador
        jl = []
        for i in range(64):
            if x[i] == 0:
                vcfc = self.buscar_vecinos(x, i, jugador)
                if not vcfc:
                    continue
                else:
                    for v in vcfc:
                        if self.hay_ficha(x, i, v, jugador):
                            jl.append(i)
                            break
        return tuple(jl)

    def terminal(self):
        if self.x.count(-1) > 32:
            return -1
        elif self.x.count(1) > 32:
            return 1
        elif self.jugadas_legales() is None:
            return 1 if self.x.count(1) > self.x.count(-1) else -1
        else:
            return None

    def hacer_jugada(self, jugada):
        x = self.x[:]
        jugador = self.jugador
        vcfc = self.buscar_vecinos(x, jugada, jugador)
        self.x[jugada] = jugador
        for v in vcfc:
            if self.hay_ficha(x, jugada, v, jugador):
                f = self.hay_ficha(x, jugada, v, jugador)
                i = jugada+v
                while i != f:
                    self.x[i] = jugador
                    i += v
        self.historial.append(x)
        self.jugador *= -1
        return None

    def deshacer_jugada(self):
        x = self.historial.pop()
        self.x = x[:]
        self.jugador *= -1

def utilidad_Oth(x):
    num_negras = x.count(1)/100
    num_blancas = x.count(-1)/100
    return num_negras - num_blancas

def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    shuffle(jugadas)
    return jugadas


class OthelloTK:
    def __init__(self, tmax=5 ,escala=2):

        self.app = app = tk.Tk()
        self.app.title("Othello")
        self.L = L = int(escala) * 30
        self.tr_ta = {}

        tmpstr = "HOLA"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=3 * L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonX = tk.Button(barra,
                           command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con X')
        botonX.grid(column=0, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con O')
        botonO.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.9 * L), 'bold')
        for i in range(64):
            self.tablero[i] = tk.Canvas(ctn, height=L, width=L,
                                        bg='light grey', borderwidth=0)
            self.tablero[i].grid(row=i // 8, column=i % 8)
            self.textos[i] = self.tablero[i].create_text(L // 2, L // 2,
                                                         font= letra, text=' ')
            self.tablero[i].val = 0
            self.tablero[i].pos = i


    def jugar(self, primero):
        juego = Othello()

        if not primero:
            jugada = minimax(juego, dmax=3, utilidad=utilidad_Oth,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)

        for _ in range(64):
            self.anuncio['text'] = "Juegas tu"
            self.actualiza_tablero(juego.x)
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)
            self.anuncio['text'] = "Juega paython"
            ganador = juego.terminal()
            if ganador is not None:
                break
            jugada = minimax(juego, dmax=3, utilidad=utilidad_Oth,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            ganador = juego.terminal()
            if ganador is not None:
                break

        self.actualiza_tablero(juego.x)
        finstr = ("Empate" if ganador == 0 else
                  "Ganaste"
                  if (ganador > 0 and primero) or (ganador < 0 and not primero)
                  else "¡Gané¡")
        self.anuncio['text'] = finstr
        self.anuncio.update()

    def escoge_jugada(self, juego):
        jugadas_posibles = list(juego.jugadas_legales())

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
            if self.tablero[i].val != x[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text=' xo'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    OthelloTK().arranca()

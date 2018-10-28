#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'nombre del alumno'
import tkinter as tk
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------


class Othello:
    def __init__(self):
        self.x = [0 for _ in range(64)]
        self.historial = []
        self.jugador = 1
        self.x[27], self.x[36] = -1, -1
        self.x[28], self.x[35] = 1, 1

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
            if (len(ady) != 0 and self.x[i] == 0):
                if len(self.buscar_lugar(i, ady)) != 0:
                    jugadas.append(i)

        return jugadas

    def hacer_jugada(self, jugada):
        self.historial.append(jugada)
        for x in self.buscar_lugar(jugada, self.adyacentes(self.x, jugada, self.jugador)):
            aux = x
            while self.x[jugada + aux] == -1 * self.jugador:
                self.x[jugada + aux] = self.jugador
                aux+=x
        self.x[jugada] = self.jugador
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
    # direcciones posibles = [-9, -8, -7, -1, 1, 7, 8, 9]
    def buscar_lugar(self, jugada, direcciones):
        captura = []
        orilla_izq = [8 * x for x in range(8)]
        orilla_der = [8 * x -1 for x in range(1,9)]
        orilla_sup = [i for i in range(8)]
        orilla_inf = [i for i in range(56,64)]
        for x in direcciones:
            aux = jugada + x
            while aux < 64 and self.x[aux] == -1 * self.jugador:
                if x in [-9, -1, 7] and aux not in orilla_izq:
                    aux+= x
                elif x in [9, 1, -7] and aux not in orilla_der:
                    aux+= x
                elif x in [8, -8]:
                    aux+=x
                else:
                    break
            if aux < 64 and self.x[aux] == self.jugador:
                captura.append(x)
        return captura


    def terminal(self):
        if len(self.jugadas_legales()) == 0:
            self.jugador = self.jugador * -1
            if len(self.jugadas_legales()) == 0:
                return True
            self.jugador = -1 * self.jugador

class OthelloTK:
    def __init__(self, escala=1):

        self.app = app = tk.Tk()
        self.app.title("Reversi")
        self.L = L = int(escala) * 50

        tmpstr = "Escoge, negras empiezan."
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=3 * L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonX = tk.Button(barra,
                           command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con Negras')
        botonX.grid(column=0, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=False: self.jugar(x),
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
        if not primero:
            jugada = self.escoge_jugada(juego)
            #jugada = minimax(juego, dmax = 100, utilidad=utilidad_uttt)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)

        self.anuncio['text'] = "A ver de que cuero salen más correas"
        for _ in range(81):
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)
            ganador = juego.terminal()
            if ganador is not None:
                break
            #jugada = minimax(juego, dmax=500, utilidad=utilidad_uttt)
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)
            ganador = juego.terminal()
            if ganador is not None:
                break

        finstr = ("UN ASQUEROSO EMPATE, aggggg" if ganador == 0 else
                  "Ganaste, bye"
                  if (ganador > 0 and primero) or (ganador < 0 and not primero)
                  else "¡Gané¡  Juar, juar, juar.")
        self.anuncio['text'] = finstr
        self.anuncio.update()

    def escoge_jugada(self, juego):
        jugadas_posibles = list(juego.jugadas_legales())
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
                self.tablero[i].val = x[i]
                self.tablero[i].update()
            elif self.tablero[i].val != x[i] and x[i] == 1:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text='\u26AB', fill = "black")
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    OthelloTK().arranca()

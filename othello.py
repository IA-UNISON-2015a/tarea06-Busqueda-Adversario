#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'nombre del alumno'
import tkinter as tk


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello:
    def __init__(self):
        self.x = [0 for i in range(64)]
        self.historial = []
        self.jugador = 1

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

        if not primero:
            #jugada = self.escoge_jugada(juego)
            jugada = minimax(juego, dmax = 100, utilidad=utilidad_uttt)
            juego.hacer_jugada(jugada)
            #el siguiente metodo tiene que actualizar los metagatos
            #ya que deshacer jugadas no lo hace
            juego.deshacer_meta()
            self.actualiza_tablero(juego.x)

        self.anuncio['text'] = "A ver de que cuero salen más correas"
        for _ in range(81):
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)
            ganador = juego.terminal()
            if ganador is not None:
                break
            jugada = minimax(juego, dmax=500, utilidad=utilidad_uttt)
            #jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            juego.deshacer_meta()
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
        for i in range(81):
            if self.tablero[i].val != x[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text=' xo'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    OthelloTK().arranca()

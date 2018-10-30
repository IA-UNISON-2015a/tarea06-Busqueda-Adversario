#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Fabian Encinas Silvas'
import tkinter as tk
from busquedas_adversarios import minimax
from busquedas_adversarios import JuegoSumaCeros2T

# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class Othello(JuegoSumaCeros2T):

    def __init__(self, jugador=1):
  
        tablero = [0 for _ in range(64)]
        tablero[28], tablero[35] = 1, 1
        tablero[27], tablero[36] = -1, -1
        super().__init__(tuple(tablero))

    def jugadas_legales(self):
        """
        Esta funcion se encarga de saber las jugadas legales para un determinado estado

        """
        return ([i * 8 + j for i in range(8) for j in range(8) if self.casillas_a_tomar(i, j) is not None])

    def casillas_a_tomar(self, i, j):
        """
        Da la casilla a tomar desde una posicion, se utiliza para ver si una uguada es legal

        """

        def mov_dentro_tablero(i, j):
            return 0 <= i <= 7 and 0 <= j <= 7

        casillas_por_voltear = []
        if self.x[i * 8 + j] != 0 or not mov_dentro_tablero(i, j):
            return None
        for (k, l) in ((-1, -1), (0, -1), (1, -1), (-1, 0),
                       (1, 0), (-1, 1), (0, 1), (1, 1)):
            aux_i = i + k
            aux_j = j + l

            if (mov_dentro_tablero(aux_i, aux_j) and
                self.x[aux_i * 8 + aux_j] == -self.jugador):
                aux_i += k
                aux_j += l

                if not mov_dentro_tablero(aux_i, aux_j):
                    continue

                while self.x[aux_i * 8 + aux_j] == -self.jugador:
                    aux_i += k
                    aux_j += l
                    if not mov_dentro_tablero(aux_i, aux_j):
                        break

                if not mov_dentro_tablero(aux_i, aux_j):
                    continue

                if self.x[aux_i * 8 + aux_j] == self.jugador:
                    while True:
                        aux_i -= k
                        aux_j -= l
                        if aux_i == i and aux_j == j:
                            break
                        casillas_por_voltear.append(aux_i * 8 + aux_j)
        if len(casillas_por_voltear) == 0:
            return None
        return (casillas_por_voltear)


    def terminal(self):
        """
        checa si un estado es terminal si no hay espacios o si ni uno de los 
        dos jugadores puede moverse

        """
        if 0 not in self.x:
            return utilidad(self.x)

        if not self.jugadas_legales():
            self.jugador *= -1
            if not self.jugadas_legales():
                self.jugador *= -1
                return utilidad(self.x)
            self.jugador *= -1

        return None


    def hacer_jugada(self, jugada):

        if jugada is not None:
            i = jugada // 8
            j = jugada % 8
            casillas = list(self.casillas_a_tomar(i, j))
            casillas.append(jugada)
            tuple(casillas)

            for casilla in casillas:
                self.x[casilla] = self.jugador

            self.historial.append(casillas)
            self.jugador *= -1
        else:
            self.historial.append(jugada)
            self.jugador *= -1


    def deshacer_jugada(self):
        """
        cambia de jugador si la jugada es none

        """
        casillas = self.historial.pop()
        if casillas is not None:
            jugada = list(casillas).pop()

            self.x[jugada] = 0
            for casilla in casillas:
                self.x[casilla] = -self.x[casilla]
            self.jugador *= -1
        else:
            self.jugador *= -1


def utilidad(x):
 
    # Movimientos
    def dentro_tablero(i, j):
        # Ver si una posicion esta dentro del tablero
        return 0 <= i <= 7 and 0 <= j <= 7

    def calcular_movimientos(x):
        mov = [0, 0]
        for i in range(8):
            for j in range(8):
                if x[i * 7 + j] == 0 or not dentro_tablero(i, j):
                    continue

                for (k, l) in ((-1, -1), (0, -1), (1, -1), (-1, 0),
                               (1, 0), (-1, 1), (0, 1), (1, 1)):
                    aux_i = i + k
                    aux_j = j + l

                    if (dentro_tablero(aux_i, aux_j) and
                        x[aux_i * 8 + aux_j] == -x[aux_i * 8 + aux_j]):
                        aux_i += k
                        aux_j += l

                        if not dentro_tablero(aux_i, aux_j):
                            continue

                        while x[aux_i * 8 + aux_j] == -x[aux_i * 8 + aux_j]:
                            aux_i += k
                            aux_j += l
                            if not dentro_tablero(aux_i, aux_j):
                                break

                        if not dentro_tablero(aux_i, aux_j):
                                continue

                        if x[aux_i * 8 + aux_j] == x[aux_i * 8 + aux_j]:
                            if x[aux_i * 8 + aux_j] == 1:
                                mov[0] += 1
                            else:
                                mov[1] += 1


        mov[0] /= 2
        mov[1] /= 2
        return (100 * (mov[0] - mov[1]) / (mov[0] + mov[1]) if
                mov[0] + mov[1] != 0 else 0)

    return (100 * (x.count(1) - x.count(-1)) / (x.count(1) + x.count(-1)) +
            calcular_movimientos(x))


def ordena_jugadas(juego):
    """
    Ordena jugadas en base a la utilidad

    """
    jugadas = list(juego.jugadas_legales())
    utilidades = []
    for jugada in jugadas:
        juego.hacer_jugada(jugada)
        utilidades.append(utilidad(juego.x))
        juego.deshacer_jugada()

    return [x for (_, x) in sorted(zip(utilidades, jugadas))]


class OthelloTK():
    def __init__(self, tmax=10, escala=2):


        self.tr_ta = {}

        self.tmax = tmax

        self.app = app = tk.Tk()
        self.app.title("Othello")
        self.L = L = int(escala) * 30

        tmpstr = "Excoge, X siempre empiezan"
        msgX = "Puntos X: 0"
        msgO = "Puntos Y: 0"
        self.anuncio = tk.Message(app, bg='black', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=8 * L)
        self.anuncio.pack()

        self.ptsX = tk.Message(app, bg='black', borderwidth=1,
                               justify=tk.CENTER, text=msgX,
                               width=8 * L)
        self.ptsX.pack()

        self.ptsO = tk.Message(app, bg='black', borderwidth=1,
                               justify=tk.CENTER, text=msgO,
                               width=8 * L)
        self.ptsO.pack()

        barra = tk.Frame(app)
        barra.pack()

        self.botonN = tk.Button(barra, command=lambda x=True: self.jugar(x),
                                text='Jugar con X')

        self.botonN.grid(column=0, row=0)

        self.botonB = tk.Button(barra, command=lambda x=False: self.jugar(x),
                                text='Jugar con O')

        self.botonB.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.4 * L), 'bold')
        for i in range(64):
            self.tablero[i] = tk.Canvas(ctn, height=L, width=L,
                                        bg='light grey', borderwidth=0)
            self.tablero[i].grid(row=i // 8, column=i % 8)
            self.tablero[i].val = 0
            self.tablero[i].pos = i
            self.textos[i] = self.tablero[i].create_text(L // 2, L // 2,
                                                         font=letra,
                                                         text=' ')

    def jugar(self, primero):
        juego = Othello()
        self.botonN['state'] = 'disabled'
        self.botonB['state'] = 'disabled'

        if not primero:
            jugada = minimax(juego, dmax=5, utilidad=utilidad,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)

        self.anuncio['text'] = "Juego de othello"

        for _ in range(64):
            self.ptsX['text'] = "Puntos X: " + str(juego.x.count(1))
            self.ptsO['text'] = "Puntos O: " + str(juego.x.count(-1))

            self.actualiza_tablero(juego.x)

            if len(juego.jugadas_legales()) > 0:
                jugada = self.escoge_jugada(juego)
                """
                jugada = minimax(juego, dmax=5, utilidad=utilidad,
                                 ordena_jugadas=ordena_jugadas,
                                 transp=self.tr_ta)
                """
                juego.hacer_jugada(jugada)

                self.actualiza_tablero(juego.x)

                ganador = juego.terminal()

                if ganador is not None:
                    break
            else:
                jugada = None
                juego.hacer_jugada(jugada)
                ganador = juego.terminal()
                if ganador is not None:
                    break

            if len(juego.jugadas_legales()) > 0:
                jugada = minimax(juego, dmax=5, utilidad=utilidad,
                                 ordena_jugadas=ordena_jugadas,
                                 transp=self.tr_ta)
                juego.hacer_jugada(jugada)

                self.actualiza_tablero(juego.x)

                ganador = juego.terminal()
                if ganador is not None:
                    break
            else:
                jugada = None
                juego.hacer_jugada(jugada)
                ganador = juego.terminal()
                if ganador is not None:
                    break

        self.actualiza_tablero(juego.x)
        print('El ganador es: ', ganador)
        finstr = ("EMPATE" if ganador == 0 else "Mijo ganaste... toma un pallmall-aliento" if
                  (ganador > 0 and primero) or (ganador < 0 and not primero)
                  else "Te gano una maquina que macana hehexd")
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
            if self.tablero[i].val != x[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text=' xo'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()



if __name__ == '__main__':
    OthelloTK().arranca()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustedes mismos, con jugador 'inteligente.'

"""

__author__ = 'Ivan Moreno'

from collections import deque
from copy import deepcopy

import busquedas_adversarios as ba


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(ba.JuegoSumaCeros2T):
    """
    Clase que implementa una representacion computacional del Othello.

    La tupla del estado es así:
    56  57  58  59  60  61  62  63
    48  49  50  51  52  53  54  55
    40  41  42  43  44  45  46  47
    32  33  34  35  36  37  38  39
    24  25  26  27  28  29  30  31
    16  17  18  19  20  21  22  23
    8   9   10  11  12  13  14  15
    0   1   2   3   4   5   6   7
    """

    def __init__(self):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza.
        """
        x0 = (0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0,-1, 1, 0, 0, 0,
              0, 0, 0, 1,-1, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0)
        super().__init__(x0 = x0)

        # Iba a guardar las fichas cambiadas dentro del historial
        # de jugadas, pero luego me puse a ver como los del semestre
        # pasado habían hecho sus interfaces, y cuando vi lo que hizo
        # Belén para el historial de jugadas dije: "ah, eso esta mejor."
        # Por lo que hago lo que ella hizo y prefiero usar mucha más
        # memoria para que la búsqueda pueda ser más rápida.
        self.historial = deque()
        self.estados_anteriores = deque()

        self.orilla = set() # Guarda las casillas donde podrían haber jugadas legales.
        self.orillas_pasadas = deque()
        for casilla in (18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45):
            self.orilla.add(casilla)

        self.jugador = 1

    def __str__(self):
        """
        Imprime bonito. Temporal.
        """
        rep = ''.join(str(self.x[i]) + ' ' for i in range(56, 64))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(48, 56))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(40, 48))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(32, 40))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(24, 32))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(16, 24))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(8, 16))
        rep += '\n'
        rep += ''.join(str(self.x[i]) + ' ' for i in range(0, 8))
        rep += '\n'
        return rep

    def jugadas_legales(self):
        """
        Calcula las jugadas en las que el jugador actual obtiene fichas
        del oponente.
        """
        jugadas = []

        for casilla in list(self.orilla):
            # Se calculan las coordenadas de la casilla actual.
            x = casilla % 8
            y = casilla // 8
            captura = self.revisarCapturas((x, y))
            # Si hay al menos una captura, es jugada legal.
            if True in captura:
                jugadas.append((x, y))

        return jugadas

    def terminal(self):
        """
        Revisa si ambos oponentes tendrán que pasar en el próximo turno.
        Regresa la utilidad en base al jugador de fichas negras.
        """
        if not self.jugadas_legales():
            self.jugador = -1 * self.jugador

            if not self.jugadas_legales():
                self.jugador = -1 * self.jugador

                negras = self.x.count(1)
                blancas = self.x.count(-1)
                return (1 if negras > blancas else
                       -1 if blancas > negras else 0)

        return None

    def revisarCapturas(self, jugada):
        """
        Revisa que hileras de fichas se capturan con una jugada
        dada. Devuelve una lista indicando que filas fueron
        capturadas.

        @param jugada: Tupla con las coordenadas de la jugada.
        """
        x, y = jugada
        casilla = x + 8*y
        estado = self.x
        filas = [False for i in range(8)]

        # Horizontal <-
        if x > 1:
            sig_capturada = estado[casilla - 1] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla-2, casilla-x-1, -1)]
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[0] = True

        # Horizontal ->
        if x < 6:
            sig_capturada = estado[casilla + 1] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla+2, casilla+8-x)]
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[1] = True

        # Vertical hacia arriba.
        if y < 6:
            sig_capturada = estado[casilla + 8] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla+16, casilla+((8-y)*8), 8)]
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[2] = True

        # Vertical hacia abajo.
        if y > 1:
            sig_capturada = estado[casilla - 8] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla-16, casilla-(8*y)-1, -8)]
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[3] = True

        # Diagonal hacia arriba e izquierda.
        if x > 1 and y < 6:
            sig_capturada = estado[casilla + 7] == -1*self.jugador
            x_sig = x - 1
            y_sig = y + 1

            if sig_capturada:
                c = casilla + 14

                while (x_sig > -1 and y_sig < 8):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig -= 1
                    y_sig += 1
                    c += 7

                if fila_capturada:
                    filas[4] = True

        # Diagonal hacia arriba y derecha.
        if x < 6 and y < 6:
            sig_capturada = estado[casilla + 9] == -1*self.jugador
            x_sig = x + 1
            y_sig = y + 1

            if sig_capturada:
                c = casilla + 18

                while (x_sig < 8 and y_sig < 8):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig += 1
                    y_sig += 1
                    c += 9

                if fila_capturada:
                    filas[5] = True

        # Diagonal hacia abajo e izquierda.
        if x > 1 and y > 1:
            sig_capturada = estado[casilla - 9] == -1*self.jugador
            x_sig = x - 1
            y_sig = y - 1

            if sig_capturada:
                c = casilla - 18

                while (x_sig > -1 and y_sig > -1):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig -= 1
                    y_sig -= 1
                    c -= 9

                if fila_capturada:
                    filas[6] = True

        # Diagonal hacia abajo y derecha.
        if x < 6 and y > 1:
            sig_capturada = estado[casilla - 7] == -1*self.jugador
            x_sig = x + 1
            y_sig = y - 1

            if sig_capturada:
                c = casilla - 14

                while (x_sig < 8 and y_sig > -1):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig += 1
                    y_sig -= 1
                    c -= 7

                if fila_capturada:
                    filas[7] = True

        return filas

    def hacer_jugada(self, jugada):
        """
        Actualiza el tablero de juego y guarda el estado anterior.

        @param jugada: Tupla que contiene la coordenada donde se agrega una ficha.
        """
        # Antes de modificar, guardamos el estado actual.
        self.estados_anteriores.append(self.x)
        self.orillas_pasadas.append(deepcopy(self.orilla))
        estado = list(self.x)

        x, y = jugada
        casilla = x + 8*y
        estado[casilla] = self.jugador # Actualizamos la casilla donde se jugó.
        filas_capturadas = self.revisarCapturas(jugada) # Obtenemos donde capturó la jugada.

        # Revisa en el orden: <-, ->, arriba, abajo, diagonal superior izquierdo,
        # diagonal superior derecho, diagonal inferior izquierdo, diagonal
        # inferior derecho.
        for (f, d) in zip(filas_capturadas, (-1, 1, 8, -8, 7, 9, -9, -7)):
            # Si una fila fue capturada, voltea todas las fichas del oponente
            # que estén entre dos fichas del jugador actual.
            if f:
                cas_capturada = casilla + d
                while(estado[cas_capturada] != self.jugador):
                    estado[cas_capturada] = self.jugador
                    cas_capturada += d

        # Actualizamos y contamos la orilla de las fichas en el tablero.
        for vecino in (-1, 7, 8, 9, 1, -7, -8, 9):
            if estado[casilla + vecino] == 0:
                self.orilla.add(casilla+vecino)

        # Formalizamos los cambios.
        self.x = tuple(estado)
        self.jugador *= -1
        self.orilla.remove(casilla)
        self.historial.append(jugada)

    def deshacer_jugada(self):
        """
        Viaja en el tiempo y restaura el estado anterior del juego, mientras
        al estado actual lo manda a volar y actualiza la orilla de las fichas.
        """
        jugada_pasada = self.historial.pop()
        self.x = self.estados_anteriores.pop()
        self.orilla = self.orillas_pasadas.pop()

if __name__ == '__main__':
    juego = Othello()
    jugadas = [(5, 4), (3, 5), (2, 6), (5, 3), (3, 2)]

    print(juego)
    print(juego.orilla)

    juego.hacer_jugada(jugadas[0])
    print(juego)
    print(juego.orilla)

    juego.deshacer_jugada()
    print(juego)
    print(juego.orilla)

    juego.hacer_jugada(jugadas[1])
    print(juego)

    juego.hacer_jugada(jugadas[2])
    print(juego)

    juego.hacer_jugada(jugadas[3])
    print(juego)

    juego.hacer_jugada(jugadas[4])
    print(juego)


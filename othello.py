#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
import numpy as np
import copy

__author__ = 'Ricardo Holguin Esquer'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):

    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:

                        56  57  58  59  60  61  62  63
                        48  49  50  51  52  53  54  55
                        40  41  42  43  44  45  46  47
                        32  33  34  35  36  37  38  39
                        24  25  26  27  28  29  30  31
                        16  17  18  19  20  21  22  23
                         8   9  10  11  12  13  14  15
                         0   1   2   3   4   5   6   7

        Y las posiciones iniciales son en 35, 36, 27, 28
        """
        super().__init__(tuple([0 for _ in range(8*8)]))
        # Yo manejare todo como una matriz pero acordamos todos usar un solo
        # vector de 8*8 que representa una matriz como el estado
        self.tablero = np.array([0 for i in range(8) for j in range(8)])
        self.tablero = np.reshape(self.tablero, (-1, 8))

        # 8 direcciones posibles
        self.dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1, 0, 0, 1, 1, 1]

        # Iniciar tablero
        # 1 = blancas, -1 = negras
        z = int((8-2)/2)
        self.tablero[z][z] = 1
        self.tablero[z+1][z+1] = 1
        self.tablero[z][z+1] = -1
        self.tablero[z+1][z] = -1

        xAux = []
        for i in self.tablero:
            xAux.extend(i)
        self.x = xAux

    def imprimirTablero2(self):
        print(self.tablero)

    def hacer_jugada(self, x, y, jugador):
        piezasTomadas = 0
        self.tablero[y][x] = jugador
        for d in range(8): # 8 direcciones
            ctr = 0
            for i in range(8): #El tamaño del tablero
                # Calcula la coordenada de la direccion en la que esta buscando
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                # Si se sale del tablero entonces se sale del ciclo
                if dx < 0 or dx > 9 or dy < 0 or dy > 9:
                    ctr = 0
                    break
                elif self.tablero[dy][dx] == jugador:
                    break
                elif self.tablero[dy][dx] == 0:
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + dirx[d]*(i+1)
                dy = y + diry[d]*(i+1)
                self.tablero[dy][dx] = jugador
            piezasTomadas += ctr

    def verificar_jugada(self, tablero, x, y, jugador):
        """
        Es exactamente igual que hacer_jugada pero esta no altera
        el tablero del juego y solo se usa para verificar si una jugada
        es valida
        """
        piezasTomadas = 0
        tablero[y][x] = jugador
        for d in range(8): # 8 direcciones
            ctr = 0
            for i in range(8): #El tamaño del tablero
                # Calcula la coordenada de la direccion en la que esta buscando
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                # Si se sale del tablero entonces se sale del ciclo
                if dx < 0 or dx > 9 or dy < 0 or dy > 9:
                    ctr = 0
                    break
                elif tablero[dy][dx] == jugador:
                    break
                elif tablero[dy][dx] == 0:
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + dirx[d]*(i+1)
                dy = y + diry[d]*(i+1)
                tablero[dy][dx] = jugador
            piezasTomadas += ctr
        return (tablero, piezasTomadas)

    def movimientoValido(self, x, y, jugador):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        if self.tablero[y][x] != 0:
            return False
        (_,piezasTomadas) = verificar_jugada(copy.deepcopy(self.tablero),
                                            x, y, jugador)
        if piezasTomadas == 0:
            return False
        return True

    def jugadas_legales(self):

    def terminal(self):
        for y in range(8):
            for x in range(8):
                if movimientoValido(x, y, jugador):
                    return False
        return True

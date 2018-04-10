#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'luis fernando'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):

    """
    Inicializa el juego, esto es: el número de columnas y
    renglones y el estado inicial del juego. Cuyas posiciones
    estan dadas como:
    8x8

    57  58  59  60  61  62  63  64
    49  50  51  52  53  54  55  56
    41  42  43  44  45  46  47  48
    32  33  34  35  36  37  38  40
    24  25  26  27  28  29  30  31
    16  17  18  19  20  21  22  23
     8   9  10  11  12  13  14  15
     0   1   2   3   4   5   6   7
    """
    def __init__(self):
        board = [0 for _ in range(8 * 8)]
        board[3 + 5*8] = 1
        board[4 + 4*8] = 1

        board[4 + 5*8] = -1
        board[3 + 4*8] = -1
        super().__init__(tuple(board))

    """
    Las jugadas legales son las columnas donde se puede
    poner una ficha (0, ..., 6), si no está llena.
    """
    def jugadas_legales(self):
        pass
        return ()
        return (j for j in range(7) if self.x[35 + j] == 0)

    def terminal(self):
        pass

    def hacer_jugada(self, jugada):
        pass

    def deshacer_jugada(self, jugada):
        pass

    def ordena_jugadas(juego):
        pass


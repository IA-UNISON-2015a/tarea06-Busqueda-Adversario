#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T

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

    56  57  58  59  60  61  62  63
    48  49  50  51  52  53  54  55
    40  41  42  43  44  45  46  47
    32  33  34  35  36  37  38  39
    24  25  26  27  28  29  30  31
    16  17  18  19  20  21  22  23
     8   9  10  11  12  13  14  15
     0   1   2   3   4   5   6   7
    """
    def __init__(self):
        board = [0 for _ in range(8 * 8)]
        board[35] = 1
        board[28] = 1

        board[36] = -1
        board[27] = -1
        super().__init__(tuple(board))

    """
    Una jugada legal es un indice del tablero (vacio) donde el jugador de
    turno puede poner una ficha.
    """
    def jugadas_legales(self):
        return (i + 8*j for i in range(8) for j in range(8)
                if jugada_legal((i,j)) and self.x[i + 8*j] == 0)

    """
    Una jugada legal es un indice del tablero (vacio) donde el jugador de
    turno puede poner una ficha.

    @param pos: Tupla (x,y) indicando el lugar en el tablero
    """
    def jugada_legal(self, pos):
        #direcciones = (-1 + 8,  0 + 8,  1 + 8,
        #               -1 + 0,          1 + 0,
        #               -1 - 8,  0 - 8,  1 - 8)

        direcciones = ((-1,1),  (0,1),  (1,1),
                       (-1,0),          (1,0),
                       (-1,-1), (0,-1), (1,-1))

        for direccion in direcciones:
            if any(fichas_seguidas(pos, direccion) for direccion in direcciones):
                return True

        return False

    """
    Si poner una ficha en la tupla indicada por pos es legal, esto regresa todas
    un diccionario con todas las direcciones que hacen a la posicion legal.

    @param pos: Tupla (x,y) indicando el lugar en el tablero

    @return Diccionario con llaves la direccion en donde poner la ficha voltearia
            fichas del oponente y valores una tupla de direcciones.
    """
    def voltea_dir(self, pos):
        direcciones = {ne:(-1,1),  n:(0,1),  no:(1,1),
                        e:(-1,0),             o:(1,0),
                       se:(-1,-1), s:(0,-1), so:(1,-1)}

        dir_volteo = dict()
        for direccion in direcciones:
            if fichas_seguidas(pos, direccion):
                dir_volteo[direccion] = direcciones[direccion]

        return dir_volteo

    #def es_orilla(pos):
        #return pos in {0,1,2,3,4,5,6,7, 57,58,59,60,61,62,63,64} or
               #pos % 8 == 0 or pos % 8 == 7

    """
    Recibe una tupla de la forma (x,y), indicando una posicion en el tablero
    """
    def dentro_tablero(pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    """
    Revisa si desde la posicion recibida, hay fichas del que no es turno en
    la direccion recibida y que terminan en una ficha del jugador de turno.

    @param pos: Posicion en el tablero. Tupla que indica la posicion
    @param direccion: Tupla que indica una direccion
    """
    def fichas_seguidas(self, pos, direccion):
        aux = pos[0] + direccion[0], pos[1] + direccion[1]
        if dentro_tablero(aux) and self.x[aux[0] + 8*aux[1]] == self.jugador*-1:
            while dentro_tablero(aux) and self.x[aux[0] + 8*aux[1]] != 0:
                aux = aux[0] + direccion[0], aux[1] + direccion[1]
                if self.x[aux[0] + 8*aux[1]] == self.jugador:
                    return True

        return False

    """
    Devuelve None si no es terminal el estado actual,
    en otro caso devuelve la ganancia para el jugador 1.
    """
    def terminal(self):
        if 0 not in self.x:
            jug_leg = [jl for jl in jugadas_legales()]
            if not jug_leg:
                return self.x.count(1)

        return None

    """
    Realiza la jugada, modifica el estado. La jugada es que el jugador de turno ponga
    una ficha en el indice indicado por la variable jugada y se voltean todas las fichas
    correspondientes del contrincante.
    """
    def hacer_jugada(self, jugada):
        self.x[jugada] = self.jugador

        direcciones = voltea_dir((jugada%8, int(jugada/8)))

        for direccion in direcciones.values():
            dir_lineal = direccion[0] + 8*direccion[1]
            aux = jugada + dir_lineal

            while self.x[aux] != self.jugador:
                self.x[aux] = self.jugador
                aux += dir_lineal

        self.historial.append(jugada)

    def deshacer_jugada(self, jugada):
        pass

    def ordena_jugadas(juego):
        pass


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'José Roberto Salazar Espinoza'

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax

class Otello(JuegoSumaCeros2T):
    def __init__(self):
        super().__init__((
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,1,-1,0,0,0,
            0,0,0,1,-1,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0  
        ))
    
    def revisar_arriba(self,pos):
        reng,col = (pos//8,pos%8)

        if reng < 2 or self.x[pos - 8] != -self.jugador:
            return False

        for i in range(reng-2,0,-1):
            if self.x[ i*8 + col ] == self.jugador:
                return True

        return False

    def revisar_abajo(self,pos):
        reng,col = (pos//8,pos%8)

        if reng > 5 or self.x[pos + 8] != -self.jugador:
            return False

        for i in range(reng+2,8):
            if self.x[ i*8 + col ] == self.jugador:
                return True

        return False

    def revisar_derecha(self,pos):
        reng,col = (pos//8,pos%8)

        if col > 5 or self.x[pos + 1] != -self.jugador:
            return False

        for i in range(col+2,8):
            if self.x[ reng*8 + i ] == self.jugador:
                return True

        return False

    def revisar_izquierda(self,pos):
        reng,col = (pos//8,pos%8)

        if col < 2 or self.x[pos - 1] != -self.jugador:
            return False

        for i in range(col-2,0,-1):
            if self.x[ reng*8 + i ] == self.jugador:
                return True

        return False

    def puede_ir_pieza(self,pos):
        return (self.revisar_arriba(pos) or self.revisar_abajo(pos) 
                or self.revisar_izquierda(pos) or self.revisar_derecha(pos))

    def imprime_tablero(self):
        tablero = '_________________\n'
        for i in range(8):
            renglon = '|'
            for j in range(8):
                if self.x[i*8 + j] == -1:
                    renglon += '○|'
                elif self.x[i*8 + j] == 1:
                    renglon += '•|'
                else:
                    renglon += ' |'
            tablero += renglon + '\n'
        tablero += '─────────────────'
        print(tablero)

if __name__ == '__main__':
    otello = Otello()
    mov = []
    for i in range(8*8):
        if otello.puede_ir_pieza(i):
            mov.append(i)
    print(mov)
    otello.imprime_tablero()
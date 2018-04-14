#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
othello.py
------------

El juego de Otello implementado por ustedess mismos, con jugador inteligente

"""

__author__ = 'Jordan Urias'

class othello():
    def __init__(self, _n=8):
        self.n = _n
        self.tablero = [['0' for x in range(self.n)] for y in range(self.n)]
        # 8 direcciones
        self.dirx = [-1,  0,  1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1,  0, 0,  1, 1, 1]
        
        if self.n % 2 == 0: # Que sea un tablero par
            z = int((self.n - 2) / 2)
            self.tablero[z][z] = '2'
            self.tablero[self.n - 1 - z][z] = '1'        
            self.tablero[z][self.n - 1 - z] = '1'
            self.tablero[self.n - 1 - z][self.n - 1 - z] = '2'
    
    
    def PrintTablero(self):
        m = len(str(self.n - 1))
        for y in range(self.n):
            renglon = ''
            for x in range(self.n):
                renglon += self.tablero[y][x]
                renglon += ' ' * m
            print (renglon + ' ' + str(y))
        renglon = ''
        for x in range(self.n):
            renglon += str(x).zfill(m) + ' '
            print (renglon + '\n')        
    
    '''
     [4, 2, 2, 2, 2, 2, 2, 4],
     [2, 1, 1, 1, 1, 1, 1, 2],
     [2, 1, 1, 1, 1, 1, 1, 2],
     [2, 1, 1, 1, 1, 1, 1, 2],
     [2, 1, 1, 1, 1, 1, 1, 2],
     [2, 1, 1, 1, 1, 1, 1, 2],
     [2, 1, 1, 1, 1, 1, 1, 2],
     [4, 2, 2, 2, 2, 2, 2, 4]]
    '''
    def UtilidadTablero(self, tablero, jugador):
        utilidad = 0
        for y in range(self.n):
            for x in range(self.n):
                if tablero[y][x] == jugador:
                    if (x == 0 or x == self.n - 1) and (y == 0 or y == self.n - 1):
                        utilidad += 4 # Esquinas
                    elif (x == 0 or x == self.n - 1) or (y == 0 or y == self.n - 1):
                        utilidad += 2 # Lados
                    else:
                        utilidad += 1
        return utilidad
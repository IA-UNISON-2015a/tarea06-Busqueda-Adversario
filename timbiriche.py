#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
timbiriche.py
------------

El juego de Timbiriche implementado por ustedes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk

__author__ = 'Irving Borboa'

class Timbiriche(JuegoSumaCeros2T):
    def __init__(self):
        '''
        
            0   1   2
        3     4   5    6
            7   8   9
        10    11  12    13
            14  15   16
        17    18   19    20
            21   22   23
        24     25   26    27
            28    29   30
          
        '''
        self.x0 = tuple(30 * [0])
        self.x = 30 * [0]
        self.historial = []
        self.jugador = 1
    def jugadas_legales(self):
        for posicion in range(30):
            if self.x[posicion] == 0:
                return posicion
            
    def terminal(self):
        x = self.x
        for i in range(3):
            if x[i] != 0 and (x[i] == x[i+ 3] == x[i + 4] == x[i+7]):
                return x[i]
        for i in range(7,10):
            if x[i] != 0 and (x[i] == x[i+ 3] == x[i + 4] == x[i+7]):
                return x[i]
        for i in range(14,17):
            if x[i] != 0 and (x[i] == x[i+ 3] == x[i + 4] == x[i+7]):
                return x[i]
        for i in range(21,24):
            if x[i] != 0 and (x[i] == x[i+ 3] == x[i + 4] == x[i+7]):
                return x[i]
        if 0 not in self.x:
            return 0
        return None
    def hacer_jugada(self,jugada):
        for i in range(30):
            if self.x[self.jugador] == 0:
                self.x[i + jugada] = self.jugador
                self.historial.append(jugada)
                self.jugador *= -1
                return None
    def deshacer_jugada(self,jugada):
        pos = self.historial.pop()
        for i in range(30):
            if self.x[pos] != 0:
                self.x[pos] = 0
                self.jugador *= -1
                return None
            
def utilidad(x):
    utilidad = 0
    for i in range(3):
        if x[i] != 0 and (x[i] == x[i+ 3] == x[i + 4] == x[i+7]):
            utilidad += .25
        
    
    
    
        
    


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk
from random import shuffle
import time

"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Jordan Urias'

class othello(JuegoSumaCeros2T):
    def __init__(self):
        #Posicion inicial del tablero
        x= [0 for _ in range(64)]
        x[27]=-1
        x[28]=1
        x[35]=1
        x[36]=-1
        
        super().__init__(tuple(x),1)
        
    def terminal(self):
        negras = self.x.count(1)
        blancas = self.x.count(-1)
        
        #Si fue eliminado
        if negras == 0 or blancas == 0:
            return 1 if blancas > negras else -1

        #Si aun hay lugares.
        if 0 in self.x:
            return None

        #1 si ganan las blancas -1 si ganan las negras 0 en empate.
        return 1 if blancas > negras else -1 if negras > blancas else 0
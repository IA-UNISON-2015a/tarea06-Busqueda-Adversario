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
        """
        Se inicializa el tablero como una matriz de 8x8
        donde llena de 0,1 y -1, donde 0 es un lugar vacío,
        1 es una pieza blanca y -1 es una pieza negra.
        Para realizar este reversi me basé en el que está en el 
        siguiente link: https://inventwithpython.com/chapter15.html
        """
        super().__init__((
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 1,-1, 0, 0, 0],
            [ 0, 0, 0,-1, 1, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0]
        ))

    def dibuja_tablero(self):
        """ 
        Método para dibujar el tablero, lo dibuja en el siguiente formato:

           1   2   3   4   5   6   7   8  
         ┌───┬───┬───┬───┬───┬───┬───┬───┐
        1│   │   │   │   │   │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        2│   │   │   │   │   │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        3│   │   │   │   │   │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        4│   │   │   │ O │ X │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        5│   │   │   │ X │ O │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        6│   │   │   │   │   │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        7│   │   │   │   │   │   │   │   │
         ├───┼───┼───┼───┼───┼───┼───┼───┤
        8│   │   │   │   │   │   │   │   │
         └───┴───┴───┴───┴───┴───┴───┴───┘
        """
        tablero = "   0   1   2   3   4   5   6   7\n"
        tablero += " ┌───┬───┬───┬───┬───┬───┬───┬───┐\n"
        for reng in range(8):
            tablero += str(reng)
            for col in range(8):
                tablero += "│"
                tablero += " O " if self.x[reng][col] == 1 else " X " if self.x[reng][col] == -1 else "   "
            tablero += "│\n"
            tablero += " ├───┼───┼───┼───┼───┼───┼───┼───┤\n" if reng < 7 else " └───┴───┴───┴───┴───┴───┴───┴───┘"
        
        print(tablero)

    def esta_fuera_tablero(self,reng,col):
        #este método revisa si dados un renglón y un columna son coordenadas válidas para el tablero
        return (reng < 0 or reng >7 or col < 0 or col > 7) 

    def es_valido(self,reng,col):
        #primero se revisa si ya hay una pieza en la posición o si está fuera del tablero
        if self.x[reng][col] != 0 or self.esta_fuera_tablero(reng,col):
            return False
        
        #se revisan las ocho direcciones en las cuales se pueden voltear piezas
        for rStep,cStep in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]:

            #se revisa si la primera pieza en la dirección está en el tablero o si es diferente del otro jugador
            if self.esta_fuera_tablero(reng + rStep, col + cStep) or self.x[reng + rStep][col + cStep] != -self.jugador:
                continue
            
            #variables para moverte en la dirección
            rengTemp = reng + 2*rStep
            colTemp = col + 2*cStep

            #Ciclo para ver si se van a voltear piezas en la dirección
            while not self.esta_fuera_tablero(rengTemp, colTemp):
                if self.x[rengTemp][colTemp] == 0:
                    break
                if self.x[rengTemp][colTemp] == self.jugador:
                    return True  

                rengTemp += rStep
                colTemp += cStep

        return False

    def jugadas_legales(self):
        legales = []
        for reng in range(8):
            for col in range(8):
                if self.es_valido(reng,col):
                    legales.append((reng,col))
                    self.x[reng][col] = 2

        return legales
if __name__ == '__main__':
    otello = Otello()
    otello.dibuja_tablero()
    print(otello.jugadas_legales())
    otello.dibuja_tablero()
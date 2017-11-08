#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------


El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk

__author__ = 'Patricia Quiroz'


class Othello(JuegoSumaCeros2T):
  
    def __init__(self, jugador=1):
  """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:
	

        0	1	2	3	4	5	6	7
        8	9	10	11	12	13	14	15
        16	17	18	19	20	21	22	23
        24	25	26	27	28	29	30	31
        32	33	34	35	36	37	38	39
        40	41	42	43	44	45	46	47
        48	49	50	51	52	53	54	55
        56	57	58	59	60	61	62	63
        """

        super().__init__(tuple([0 for _ in range(8 * 8)]))

    def jugadas_legales(self):
    	 """
        Las jugadas legales son las posiciones donde se puede colocar una ficha 
        del propio color en una casilla vacía. Entre la ficha recién colocada y otra
		del mismo color (previamente en el tablero) debe haber fichas del color contrario en la misma
		línea (ya sea en dirección diagonal, horizontal o vertical).

		Voltear las fichas del color contrario que quedan entre la ficha recién colocada y cualquier
		otra del mismo color ya colocada. De esta forma, cambian de color.
        """

        """
        HELLO
		Se espera que apartir de mis fichas actuales cheque cuales tienen oportunidad de moverse
		Al inicio tiene 4 formas de colocar una ficha.
		
		Propuesta: Obtener la distancia entre cada una de las fichas en el tablero y 
		meterlos a un arreglo. ¿De que me sirve la distancia? Como tengo un arreglo para 
		el tableto, me sirve para saber si estan en diagonal, horizontal o vertical. 

		ES DECIR, si se intenta colocar una ficha, primero se checa si es legal hacerla, si no,
		no deja ponerla en la posicion.

		Al poder hacer una jugada significa que todas las fichas del oponente que esten en 
		esa "LINEA" me las voy a comer.

		COMO EL CONECTA 4, PODRIA CHECAR SI ESTAN EN LAS ESQUINAS O NO
        """
        for i in 8:
        	
        return None

    def terminal(self):
        """
		La partida acaba cuando nadie puede mover (normalmente cuando el tablero está lleno o casi
		lleno) y gana quien en ese momento tenga más fichas sobre el tablero.
        """
        return None

    def hacer_jugada(self, jugada):
        """for i in range(0, 41, 7):
            if self.x[i + jugada] == 0:
                self.x[i + jugada] = self.jugador
                self.historial.append(jugada)
                self.jugador *= -1
                return None"""

    def deshacer_jugada(self):
        """pos = self.historial.pop()
        for i in (35, 28, 21, 14, 7, 0):
            if self.x[i + pos] != 0:
                self.x[i + pos] = 0
                self.jugador *= -1
                return None"""

def utilidad_othello(x):
	return None

def ordena_jugadas(juego):
    """
    Ordena las jugadas de acuerdo al jugador actual, en función
    de las más prometedoras.

    Para que funcione le puse simplemente las jugadas aleatorias
    pero es un criterio bastante inaceptable

    """
    jugadas = list(juego.jugadas_legales())
    shuffle(jugadas)
    return jugadas	


def pprint_gato(x):
    y = [('X' if x[i] > 0 else 'O' if x[i] < 0 else str(i))
         for i in range(9)]
    print(" {} | {} | {} ".format(y[0], y[1], y[2]).center(60))
    print("---+---+---".center(60))
    print(" {} | {} | {} ".format(y[3], y[4], y[5]).center(60))
    print("---+---+---".center(60))
    print(" {} | {} | {} ".format(y[6], y[7], y[8]).center(60))


class OthelloTK:
    def __init__(self, escala=2):

    def jugar(self, primero):
    	return None
    def escoge_jugada(self, juego):


    def actualiza_tablero(self, x):
       

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    # juega_gato('X')
    OthelloTK().arranca()

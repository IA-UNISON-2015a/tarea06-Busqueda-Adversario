#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
timbiriche.py
------------

El juego de Timbiriche implementado por ustedes mismos, con jugador inteligente

"""

__author__ = 'nombre del alumno'

# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
class Timbiriche(JuegoSumaCeros2T):
    """
    El juego del timbiriche para ilustrar los modelos de juegos

    """
    def __init__(self, jugador=1, altura=2, ancho=2):
        """
        Inicializa el juego del timbiriche

        """
        self.x0 = tuple((altura-1)*(ancho-1) * [0])
        self.y0 = tuple(((altura * ancho) + len(self.x0) - 1) * [0])
        self.x = list(self.x0)
        self.y = list(self.y0)
        self.historial = []
        self.jugador = 1

    def jugadas_legales(self):
        return (posicion for posicion in range(len(self.y0)) if self.y[posicion] == 0)

    def terminal(self):
        x = self.x
        jugadorX = 0
        jugadorO = 0
        for box in range(len(x)):
            if x[box] == 1:
                jugadorX += 1
            if x[box] == -1:
                jugadorO += 1
        if (jugadorX + jugadorO) < len(x):
            return None
        if jugadorX > jugadorO:
            return 1
        if jugadorO > jugadorX:
            return -1
        if jugadorX == jugadorO:
            return 0
        
    def hacer_jugada(self, jugada):
        self.historial.append(jugada)
        self.y[jugada] = self.jugador
        self.jugador *= -1
        
    def actualiza_tablero(self, jugada):    
        self.jugador *= -1
        c = 0
        aux = 0
        for i in range(altura - 1):
            for j in range(ancho - 1):
                if(self.x[c] == 0):
                    if (self.y[c + ancho * i] != 0 and 
                        self.y[c + i * ancho + ancho - 1] != 0 and 
                        self.y[c + i * ancho + ancho] != 0 and 
                        self.y[c + i * ancho + 2 * ancho - 1] != 0):
                        self.x[c] = self.jugador
                        aux = 1
                c += 1       
        if aux == 0: 
            self.jugador *= -1

    def deshacer_jugada(self):#PENDIENTE---------------------------------------------
        jugada = self.historial.pop()
        self.y[jugada] = 0
        self.jugador *= -1


def juega_timbiriche(jugador='X', altura=2, ancho=2):
    
    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = Timbiriche(1,altura, ancho)
    
    if jugador is 'O':
        jugada = minimax(juego)
        juego.hacer_jugada(jugada)
    
    acabado = False
    
    while not acabado:
        pprint_timbiriche(juego.x, juego.y, altura, ancho)
        print("\nEscoge una linea juegor ", juego.jugador, ": ")

        try:
            if (juego.jugador == 1):
                jugada = int(input("Jugador X: ".format()))
            else:
                jugada = minimax(juego)
            print()
        except:
            print("¡No seas macana y pon un número!")
            continue
        if jugada < 0 or jugada >= len(juego.y) or juego.y[jugada] != 0:
            print("¡No seas macana, pon un número válido!")
            continue

        juego.hacer_jugada(jugada)
        juego.actualiza_tablero(jugada)
        
        if juego.terminal() is not None:
            acabado = True
            
    pprint_timbiriche(juego.x, juego.y, altura, ancho)
    ganador = juego.terminal()
    if ganador == 0:
        print("UN ASQUEROSO EMPATE".center(60))
    elif (ganador < 0 and jugador is 'X') or (ganador > 0 and jugador is 'O'):
        print("¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?".center(60))
    else:
        print("Ganaste, bye.")
    print("\n\nFin del juego")
    

def pprint_timbiriche(x, y, altura, ancho):

    aux = 0
    for i in range(altura):
        #renglones
        for j in range(ancho-1):
            print("{}".format("+").center(4), end="")
            if y[aux+(i+j)] == 0:
                print("{}".format(aux+(i+j)).center(4), end="")
            else:
                print("{}".format("–").center(4), end="")
        print("{}".format("+").center(4))
        aux += ancho - 1
        
        #auxiliar columnas superior
        if i < altura - 1:
            for j in range(ancho - 1):
                print("{}".format(" ").center(4), end="")
                print("{}".format(" ").center(4), end="")
            print("{}".format(" ").center(4))
        
        #columnas centro
        if i < altura - 1:
            for j in range(ancho - 1):
                #columnas izq
                if y[aux+(i+j)] == 0:
                    print("{}".format(aux+(i+j)).center(4), end="")
                else:
                    print("{}".format("|").center(4), end="")
                #centro cuadro
                if x[(i+j)+(i*(ancho-2))] == 0:
                    print("{}".format(" ").center(4), end="")
                else:
                    if x[(i+j)+(i*(ancho-2))] == 1:
                        print("{}".format("X").center(4), end="")
                    elif(x[(i+j)+(i*(ancho-2))] == -1):
                        print("{}".format("O").center(4), end="")
            #ultima columna
            if y[aux+(i+ancho-1)] == 0:
                print("{}".format(aux+(i+ancho-1)).center(4), end="")
            else:
                print("{}".format("|").center(4), end="")
            print("")
        aux += ancho - 1
        
        #auxiliar columnas inferior
        if i < altura - 1:
            for j in range(ancho):
                print("{}".format(" ").center(4), end="")
                print("{}".format(" ").center(4), end="")
            print("{}".format(" ").center(4))


if __name__ == '__main__':
    altura, ancho = None, None
    while(altura is None):
        try:
            altura = int(input("Elegir la altura del tablero (mayor o igual a 2): ".format(int)))
        except:
            print("¡Pon un número por favor!")
            altura = None
            continue
        if altura < 2:
            print("La altura del tablero debe ser mayor o igual a 2")
            altura = None
            continue
        break
    while(ancho is None):
        try:
            ancho = int(input("Elegir el ancho del tablero (mayor o igual a 2): ".format(int)))
        except:
            print("¡Pon un número por favor!")
            ancho = None
            continue
        if ancho < 2:
            print("El ancho del tablero debe ser mayor o igual a 2")
            ancho = None
            continue
        break
    juega_timbiriche('X', altura, ancho)
    
    
    
    
    
    
    
    
    
    
    
    
    
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

__author__ = 'Cesar Salazar'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):
    """
    Estado inicial del tablero:
        0   0   0   0   0   0   0   0 
        0   0   0   0   0   0   0   0
        0   0   1   0   1   0   0   0
        0   0   0   -1  1   1   0   0
        0   0   1   1  -1   0   0   0
        0   0   0   1   0   1   0   0
        0   0   0   0   0   0   0   0
        0   0   0   0   0   0   0   0
    Las posiciones del tablero son :
        0   1   2   3   4   5   6   7
        8   9   10  11  12  13  14  15
        16  17  18  19  20  21  22  23
        24  25  26  27  28  29  30  31
        32  33  34  35  36  37  38  39
        40  41  42  43  44  45  46  47
        48  49  50  51  52  53  54  55
        56  57  58  59  60  61  62  63
    Las posiciones del centro son las iniciales: 27, 28, 35, 36
    """
    def __init__(self):
        x = [0 for _ in range(64)]
        x[27] = x[36] =-1
        x[28] = x[35] =x[29] =x[34]=x[20] =x[43]=x[18]=x[45]=1
        super().__init__(tuple(x))
        self.turno=1
        #son las casillas que se descartan en las jugadas legales para cada direccion
        self.derecha=[6,7,14,15,22,23,30,31,38,39,46,47,53,55,62,63]
        self.izquierda=[0,1,8,9,16,17,24,25,32,33,40,41,48,49,56,57]
        self.abajo=[i for i in range(48,64)]
        self.arriba=[i for i in range(0,16)]
        #para las diagonales combino las listas dependiendo de que ocupe
        self.dDAbajo=combinarListas(self.derecha,self.abajo)
        self.dIAbajo=combinarListas(self.izquierda,self.abajo)
        self.dDArriba=combinarListas(self.derecha,self.arriba)
        self.dIArriba=combinarListas(self.izquierda,self.arriba)
    #pintar en consola el tablero
    def imprimirTablero(self):
        """
        nomas pa la lista en forma de tablero 
        """
        tablero=np.reshape(self.x.copy(),(8,8))
        print(tablero)
    #funcion para ver si se puede poner en esa casilla
    def esValida(self,jugador,casilla):
        rival=jugador*-1
        fila=casilla//8
        finalFila=8*fila+7
        inicioFila=8*fila
        #Horizontal
        #hacia la derecha
        #si tiene casilla del rival a la derecha
        if casilla not in self.derecha: 
            if self.x[casilla+1] == rival:
                for i in range(casilla+2, finalFila+1):
                    #si encuenta un -1 es valido hacer el movimiento
                    if self.x[i]==jugador: return True 
                    elif self.x[i]==0: return False 
        #hacia la izquierda
        #si tiene casilla del rival a la izquierda
        if casilla not in self.izquierda: 
            if self.x[casilla-1] == rival:
                rangoBusqueda=casilla-2-inicioFila
                for i in range(2,rangoBusqueda+1):
                    if self.x[casilla-i]==jugador: return True 
                    elif self.x[casilla-i]==0: return False
        #Vertical
        #hacia abajo
        #si tiene casilla del rival abajo
        if casilla not in self.abajo: 
            if self.x[casilla+8] == rival:
                for i in range(2,8-fila):
                    if self.x[casilla+i*8]==jugador: return True 
                    elif self.x[casilla+i*8]==0: return False
                return True
        #hacia arriba
        #si tiene casilla del rival abajo
        if casilla not in self.arriba: 
            if self.x[casilla-8] == rival:
                for i in range(2,8+fila):
                    if self.x[casilla-i*8]==jugador: return True 
                    elif self.x[casilla-i*8]==0: return False
                return True
        #diagonales
        #diagonal hacia abajo-derecha
        if casilla not in self.dDAbajo: 
            if self.x[casilla+8+1] == rival:
                for i in range(fila,8-fila):
                    if self.x[casilla+(8*i)+i]==jugador: return True 
                    elif self.x[casilla+(8*i)+i]==0: return False
        #diagonal hacia abajo-izquierda
        if casilla not in self.dIAbajo: 
            if self.x[casilla+8-1] == rival:
                for i in range(fila,8-fila):
                    if self.x[casilla+(8*i)-i]==jugador: return True 
                    elif self.x[casilla+(8*i)-i]==0: return False
        #diagonal hacia arriba-derecha
        if casilla not in self.dDArriba: 
            if self.x[casilla-8+1] == rival:
                for i in range(2,fila):
                    if self.x[casilla-(8*i)+i]==jugador: return True 
                    elif self.x[casilla-(8*i)+i]==0: return False
        #diagonal hacia arriba-izquierd
        if casilla not in self.dIArriba: 
            if self.x[casilla-8-1] == rival:
                for i in range(2,fila):
                    if self.x[casilla-(8*i)-i]==jugador: return True 
                    elif self.x[casilla-(8*i)-i]==0: return False
        return False
    def jugadas_legales(self):
        legales=[]
        legal=False
        for casilla in range(64):
            if self.x[casilla]==0:
                legal=self.esValida(self.turno,casilla) 
                if legal: legales.append(casilla)
        print("\n\nJUGADAS LEGALES PARA :",self.turno," :",legales,"\n\n")
    def terminal(self):
        pass
    def hacer_jugada(self, jugada):
        pass
    def deshacer_jugada(self):
        pass

def combinarListas(lista1,lista2):
    lista=lista1.copy()
    lista.extend([element for element in lista2 if element not in lista1])
    return lista
juego = Othello()
juego.jugadas_legales()
juego.imprimirTablero()
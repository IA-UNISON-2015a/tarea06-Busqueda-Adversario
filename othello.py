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
        0   0   0   0   0   0   0   0
        0   0   0   -1  1   0   0   0
        0   0   0   1  -1   0   0   0
        0   0   0   0   0   0   0   0
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
        x[28] = x[35] =1
        super().__init__(tuple(x))
        self.turno=-1
        self.x_anterior=[]
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
        #tablero=np.reshape(self.x.copy(),(8,8))
        #print(tablero)
        tablero = "┌───┬───┬───┬───┬───┬───┬───┬───┐\n"
        for renglon in range(8):
            for col in range(8):
                tablero += "│"
                tablero += " o " if self.x[ 8*renglon + col ] == 1 else " * " if self.x[8*renglon + col] == -1 else "   "
            tablero += "│\n"
            tablero += "├───┼───┼───┼───┼───┼───┼───┼───┤\n" if renglon < 7 else "└───┴───┴───┴───┴───┴───┴───┴───┘\n"
        
        blancas,negras = self.x.count(1),self.x.count(-1)

        tablero += "*: " + str(blancas) + "\n"
        tablero += "o: " + str(negras) + "\n"

        print(tablero)
    #funcion para ver si se puede poner en esa casilla
    def esValida(self,jugador,casilla):
        #se modifico para que regresara en que direcciones podria voltear para usar en "hacer_jugada"
        rival=jugador*-1
        fila=casilla//8
        finalFila=8*fila+7
        inicioFila=8*fila
        arriba,abajo,derecha,izquierda,dIAbajo,dIArriba,dDArriba,dDAbajo=False,False,False,False,False,False,False,False
        #Horizontal
        #hacia la derecha
        #si tiene casilla del rival a la derecha
        if casilla not in self.derecha: 
            if self.x[casilla+1] == rival:
                for i in range(casilla+2, finalFila+1):
                    #si encuenta un -1 es valido hacer el movimiento
                    if self.x[i]==jugador: 
                        derecha= True
                        break 
                    elif self.x[i]==0: 
                        derecha= False
                        break 
        #hacia la izquierda
        #si tiene casilla del rival a la izquierda
        if casilla not in self.izquierda: 
            if self.x[casilla-1] == rival:
                rangoBusqueda=casilla-2-inicioFila
                for i in range(2,rangoBusqueda+1):
                    if self.x[casilla-i]==jugador: 
                        izquierda= True
                        break 
                    elif self.x[casilla-i]==0: 
                        izquierda= False
                        break
        #Vertical
        #hacia abajo
        #si tiene casilla del rival abajo
        if casilla not in self.abajo: 
            if self.x[casilla+8] == rival:
                for i in range(2,8-fila):
                    if self.x[casilla+i*8]==jugador: 
                        abajo= True
                        break 
                    elif self.x[casilla+i*8]==0: 
                        abajo= False
                        break
        #hacia arriba
        #si tiene casilla del rival abajo
        if casilla not in self.arriba: 
            if self.x[casilla-8] == rival:
                for i in range(2,8+fila):
                    if self.x[casilla-i*8]==jugador: 
                        arriba= True
                        break 
                    elif self.x[casilla-i*8]==0: 
                        arriba= False
                        break
        #diagonales
        #diagonal hacia abajo-derecha
        if casilla not in self.dDAbajo: 
            if self.x[casilla+8+1] == rival:
                for i in range(fila,8-fila-1):
                    if self.x[casilla+(8*i)+i]==jugador: 
                        dDAbajo= True 
                        break
                    elif self.x[casilla+(8*i)+i]==0: 
                        dDAbajo= False
                        break
        #diagonal hacia abajo-izquierda
        if casilla not in self.dIAbajo: 
            if self.x[casilla+8-1] == rival:
                for i in range(fila,8-fila-1):
                    if self.x[casilla+(8*i)-i]==jugador: 
                        dIAbajo= True
                        break 
                    elif self.x[casilla+(8*i)-i]==0: 
                        dIAbajo= False
                        break
        #diagonal hacia arriba-derecha
        if casilla not in self.dDArriba: 
            if self.x[casilla-8+1] == rival:
                for i in range(2,fila):
                    if self.x[casilla-(8*i)+i]==jugador: 
                        dDArriba =True 
                        break
                    elif self.x[casilla-(8*i)+i]==0: 
                        dDArriba= False
                        break
        #diagonal hacia arriba-izquierd
        if casilla not in self.dIArriba: 
            if self.x[casilla-8-1] == rival:
                for i in range(2,fila):
                    if self.x[casilla-(8*i)-i]==jugador: 
                        dIArriba= True 
                        break
                    elif self.x[casilla-(8*i)-i]==0: 
                        dIArriba= False
                        break
        puedeVoltear=[dDAbajo,arriba,dIAbajo,derecha,izquierda,dDArriba,abajo,dIArriba]  
        return puedeVoltear
    def jugadas_legales(self):
        legales=[]
        for casilla in range(64):
            if self.x[casilla]==0: 
                if True in self.esValida(self.turno,casilla): legales.append(casilla)
        #print("\n\nJUGADAS LEGALES PARA :",self.turno," :",legales,"\n\n")            
        return tuple(legales)
    def esTerminal(self):
        jugadas1=len(self.jugadas_legales())
        self.turno*=-1
        jugadas2=len(self.jugadas_legales())
        self.turno*=-1
        if jugadas1 == 0:
            if jugadas2 == 0:
                blancas = self.x.count(-1)
                negras = self.x.count(1)
                return 1 if blancas < negras else -1 if negras < blancas else 0
        return None

    def hacer_jugada(self, jugada):
        self.x_anterior.append(self.x[:])
        self.historial.append(jugada)
        self.x[jugada] = self.jugador
        self.jugador *= -1
    def deshacer_jugada(self):
        pass
#para combinar las listas d eno posibles en la diagonal
def combinarListas(lista1,lista2):
    lista=lista1.copy()
    lista.extend([element for element in lista2 if element not in lista1])
    return lista
if __name__ == '__main__':
    juego = Othello()
    juego.jugadas_legales()
    juego.imprimirTablero()
    #juego.hacer_jugada(19)
    #juego.imprimirTablero()
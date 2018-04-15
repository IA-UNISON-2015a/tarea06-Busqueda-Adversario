#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
othello.py
------------

El juego de Otello implementado por ustedess mismos, con jugador inteligente

"""

__author__ = 'Jordan Urias'

import copy
import os

class othello():
    def __init__(self, _n=8):
        self.n = _n
        self.tablero = [['0' for x in range(self.n)] for y in range(self.n)]
        # 8 direcciones
        self.dirx = [-1,  0,  1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1,  0, 0,  1, 1, 1]
        self.minUtilidadTablero = -1 
        self.maxUtilidadTablero = self.n * self.n + 4 * self.n + 4 + 1 
        
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
    
    '''
    Asumimos que el movimiento es legal.
    '''
    def hacerMoviento(self, tablero, x, y, jugador): 
        numFichasOpp = 0 # Fichas ganadas
        tablero[y][x] = jugador
        for d in range(8): # Son las direcciones posibles
            fichasOpp = 0
            for i in range(self.n):
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                if dx < 0 or dx > self.n - 1 or dy < 0 or dy > self.n - 1:#salimos del tablero
                    fichasOpp = 0; 
                    break
                elif tablero[dy][dx] == jugador:#topamos con una ficha igual
                    break
                elif tablero[dy][dx] == '0':#topamos con casilla vacia
                    fichasOpp = 0; 
                    break
                else:
                    fichasOpp += 1
            for i in range(fichasOpp):#cambiamos las fichas
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                tablero[dy][dx] = jugador
            numFichasOpp += fichasOpp
        return (tablero, numFichasOpp)
    
    def esLegal(self,tablero, x, y, jugador):
        if x < 0 or x > self.n - 1 or y < 0 or y > self.n - 1:
            return False
        if tablero[y][x] != '0':
            return False
        (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
        if numFichasOpp == 0:
            return False
        return True
    
    def esJugadaTerminal(self, tablero, jugador):
        for y in range(self.n):
            for x in range(self.n):
                if self.esLegal(tablero, x, y, jugador):
                    return False
        return True

    def getJugadaOrd(self, tablero, jugador):
        jugadasOrdenadas = []
        for y in range(self.n):
            for x in range(self.n):
                if self.esLegal(tablero, x, y, jugador):
                    (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
                    jugadasOrdenadas.append((tableroTemp, self.UtilidadTablero(tableroTemp, jugador)))
        jugadasOrdenadas = sorted(jugadasOrdenadas, key = lambda node: node[1], reverse = True)
        jugadasOrdenadas = [node[0] for node in jugadasOrdenadas]
        return jugadasOrdenadas
    
    
    def Minimax(self, tablero, jugador, prof, maximizarjugador):
        if prof == 0 or self.esJugadaTerminal(tablero, jugador):
            return self.UtilidadTablero(tablero, jugador)
        if maximizarjugador:
            mejorUtilidad = self.minUtilidadlTablero
            for y in range(self.n):
                for x in range(self.n):
                    if self.esLegal(tablero, x, y, jugador):
                        (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
                        v = self.Minimax(tableroTemp, jugador, prof - 1, False)
                        mejorUtilidad = max(mejorUtilidad, v)
        else: # minimizargjugador
            mejorUtilidad = self.maxUtilidadlTablero
            for y in range(self.n):
                for x in range(self.n):
                    if self.esLegal(tablero, x, y, jugador):
                        (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
                        v = self.Minimax(tableroTemp, jugador, prof - 1, True)
                        mejorUtilidad = min(mejorUtilidad, v)
        return mejorUtilidad
    
    def AlphaBeta(self, tablero, jugador, prof, alpha, beta, maximizarjugador):
        if prof == 0 or self.esJugadaTerminal(tablero, jugador):
            return self.UtilidadTablero(tablero, jugador)
        jugadasOrdenadas = self.getJugadaOrd(tablero, jugador)
        if maximizarjugador:
            v = self.minUtilidadTablero
            for tableroTemp in jugadasOrdenadas:
                v = max(v, self.AlphaBeta(tableroTemp, jugador, prof - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break # poda de beta
            return v
        else: # minimizar jugador
            v = self.maxUtilidadTablero
            for tableroTemp in jugadasOrdenadas:
                v = min(v, self.AlphaBeta(tableroTemp, jugador, prof - 1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    break # poda de alpha
            return v


    def MejorMovimientoUtilidad(self,tablero, jugador, prof):
        maxpuntos = 0
        mx = -1; my = -1
        for y in range(self.n):
            for x in range(self.n):
                if self.esLegal(tablero, x, y, jugador):
                    (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
                    puntos = self.UtilidadlTablero(tableroTemp, jugador) 
                    if puntos > maxpuntos:
                        maxpuntos = puntos
                        mx = x; my = y
        return (mx, my)
    
    def MejorMovimientoMinimax(self,tablero, jugador, prof):
        maxpuntos = 0
        mx = -1; my = -1
        for y in range(self.n):
            for x in range(self.n):
                if self.esLegal(tablero, x, y, jugador):
                    (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
                    puntos = self.Minimax(tableroTemp, jugador, prof, True)
                    if puntos > maxpuntos:
                        maxpuntos = puntos
                        mx = x; my = y
        return (mx, my)
    
    def MejorMovimientoAlphaBeta(self,tablero, jugador, prof):
        maxpuntos = 0
        mx = -1; my = -1
        for y in range(self.n):
            for x in range(self.n):
                if self.esLegal(tablero, x, y, jugador):
                    (tableroTemp, numFichasOpp) = self.hacerMoviento(copy.deepcopy(tablero), x, y, jugador)
                    puntos = self.AlphaBeta(tablero, jugador, prof, self.minUtilidadTablero, self.maxUtilidadTablero, True)
                    if puntos > maxpuntos:
                        maxpuntos = puntos
                        mx = x; my = y
        return (mx, my)
    
if __name__ == '__main__':
    juego=othello()
    prof = 4
    while True:
        for p in range(2):
            print
            juego.PrintTablero()
            jugador = str(p + 1)
            print ('jugador: ' + jugador)
            if juego.esJugadaTerminal(juego.tablero, jugador):
                print ('jugador no puede jugar! Game over!')
                print ('puntaje jugador: ' + str(juego.UtilidadlTablero(juego.tablero, '1')))
                print ('puntaje AI  : ' + str(juego.UtilidadlTablero(juego.tablero, '2')))
                os._exit(0)            
            if jugador == '1':
                while True:
                    xy = input('X Y: ')
                    if xy == '': os._exit(0)
                    (x, y) = xy.split()
                    x = int(x); y = int(y)
                    if juego.esLegal(juego.tablero, x, y, jugador):
                        (juego.tablero, numFichasOpp) = juego.hacerMoviento(juego.tablero, x, y, jugador)
                        print ('Piezas adquiridas: ' + str(numFichasOpp))
                        break
                    else:
                        print ('Movimiento invalido!')
            else: # 
                (x, y) = juego.MejorMovimientoAlphaBeta(juego.tablero, jugador,prof)
                if not (x == -1 and y == -1):
                    (juego.tablero, numFichasOpp) = juego.hacerMoviento(juego.tablero, x, y, jugador)
                    print ('AI jugo (X Y): ' + str(x) + ' ' + str(y))
                    print ('Piezas adquiridas: ' + str(numFichasOpp))
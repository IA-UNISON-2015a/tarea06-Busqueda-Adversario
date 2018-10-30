#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'nombre del alumno'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
import os, copy
n = 8 # tamanio del tablero
tablero = [['0' for x in range(n)] for y in range(n)]
# 8 direcciones
dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]

def InitTablero():
    if n % 2 == 0: # checa si el tablero es parejo
        z = (n - 2) // 2
        tablero[z][z] = '2'
        tablero[n - 1 - z][z] = '1'
        tablero[z][n - 1 - z] = '1'
        tablero[n - 1 - z][n - 1 - z] = '2'

def imprime_tablero():
    m = len(str(n - 1))
    for y in range(n):
        row = ''
        for x in range(n):
            row += tablero[y][x]
            row += ' ' * m
        print (row + ' ' + str(y))
    print
    row = ''
    for x in range(n):
        row += str(x).zfill(m) + ' '
    print (row + '\n')


def movida(tablero, x, y, jugador):
    totctr = 0 # numero de piezas obtenidas del oponente
    tablero[y][x] = jugador
    for d in range(8):
        ctr = 0
        for i in range(n):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                ctr = 0; break
            elif tablero[dy][dx] == jugador:
                break
            elif tablero[dy][dx] == '0':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            tablero[dy][dx] = jugador
        totctr += ctr
    return (tablero, totctr)

def jugada_valida(tablero, x, y, jugador):
    if x < 0 or x > n - 1 or y < 0 or y > n - 1:
        return False
    if tablero[y][x] != '0':
        return False
    (tableroTemp, totctr) = movida(copy.deepcopy(tablero), x, y, jugador)
    if totctr == 0:
        return False
    return True

minEvaltablero = -1 # min - 1
maxEvaltablero = n * n + 4 * n + 4 + 1 # max + 1
def eval_tablero(tablero, jugador):
    tot = 0
    for y in range(n):
        for x in range(n):
            if tablero[y][x] == jugador:
                if (x == 0 or x == n - 1) and (y == 0 or y == n - 1):
                    tot += 4 # esquina
                elif (x == 0 or x == n - 1) or (y == 0 or y == n - 1):
                    tot += 2 # lado
                else:
                    tot += 1
    return tot

# Si no hay movimiento posible regresa True
def es_meta(tablero, jugador):
    for y in range(n):
        for x in range(n):
            if jugada_valida(tablero, x, y, jugador):
                return False
    return True


def Minimax(tablero, jugador, depth, maxJugador):
    if depth == 0 or es_meta(tablero, jugador):
        return eval_tablero(tablero, jugador)
    if maxJugador:
        val = minEvaltablero
        for y in range(n):
            for x in range(n):
                if jugada_valida(tablero, x, y, jugador):
                    (tableroTemp, totctr) = movida(copy.deepcopy(tablero), x, y, jugador)
                    v = Minimax(tableroTemp, jugador, depth - 1, False)
                    val = max(val, v)
    else: # minimiza
        val = maxEvaltablero
        for y in range(n):
            for x in range(n):
                if jugada_valida(tablero, x, y, jugador):
                    (tableroTemp, totctr) = movida(copy.deepcopy(tablero), x, y, jugador)
                    v = Minimax(tableroTemp, jugador, depth - 1, True)
                    val = min(val, v)
    return val

def mejor_movimiento(tablero, jugador):
    maxPuntos = 0
    mx = -1; my = -1
    for y in range(n):
        for x in range(n):
            if jugada_valida(tablero, x, y, jugador):
                (tableroTemp, totctr) = movida(copy.deepcopy(tablero), x, y, jugador)
                if opt == 0:
                    puntos = eval_tablero(tableroTemp, jugador)
                elif opt == 1:
                    puntos = Minimax(tableroTemp, jugador, depth, True)
                if puntos > maxPuntos:
                    maxPuntos = puntos
                    mx = x; my = y
    return (mx, my)

print ('REVERSI/OTHELLO tablero')
print ('0: eval_tablero')
print ('1: Minimax')
opt = int(input('Selecciona: '))
if opt is 1:
    depth = 4
    depthStr = input('Selecciona la profundidad de la busqueda(DEFAULT: 4): ')
    if depthStr != '': depth = int(depth)
print ('\n1:  2: CPU (presiona enter para salir)')
InitTablero()
while True:
    for p in range(2):
        print
        imprime_tablero()
        jugador = str(p + 1)
        print ('jugador: ' + jugador)
        if es_meta(tablero, jugador):
            print ('El jugador ya no puede jugar... SE ACABO!')
            print ('Puntos del jugador: ' + str(eval_tablero(tablero, '1')))
            print ('Puntos del CPU  : ' + str(eval_tablero(tablero, '2')))
            os._exit(0)
        if jugador == '1':
            while True:
                xy = input('X Y: ')
                if xy == '': os._exit(0)
                (x, y) = xy.split()
                x = int(x); y = int(y)
                if jugada_valida(tablero, x, y, jugador):
                    (tablero, totctr) = movida(tablero, x, y, jugador)
                    print ('# de fichas obtenidas: ' + str(totctr))
                    break
                else:
                    print ('Movimiento invalido... el que no tranza no avanza!')
        else: # CPU
            (x, y) = mejor_movimiento(tablero, jugador)
            if not (x == -1 and y == -1):
                (tablero, totctr) = movida(tablero, x, y, jugador)
                print ('CPU jugo (X Y): ' + str(x) + ' ' + str(y))
                print ('# de piezas obtenidas: ' + str(totctr))

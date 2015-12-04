#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Luis Fernando Suarez Astiazaran'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

import juegos_cuadricula
import time
import random

class Othello(juegos_cuadricula.Juego2ZT):
    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y renglones y el estado inicial del juego.

                         0   1   2   3   4   5   6   7
                         8   9  10  11  12  13  14  15
                        16  17  18  19  20  21  22  23
                        24  25  26  27  28  29  30  31
                        32  33  34  35  36  37  38  39
                        40  41  42  43  44  45  46  47
                        48  49  50  51  52  53  54  55
                        56  57  58  59  60  61  62  63
        """
        juegos_cuadricula.Juego2ZT.__init__(self, 8, 8, tuple([0 for i in range(64)]))
        temp = list(self.estado_inicial)
        temp[27] = temp[36] =  1
        temp[28] = temp[35] = -1
        self.estado_inicial = tuple(temp)

        self.bases = range(56, 63)

        def f_combinaciones(pos):
            """
            Funcion interna para encontrar todas las combinaciones de una posición

            """
            combinaciones = []
            # Columna
            if pos < 21:
                combinaciones.append(range(pos, pos + 22, 7))
                # Renglones y diagonales
            for i in range(0, 4):
                if 0 <= pos % 7 - i < 4:
                    # Renglones
                    combinaciones.append(range(pos - i, pos - i + 4))
                    # Diagonal hacia abajo
                    pos_d = pos - 8 * i
                    if 0 <= pos_d < 18:
                        combinaciones.append(range(pos_d, pos_d + 25, 8))
                        # Diagonal hacia arriba
                    pos_d = pos + 6 * i
                    if 20 < pos_d < 39:
                        combinaciones.append(range(pos_d, pos_d - 19, -6))
            return tuple(combinaciones)

        self.combinaciones = {i: f_combinaciones(i) for i in range(42)}

    def jugadas_legales(self, estado, jugador):

        def esLegal(jugada, estado, jugador):
            e = estado[:]
            r = jugada[1] / self.columnas
            c = jugada[1] % self.columnas
            #Buscar jugada O
            for i in range(1, self.columnas):
                if c + i < self.columnas:
                    if e[(r * self.columnas) + (c + i)] == 0:
                        break
                    if e[(r * self.columnas) + (c + i)] == -jugador:
                        continue
                    if e[(r * self.columnas) + (c + i)] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada E
            for i in range(1, self.columnas):
                if c - i >= 0:
                    if e[(r * self.columnas) + (c - i)] == 0:
                        break
                    if e[(r * self.columnas) + (c - i)] == -jugador:
                        continue
                    if e[(r * self.columnas) + (c - i)] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada S
            for i in range(1, self.renglones):
                if r + i < self.renglones:
                    if e[((r + i) * self.columnas) + c] == 0:
                        break
                    if e[((r + i) * self.columnas) + c] == -jugador:
                        continue
                    if e[((r + i) * self.columnas) + c] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada N
            for i in range(1, self.renglones):
                if r - i >= 0:
                    if e[((r - i) * self.columnas) + c] == 0:
                        break
                    if e[((r - i) * self.columnas) + c] == -jugador:
                        continue
                    if e[((r - i) * self.columnas) + c] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada SO
            for i in range(1, (self.columnas + self.renglones) / 2):
                if r + i < self.renglones and c + i < self.columnas:
                    if e[((r + i) * self.columnas) + (c + i)] == 0:
                        break
                    if e[((r + i) * self.columnas) + (c + i)] == -jugador:
                        continue
                    if e[((r + i) * self.columnas) + (c + i)] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada NE
            for i in range(1, (self.columnas + self.renglones) / 2):
                if r - i >= 0 and c - i >= 0:
                    if e[((r - i) * self.columnas) + (c - i)] == 0:
                        break
                    if e[((r - i) * self.columnas) + (c - i)] == -jugador:
                        continue
                    if e[((r - i) * self.columnas) + (c - i)] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada SE
            for i in range(1, (self.columnas + self.renglones) / 2):
                if r + i < self.renglones and c - i >= 0:
                    if e[((r + i) * self.columnas) + (c - i)] == 0:
                        break
                    if e[((r + i) * self.columnas) + (c - i)] == -jugador:
                        continue
                    if e[((r + i) * self.columnas) + (c - i)] == jugador:
                        if i > 1:
                            return 1
                        break

                #Buscar jugada NO
            for i in range(1,(self.columnas + self.renglones) / 2):
                if r - i >= 0 and c + i < self.columnas:
                    if e[((r - i) * self.columnas) + (c + i)] == 0:
                        break
                    if e[((r - i) * self.columnas) + (c + i)] == -jugador:
                        continue
                    if e[((r - i) * self.columnas) + (c + i)] == jugador:
                        if i > 1:
                            return 1
                        break
            return 0

        e = estado[:]
        jugadas = []
        for i in range(len(e)):
            if e[i] == 0:
                if esLegal((None, i), e, jugador):
                    jugadas.append((None, i))
        return jugadas

    def estado_terminal(self, estado):
        """
        Devuelve 1 si el estado es final y gana el jugador 1,
                -1 si el estado es final y gana el jugador -1,
                 0 si es terminal y hay empate
                 None si el estado no es terminal
        """
        jugadas1 = self.jugadas_legales(estado, 1)
        jugadas2 = self.jugadas_legales(estado, -1)
        e = estado[:]

        if len(jugadas1) == 0 and len(jugadas2) == 0:
            #showinfo("Fin del juego","No quedan jugadas legales")
            total = 0
            for v in e:
                total += v
            if total == 0:
                return total
            if total > 0:
                return 1
            return -1

        if e.count(0) > 0:
            return None

        total = 0
        for v in e:
            total += v
        if total == 0:
            return total
        if total > 0:
            return 1
        return -1

    def hacer_jugada(self, estado, jugada, jugador):
        # jugada = list(jugadas)
        if jugada[1] == None:
            return estado
        e = list(estado[:])
        e[jugada[1]] = jugador

        r = jugada[1] / 8
        c = jugada[1] % 8

        #Hacer jugada O
        for i in range(1,8):
            if c + i < 8:
                if e[(r * 8) + (c + i)] == 0:
                    break
                if e[(r * 8) + (c + i)] == -jugador:
                    continue
                if e[(r * 8) + (c + i)] == jugador:
                    if i > 1:
                        for j in range(1, i + 1):
                            e[(r * 8) + (c + j)] = jugador
                    break
            #Hacer jugada E
        for i in range(1,8):
            if c - i >= 0:
                if e[(r * 8) + (c - i)] == 0:
                    break
                if e[(r * 8)+(c - i)] == -jugador:
                    continue
                if e[(r * 8)+(c - i)] == jugador:
                    if i > 1:
                        for j in range(1, i + 1):
                            e[(r * 8) + (c - j)] = jugador
                    break
            #Hacer jugada S
        for i in range(1, 8):
            if r + i < 8:
                if e[((r + i) * 8) + c] == 0:
                    break
                if e[((r + i) * 8) + c] == -jugador:
                    continue
                if e[((r + i) * 8) + c] == jugador:
                    if i > 1:
                        for j in range(1, i + 1):
                            e[((r + j) * 8) + c] = jugador
                    break
            #Hacer jugada N
        for i in range(1,8):
            if r - i >= 0:
                if e[((r - i) * 8) + c] == 0:
                    break
                if e[((r - i) * 8) + c] == -jugador:
                    continue
                if e[((r - i) * 8) + c] == jugador:
                    if i > 1:
                        for j in range(1, i + 1):
                            e[((r - j) * 8) + c] = jugador
                    break
            #Hacer jugada SO
        for i in range(1, (8 + 8) / 2):
            if r + i < 8 and c + i < 8:
                if e[((r + i) * 8) + (c + i)] == 0:
                    break
                if e[((r + i) * 8) + (c + i)] == -jugador:
                    continue
                if e[((r + i) * 8) + (c + i)] == jugador:
                    if i > 1:
                        for j in range (1, i + 1):
                            e[((r + j) * 8) + (c + j)] = jugador
                    break

        #Hacer jugada NE
        for i in range(1, (8 + 8) / 2):
            if r - i >= 0 and c - i >= 0:
                if e[((r - i) * 8) + (c - i)] == 0:
                    break
                if e[((r - i) * 8) + (c - i)] == -jugador:
                    continue
                if e[((r - i) * 8) + (c - i)] == jugador:
                    if i > 1:
                        for j in range (1,i+1):
                            e[((r - j) * 8) + (c - j)] = jugador
                    break

        #Hacer jugada SE
        for i in range(1, (8 + 8) / 2):
            if r + i < 8 and c - i >= 0:
                if e[((r + i) * 8) + (c - i)] == 0:
                    break
                if e[((r + i) * 8) + (c - i)] == -jugador:
                    continue
                if e[((r + i) * 8) + (c - i)] == jugador:
                    if i > 1:
                        for j in range (1, i + 1):
                            e[((r + j) * 8) + (c - j)] = jugador
                    break
            #Hacer jugada NO
        for i in range(1, (8 + 8) / 2):
            if r - i >= 0 and c + i < 8:
                if e[((r - i) * 8) + (c + i)] == 0:
                    break
                if e[((r - i) * 8) + (c + i)] == -jugador:
                    continue
                if e[((r - i) * 8) + (c + i)] == jugador:
                    if i > 1:
                        for j in range (1,i+1):
                            e[((r - j) * 8) + (c + j)] = jugador
                    break
        return tuple(e)

def encuentra(tupla, valor):
    try:
        return tupla.index(valor)
    except ValueError:
        return None


class JugadorOthello(juegos_cuadricula.JugadorNegamax):
    def __init__(self, tiempo_espera=10):
        juegos_cuadricula.JugadorNegamax.__init__(self, d_max=1)
        self.tiempo = tiempo_espera
        self.maxima_d = 20

    def ordena(self, juego, estado, jugadas):
        return jugadas

    def utilidad(self, juego, estado):

        pesos = [10, 10, 10, 10, 10, 10, 10, 10,
                 10,  9,  9,  9,  9,  9,  9, 10,
                 10,  9,  8,  8,  8,  8,  9, 10,
                 10,  9,  8,  0,  0,  8,  9, 10,
                 10,  9,  8,  0,  0,  8,  9, 10,
                 10,  9,  8,  8,  8,  8,  9, 10,
                 10,  9,  9,  9,  9,  9,  9, 10,
                 10, 10, 10, 10, 10, 10, 10, 10]
        val = 0
        for i in range(len(pesos)):
            if estado[i] == 0:
                val += pesos[i]
        return val

    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego, estado, juego.jugadas_legales(estado, jugador)),
                         key=lambda jugada: -self.negamax(juego,
                                                          estado=juego.hacer_jugada(estado, jugada, jugador),
                                                          jugador=-jugador,
                                                          alpha=-1e10,
                                                          beta=1e10,
                                                          profundidad=self.dmax))
            self.dmax += 1
        return jugada

if __name__ == '__main__':

    # Ejemplo donde empieza el jugador humano
    juego = juegos_cuadricula.InterfaseTK(Othello(),
                                          juegos_cuadricula.JugadorHumano(),
                                          JugadorOthello(1),
                                          1)
    juego.arranca()

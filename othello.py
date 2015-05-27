#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Juan Manuel Cruz Luque'

import juegos_cuadricula
import time

# -------------------------------------------------------------------------
# (60 puntos)
# INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class Othello(juegos_cuadricula.Juego2ZT):
    def __init__(self):

        juegos_cuadricula.Juego2ZT.__init__(self, 8, 8, tuple([0 for _ in range(64)]))
        cuadricula = list(self.estado_inicial)
        cuadricula[27] = 1
        cuadricula[36] = 1
        cuadricula[28] = -1
        cuadricula[35] = -1
        self.estado_inicial = tuple(cuadricula)

    def revisar(self, estado, jugador, renglon, columna):

        def obtener_indice(columna, renglon):
            return columna + renglon * 8

        if jugador == 1:
            jugador2 = -1
        else:
            jugador2 = 1

        lugares = []

        e = list(estado)

        if renglon < 0 or renglon > 7 or columna < 0 or columna > 7:
            return lugares

        # NORTE
        i = renglon - 1
        if i >= 0 and e[obtener_indice(i, columna)] == jugador2:
            i -= 1
            while i >= 0 and e[obtener_indice(i, columna)] == jugador2:
                i -= 1
            if i >= 0 and e[obtener_indice(i, columna)] == 0:
                valor = obtener_indice(i, columna)
                temp = tuple((None, valor))
                lugares.append(temp)

        # NORESTE
        i = renglon - 1
        j = columna + 1
        if i >= 0 and j < 8 and e[obtener_indice(i, j)] == jugador2:
            i -= 1
            j += 1
            while i >= 0 and j < 8 and e[obtener_indice(i, j)] == jugador2:
                i -= 1
                j += 1
            if i >= 0 and j < 8 and e[obtener_indice(i, j)] == 0:
                valor = obtener_indice(i, j)
                temp = tuple((None, valor))
                lugares.append(temp)

        # ESTE
        j = columna + 1
        if j < 8 and e[obtener_indice(renglon, j)] == jugador2:
            j += 1
            while j < 8 and e[obtener_indice(renglon, j)] == jugador2:
                j += 1
            if j < 8 and e[obtener_indice(renglon, j)] == 0:
                valor = obtener_indice(renglon, j)
                temp = tuple((None, valor))
                lugares.append(temp)

        # SURESTE
        i = renglon + 1
        j = columna + 1
        if i < 8 and j < 8 and e[obtener_indice(i, j)] == jugador2:
            i += 1
            j += 1
            while i < 8 and j < 8 and e[obtener_indice(i, j)] == jugador2:
                i += 1
                j += 1
            if i < 8 and j < 8 and e[obtener_indice(i, j)] == 0:
                valor = obtener_indice(i, j)
                temp = tuple((None, valor))
                lugares.append(temp)

        # SUR
        i = renglon + 1
        if i < 8 and e[obtener_indice(i, columna)] == jugador2:
            i += 1
            while i < 8 and e[obtener_indice(i, columna)] == jugador2:
                i += 1
            if i < 8 and e[obtener_indice(i, columna)] == 0:
                valor = obtener_indice(i, columna)
                temp = tuple((None, valor))
                lugares.append(temp)

        # SUROESTE
        i = renglon + 1
        j = columna - 1
        if i < 8 and j >= 0 and e[obtener_indice(i, j)] == jugador2:
            i += 1
            j -= 1
            while i < 8 and j >= 0 and e[obtener_indice(i, j)] == jugador2:
                i += 1
                j -= 1
            if i < 8 and j >= 0 and e[obtener_indice(i, j)] == 0:
                valor = obtener_indice(i, j)
                temp = tuple((None, valor))
                lugares.append(temp)

        # OESTE
        j = columna - 1
        if j >= 0 and e[obtener_indice(renglon, j)] == jugador2:
            j -= 1
            while j >= 0 and e[obtener_indice(renglon, j)] == jugador2:
                j -= 1
            if j >= 0 and e[obtener_indice(renglon, j)] == 0:
                valor = obtener_indice(renglon, j)
                temp = tuple((None, valor))
                lugares.append(temp)

        # NOROESTE
        i = renglon - 1
        j = columna - 1
        if i >= 0 and j >= 0 and e[obtener_indice(i, j)] == jugador2:
            i -= 1
            j -= 1
            while i >= 0 and j >= 0 and e[obtener_indice(i, j)] == jugador2:
                i -= 1
                j -= 1
            if i >= 0 and j >= 0 and e[obtener_indice(i, j)] == 0:
                valor = obtener_indice(i, j)
                temp = tuple((None, valor))
                lugares.append(temp)

        return lugares

    def jugadas_legales(self, estado, jugador):


        def obtener_indice(columna, renglon):
            return columna + renglon * 8

        e = list(estado)
        lugares = []

        for i in xrange(8):
            for j in xrange(8):
                if e[obtener_indice(i, j)] == jugador:
                    lugares = lugares + self.revisar(estado, jugador, i, j)

        lugares = list(set(lugares))

        return lugares

    def hacer_jugada(self, estado, jugada, jugador):

        e = list(estado)
        e[jugada[1]] = jugador
        return tuple(e)

    def contar_piezas(self, estado):

        def obtener_indice(columna, renglon):
            return columna + renglon * 8

        e = list(estado)

        j1 = 0
        j2 = 0

        for c in xrange(8):
            for r in xrange(8):
                if e[obtener_indice(c, r)] == 1:
                    j1 += 1
                elif e[obtener_indice(c, r)] == -1:
                    j2 += 1

        return j1, j2

    def estado_terminal(self, estado, jugador):

        jugadas1 = self.jugadas_legales(estado, jugador)
        jugadas2 = self.jugadas_legales(estado, -jugador)

        e = list(estado)

        if len(jugadas1) == 0 and len(jugadas2) == 0:

            j1, j2 = self.contar_piezas(estado)

            if j1 > j2:
                return 1
            elif j1 == j2:
                return 0
            else:
                return -1
        else:
            if 0 not in e:
                return 0
        return None


class JugadorOthello(juegos_cuadricula.JugadorNegamax):
    def __init__(self, tiempo_espera=10):
        """
        Inicializa el jugador limitado en tiempo y no en profundidad
        """
        juegos_cuadricula.JugadorNegamax.__init__(self, d_max=1)
        self.tiempo = tiempo_espera
        self.maxima_d = 20

    def ordena(self, juego, estado, jugadas, jugador):

        jugadas_ordenadas = []

        for j in jugadas:
            jugada_temp = juego.hacer_jugada(estado, j, jugador)
            cont1, cont2 = juego.contar_piezas(jugada_temp)

            valor = tuple((cont1, tuple(j)))
            jugadas_ordenadas.append(valor)

            jugadas_ordenadas.sort(key=lambda x: x[0], reverse=True)
            jugadas = [i[1] for i in jugadas_ordenadas]

        return jugadas

    def utilidad(self, juego, estado, jugador):

        val = juego.estado_terminal(estado, jugador)
        if val is None:
            return 0
        return val

    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego,
                                     estado,
                                     juego.jugadas_legales(estado, jugador),
                                     jugador),
                         key=lambda jugada: -self.negamax(juego,
                                                          estado=juego.hacer_jugada(estado, jugada, jugador),
                                                          jugador=-jugador,
                                                          alpha=-1e10,
                                                          beta=1e10,
                                                          profundidad=self.dmax))
            # print "A profundad ", self.dmax, " la mejor jugada es ", jugada
            self.dmax += 1
        return jugada


if __name__ == '__main__':
    # Ejemplo donde empieza el jugador humano
    juego = juegos_cuadricula.InterfaseTK(Othello(),
                                          juegos_cuadricula.JugadorHumano(),
                                          JugadorOthello(1), 1)
    juego.arranca()
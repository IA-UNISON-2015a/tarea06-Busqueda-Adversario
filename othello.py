#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'nombre del alumno'
import os
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from random import shuffle
import tkinter as tk

class Donathello(JuegoSumaCeros2T):
    def __init__(self):
        '''
                 0,0  0,1  0,2  0,3  0,4  0,5  0,6  0,7
                 1,0  1,1  1,2  1,3  1,4  1,5  1,6  1,7
                 2,0  2,1  2,2  2,3  2,4  2,5  2,6  2,7
                 3,0  3,1  3,2  3,3  3,4  3,5  3,6  3,7
                 4,0  4,1  4,2  4,3  4,4  4,5  4,6  4,7
                 5,0  5,1  5,2  5,3  5,4  5,5  5,6  5,7
                 6,0  6,1  6,2  6,3  6,4  6,5  6,6  6,7
                 7,0  7,1  7,2  7,3  7,4  7,5  7,6  7,7
        '''
        super().__init__([ [0] * 8 for _ in range(8) ])
        self.x[3][3] = 1
        self.x[3][4] = -1
        self.x[4][3] = 1
        self.x[4][4] = -1

    def oye_eso_es_legal(self, i, j):
        if self.x[i][j] == 0:
            for ca,k in ((-1,-1), (-1,0), (1,1), (0,-1), (0,1), (1,0), (-1,1), (1,-1)):
                isita, jotita = i, j
                frog = 0
                while True:
                    isita += ca
                    jotita += k
                    if not 0 <= isita <= 7 or not 0 <= jotita <= 7:
                        break
                    actual = self.x[isita][jotita]
                    if actual == 0:
                        break
                    elif frog == 0 and actual == self.jugador:
                        break
                    elif frog == 1 and actual == self. jugador:
                        return True
                    else:
                        frog = 1 if self.x[isita][jotita] == -self.jugador else 0

        return False

    def jugadas_legales(self):
        return [(i,j) for i in range(8) for j in range(8) if self.oye_eso_es_legal(i,j)]

    def terminal(self):
        jugador_1 = 0
        jugador_2 = 0
        for i in range(8):
            for j in range(8):
                if self.x[i][j] == 0:
                    return None
                elif self.x[i][j] == 1:
                    jugador_1 += 1
                else:
                    jugador_2 += 1
        if jugador_1 > jugador_2:
            return 1
        else:
            return -1

    def hacer_jugada(self, jugada):
        i,j = jugada
        self.historial.append([fila[:] for fila in self.x])
        self.x[i][j] = self.jugador

        for ca,k in ((-1,-1), (-1,0), (1,1), (0,-1), (0,1), (1,0), (-1,1), (1,-1)):
            isita, jotita = i, j
            frog = 0
            aux = []
            while True:
                isita += ca
                jotita += k
                if not 0 <= isita <= 7 or not 0 <= jotita <= 7:
                    break
                actual = self.x[isita][jotita]
                if actual == 0:
                    break
                elif frog == 0 and actual == self.jugador:
                    break
                elif frog == 1 and actual == self.jugador:
                    for c,k in aux:
                        self.x[c][k] = self.jugador
                    break
                else:
                    frog = 1
                    aux.append((isita, jotita))
        self.jugador = -self.jugador

    def deshacer_jugada(self):
        self.x = self.historial.pop()

    def dibuja_tablero(self):
        """
                Método para dibujar el tablero, lo dibuja en el siguiente formato:
                   A   B   C   D   E   F   G   H
                 ┌───┬───┬───┬───┬───┬───┬───┬───┐
                1│   │   │   │   │   │   │   │   │
                 ├───┼───┼───┼───┼───┼───┼───┼───┤
                2│   │   │   │   │   │   │   │   │
                 ├───┼───┼───┼───┼───┼───┼───┼───┤
                3│   │   │   │   │   │   │   │   │
                 ├───┼───┼───┼───┼───┼───┼───┼───┤
                4│   │   │   │ ☺ │ ☻ │   │   │   │
                 ├───┼───┼───┼───┼───┼───┼───┼───┤
                5│   │   │   │ ☻ │ ☺ │   │   │   │
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
                tablero += " ☺ " if self.x[reng][col] == 1 else " ☻ " if self.x[reng][col] == -1 else "   "
            tablero += "│\n"
            tablero += " ├───┼───┼───┼───┼───┼───┼───┼───┤\n" if reng < 7 else " └───┴───┴───┴───┴───┴───┴───┴───┘\n"

        blancas, negras = self.x.count(1), self.x.count(-1)

        tablero += "☺: " + str(blancas) + "\n"
        tablero += "☻: " + str(negras) + "\n"

        print(tablero)

    def esta_fuera_tablero(self, reng, col):
        """
        Este método revisa si dados un renglón y un columna son coordenadas válidas para el tablero.
        @return: un booleano.
        """
        return (reng < 0 or reng > 7 or col < 0 or col > 7)

    def es_valido(self, reng, col):
        """
        este método dice si una casilla es válida para poner una pieza en ella.
        @param reng: renglon de la casilla
        @param col: columna de la casilla
        @return: una lista con las direcciones en las cuales
                 puede voltear piezas, vacía si es un movimiento
                 incorrecto
        """
        # direcciones en las cuales puede voltear piezas
        direcciones = []

        # primero se revisa si ya hay una pieza en la posición o si está fuera del tablero
        if self.x[reng][col] != 0 or self.esta_fuera_tablero(reng, col):
            return direcciones

        # se revisan las ocho direcciones en las cuales se pueden voltear piezas
        for rStep, cStep in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]:

            # se revisa si la primera pieza en la dirección está en el tablero o si es diferente del otro jugador
            if self.esta_fuera_tablero(reng + rStep, col + cStep) or self.x[reng + rStep][col + cStep] != -self.jugador:
                continue

            # variables para moverte en la dirección
            rengTemp = reng + 2 * rStep
            colTemp = col + 2 * cStep

            # Ciclo para ver si se van a voltear piezas en la dirección
            while not self.esta_fuera_tablero(rengTemp, colTemp):
                if self.x[rengTemp][colTemp] == 0:
                    break
                if self.x[rengTemp][colTemp] == self.jugador:
                    direcciones.append((rStep, cStep))  # se agrega la dirección
                    break

                rengTemp += rStep
                colTemp += cStep

        return direcciones  # se regresan las direcciones para el momento de hacer la jugada

def utilidad(x):
    sum_jugador1 = 0
    sum_jugador2 = 0

    for i in range(8):
        for j in range(8):
            if x[i][j] == 1:
                sum_jugador1 += 1
            elif x[i][j] == -1:
                sum_jugador2 += 1
    return sum_jugador1 / (sum_jugador2 + sum_jugador1)


def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    aux_sort = []
    for play in jugadas:
        juego.hacer_jugada(play)
        aux_sort.append((utilidad(juego.x), play))
        juego.deshacer_jugada()
    aux_sort.sort(reverse=True)
    return [jugadas_chilas for i, jugadas_chilas in aux_sort]


def jugar():
    juego = Donathello()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Juego de othello contra una máquina con el algoritmo minimax.\n")
    print("En este juego siempre empiezan las negras: ")
    print("☻: Piezas negras.")
    print("☺: Piezas blancas.\n")
    res = ""

    while res != "s" and res != "n":
        res = input("¿Quieres ser primeras(s/n)?")

    if res == "n":
        os.system('cls' if os.name == 'nt' else 'clear')
        juego.dibuja_tablero()
        print("Esperando el movimiento de la máquina...")
        jugada = minimax(juego, dmax=4, utilidad=utilidad,
                         ordena_jugadas=ordena_jugadas,
                         transp=None)

        juego.hacer_jugada(jugada)

    while (juego.terminal() == None):
        os.system('cls' if os.name == 'nt' else 'clear')
        juego.dibuja_tablero()

        jugadas = juego.jugadas_legales()
        if len(jugadas) > 0:
            print("Jugadas: ")
            for i in range(len(jugadas)):
                print(i, ":", jugadas[i][0], "  ", sep='', end='')

            opc = input("\nOpción: ")

            while int(opc) >= len(jugadas) or int(opc) < 0:
                print("Opción incorrecta...")
                opc = input("Opción: ")

            juego.hacer_jugada(jugadas[int(opc)])
            os.system('cls' if os.name == 'nt' else 'clear')
            juego.dibuja_tablero()
        else:
            juego.jugador = -juego.jugador

        print("Esperando el movimiento de la máquina...")

        jugadas = juego.jugadas_legales()

        if len(jugadas) > 0:
            jugada = minimax(juego, dmax=4, utilidad=utilidad,
                             ordena_jugadas=ordena_jugadas,
                             transp=None)

            juego.hacer_jugada(jugada)
        else:
            juego.jugador = -juego.jugador

    os.system('cls' if os.name == 'nt' else 'clear')
    juego.dibuja_tablero()

    mensaje = "Ganaron las blancas" if juego.terminal() == 1 else "Ganaron las negras" if juego.terminal() == -1 else "Empate D:"

    print(mensaje)


if __name__ == '__main__':
    jugar()
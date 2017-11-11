#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
from games import Position, Negamax
from itertools import product
import os

__author__ = 'Rafael Castillo'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class ReversiPosition(Position):
    directions = set(product(*((-1, 0, 1),) * 2)) - {(0, 0)}

    @property
    def legal_moves(self):
        return self.moves_for(self.player)

    def moves_for(self, player):
        return [i for (i, v) in enumerate(self.board)
                if self.is_legal(i, player)]

    def is_legal(self, i, player):
        x, y = self.index_to_coord(i)
        if self.board[i]:
            return False
        for walk in (self.walk(d, i, player) for d in self.directions):
            for _ in walk:
                return True
        return False

    def make_move(self, move):
        if move == -1:
            return ReversiPosition(self.board, self.player, self.length + 1)

        new_board = list(self.board)

        x, y = self.index_to_coord(move)
        new_board[move] = self.player
        for walk in (self.walk(d, move, self.player) for d in self.directions):
            for i in walk:
                new_board[i] = self.player

        return ReversiPosition(tuple(new_board), -self.player, self.length + 1)

    def walk(self, direction, i, player):
        dx, dy = direction
        xi, yi = self.index_to_coord(i)
        xi, yi = xi + dx, yi + dy
        walk = []
        while self.valid_coord(xi, yi):
            i = self.coord_to_index(xi, yi)
            if not self.board[i]:
                break
            if self.board[i] == player:
                return walk
            walk.append(i)

            xi, yi = xi + dx, yi + dy

        return []

    @staticmethod
    def coord_to_index(x, y):
        return 8 * y + x

    @staticmethod
    def valid_coord(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    @staticmethod
    def index_to_coord(i):
        return i % 8, i // 8

    @property
    def terminal(self):
        if all(v != 0 for v in self.board) or not self.legal_moves:
            return max((-1, 1), key=self.board.count)
        return 0

    def empty_neighbors(self, i):
        x, y = self.index_to_coord(i)
        return (self.coord_to_index(x + dx, y + dy)
                for (dx, dy) in self.directions
                if self.valid_coord(x + dx, y + dy))

    """
    Me robé la interfaz del dui, nomas dejo esta nota si olvido reemplazarla
    por una propia y borrar esto
    """
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
                tablero += " O " if self.board[8*reng + col] == 1 else " X " \
                           if self.board[8*reng + col] == -1 else "   "
            tablero += "│\n"
            tablero += " ├───┼───┼───┼───┼───┼───┼───┼───┤\n" if reng < 7 \
                       else " └───┴───┴───┴───┴───┴───┴───┴───┘\n"

        blancas, negras = self.board.count(1), self.board.count(-1)

        tablero += "O: " + str(blancas) + "\n"
        tablero += "X: " + str(negras) + "\n"

        print(tablero)


SQUARE_SCORE = [9, 3, 3, 3, 3, 3, 3, 9,
                3, 1, 1, 1, 1, 1, 1, 3,
                3, 1, 1, 1, 1, 1, 1, 3,
                3, 1, 1, 1, 1, 1, 1, 3,
                3, 1, 1, 1, 1, 1, 1, 3,
                3, 1, 1, 1, 1, 1, 1, 3,
                3, 1, 1, 1, 1, 1, 1, 3,
                9, 3, 3, 3, 3, 3, 3, 9]


def reversi_utility(position):
    max_pot_mob = sum(len(position.empty_neighbors())
                      for i in range(64) if position.board[i] == -1)
    min_pot_mob = sum(len(position.empty_neighbors())
                      for i in range(64) if position.board[i] == 1)

    if max_pot_moby + min_pot_mob:
        potential_mobility = ((max_pot_mob - min_pot_mob)
                              / max_pot_mob + min_pot_mob)
    else:
        potential_mobility = 0

    if position.length < 32:
        partial = sum(SQUARE_SCORE[i] * position.board[i] for i in range(64))
    else:
        my_pieces = sum(1 for i in position.board if i == 1)
        his_pieces = sum(1 for i in position.board if i == -1)
        partial = (my_pieces - his_pieces / 64)

    mobility = position.player * (len(position.moves_for(position.player))
                                  - len(position.moves_for(-position.player)))

    return mobility + partial


def jugar():
    juego = make_reversi()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Juego de othello contra una máquina con el algoritmo minimax.\n")
    print("En este juego siempre empiezan las negras: ")
    print("X: Piezas negras.")
    print("O: Piezas blancas.\n")
    res = ""

    while res != "s" and res != "n":
        res = input("¿Quieres ser primeras(s/n)?")

    minimax = Negamax(reversi_utility)

    if res == "n":
        juego.dibuja_tablero()
        print("Esperando el movimiento de la máquina...")
        jugada = minimax(juego, 4)

        juego = juego.make_move(jugada)

    while not juego.terminal:
        juego.dibuja_tablero()

        jugadas = list(juego.legal_moves)
        print("Jugadas: ")
        for i in range(len(jugadas)):
            print(i, ":", juego.index_to_coord(jugadas[i]),
                  "  ", sep='', end='')

        opc = input("\nOpción: ")

        while int(opc) >= len(jugadas) or int(opc) < 0:
            print("Opción incorrecta...")
            opc = input("Opción: ")

        juego = juego.make_move(jugadas[int(opc)])
        juego.dibuja_tablero()

        print("Esperando el movimiento de la máquina...")

        jugada = minimax(juego, 4)

        juego = juego.make_move(jugada)

    juego.dibuja_tablero()

    mensaje = ("Ganaron las blancas" if juego.terminal() == 1
               else "Ganaron las negras" if juego.terminal() == -1
               else "Empate D:")

    print(mensaje)


def make_reversi():
    return ReversiPosition((0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 1, -1, 0, 0, 0,
                            0, 0, 0, -1, 1, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0), 1, 0)


if __name__ == '__main__':
    jugar()

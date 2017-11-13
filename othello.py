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
import numpy as np

__author__ = 'Rafael Castillo'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class ReversiPosition(Position):
    directions = set(product(*((-1, 0, 1),) * 2)) - {(0, 0)}

    @property
    def legal_moves(self):
        moves = list(self.moves_for(self.player))
        return moves if moves else ['pass']

    def moves_for(self, player):
        return (coord for (coord, _) in np.ndenumerate(self.board)
                if self.is_legal(coord, player))

    def is_legal(self, coord, player):
        if self.board[coord]:
            return False
        for walk in (self.walk(d, coord, player) for d in self.directions):
            for _ in walk:
                return True
        return False

    def make_move(self, move):
        if move == 'pass':
            return ReversiPosition(self.board, self.player)

        new_board = np.copy(self.board)

        new_board[move] = self.player
        for walk in (self.walk(d, move, self.player) for d in self.directions):
            for coord in walk:
                new_board[coord] = self.player

        return ReversiPosition(new_board, -self.player)

    def walk(self, direction, coord, player):
        dx, dy = direction
        xi, yi = coord
        xi, yi = xi + dx, yi + dy
        walk = []
        while self.valid_coord(xi, yi):
            if not self.board[xi, yi]:
                break
            if self.board[xi, yi] == player:
                return walk
            walk.append((xi, yi))

            xi, yi = xi + dx, yi + dy

        return []

    @staticmethod
    def valid_coord(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    @property
    def terminal(self):
        if (not np.sum(self.board == 0) or
                self.moves_for(1) == self.moves_for(-1) == ['pass']):
            return max((-1, 1), key=lambda p: np.sum(self.board == p))
        return 0

    def hashable_pos(self):
        return self.board.tostring(), self.player

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
                tablero += " ● " if self.board[reng, col] == 1 else " ○ " \
                           if self.board[reng, col] == -1 else "   "
            tablero += "│\n"
            tablero += " ├───┼───┼───┼───┼───┼───┼───┼───┤\n" if reng < 7 \
                       else " └───┴───┴───┴───┴───┴───┴───┴───┘\n"

        blancas, negras = np.sum(self.board == 1), np.sum(self.board == -1)

        tablero += "●: " + str(blancas) + "\n"
        tablero += "○: " + str(negras) + "\n"

        print(tablero)


SQUARE_SCORE = np.array([[9, 1, 3, 3, 3, 3, 1, 9],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [9, 1, 3, 3, 3, 3, 1, 9]])


def corner_utility(position):
    corners = position.board[[0, 0, -1, -1], [0, -1, 0, -1]]
    max_corners = len(corners == 1)
    min_corners = len(corners == -1)

    return ((max_corners - min_corners) / (max_corners + min_corners)
            if (max_corners + min_corners) else 0)


def bad_utility(position):
    return np.sum(position.board)


def static_utility(position):
    return np.sum(np.multiply(SQUARE_SCORE, position.board))


def hybrid_utility(position):
    max_chips = np.sum(position.board == 1)
    min_chips = -np.sum(position.board == -1)
    total_chips = max_chips + min_chips

    if total_chips < 48:
        return static_utility(position)
    else:
        return (max_chips - min_chips) / total_chips


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

    minimax = Negamax(hybrid_utility)

    if res == "n":
        juego.dibuja_tablero()
        print("Esperando el movimiento de la máquina...")
        jugada = minimax(juego, 4)

        juego = juego.make_move(jugada)

    while not juego.terminal:
        print(np.multiply(SQUARE_SCORE, juego.board))
        juego.dibuja_tablero()

        jugadas = list(juego.legal_moves)
        print("Jugadas: ")
        for i in range(len(jugadas)):
            print(i, ":", jugadas[i],
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
    board = np.zeros((8, 8), dtype=np.int8)
    board[3, [3, 4]] = [1, -1]
    board[4, [3, 4]] = [-1, 1]
    return ReversiPosition(board, 1)


if __name__ == '__main__':
    reversi = make_reversi()

    bad_player = Negamax(hybrid_utility)
    good_player = Negamax(hybrid_utility)

    next = bad_player

    while not reversi.terminal:
        print('juega', reversi.player)
        reversi.dibuja_tablero()
        move = next(reversi)
        reversi = reversi.make_move(move)
        next = bad_player if next == good_player else good_player
    reversi.dibuja_tablero()

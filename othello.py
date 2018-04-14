#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
othello.py
------------

El juego de Otello implementado por ustedess mismos, con jugador inteligente

"""

__author__ = 'Jordan Urias'

class othello():
    def __init__(self, _n=8):
        self.n = _n
        self.board = [['0' for x in range(self.n)] for y in range(self.n)]
        # 8 directions
        self.dirx = [-1,  0,  1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1,  0, 0,  1, 1, 1]
        
        if self.n % 2 == 0: # if board size is even
            z = int((self.n - 2) / 2)
            self.board[z][z] = '2'
            self.board[self.n - 1 - z][z] = '1'        
            self.board[z][self.n - 1 - z] = '1'
            self.board[self.n - 1 - z][self.n - 1 - z] = '2'
    
    
    def PrintBoard(self):
        m = len(str(self.n - 1))
        for y in range(self.n):
            row = ''
            for x in range(self.n):
                row += self.board[y][x]
                row += ' ' * m
            print (row + ' ' + str(y))
        row = ''
        for x in range(self.n):
            row += str(x).zfill(m) + ' '
        print (row + '\n')        

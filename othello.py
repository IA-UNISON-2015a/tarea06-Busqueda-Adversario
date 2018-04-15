#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
from busquedas_adversarios import JuegoSumaCeros2T
from collections import deque

__author__ = 'Raul Perez'

# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):
    """
    Clase para el juego de Othello donde la representacion
    del estado es el siguiente:

        0   1   2   3   4   5   6   7
        8   9   10  11  12  13  14  15
        16  17  18  19  20  21  22  23
        24  25  26  27  28  29  30  31
        32  33  34  35  36  37  38  39
        40  41  42  43  44  45  46  47
        48  49  50  51  52  53  54  55
        56  57  58  59  60  61  62  63

    """

    def __init__(self):
        """
        Inicializa el Othello con el siguiente estado

            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0  -1   1   0   0   0
            0   0   0   1  -1   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0

            arriba a la izquierda
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0 
            0   0   2   2   2   2   2   2  
            0   0   2   3   3   3   3   3  
            0   0   2   3   4   4   4   4    
            0   0   2   3   4   5   5   5      
            0   0   2   3   4   5   6   6   
            0   0   2   3   4   5   6   7

            arriba a la derecha
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0 
            2   2   2   2   2   2   0   0  
            3   3   3   3   3   2   0   0  
            4   4   4   4   3   2   0   0    
            5   5   5   4   3   2   0   0      
            6   6   5   4   3   2   0   0   
            7   6   5   4   3   2   0   0   

            abajo a la izquierda
            0   0   2   3   4   5   6   7
            0   0   2   3   4   5   6   6  
            0   0   2   3   4   5   5   5   
            0   0   2   3   4   4   4   4  
            0   0   2   3   3   3   3   3    
            0   0   2   2   2   2   2   2      
            0   0   0   0   0   0   0   0   
            0   0   0   0   0   0   0   0

            abajo a la derecha
            7   6   5   4   3   2   0   0
            6   6   5   4   3   2   0   0  
            5   5   5   4   3   2   0   0   
            4   4   4   4   3   2   0   0  
            3   3   3   3   3   2   0   0    
            2   2   2   2   2   2   0   0      
            0   0   0   0   0   0   0   0   
            0   0   0   0   0   0   0   0
        """
        # estado inicial
        x = [0 for _ in range(64)]
        x[27] = x[36] = -1
        x[28] = x[35] = 1
        super().__init__(tuple(x)
        self.area_de_jugadas = [18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45] # inicial
        self.historial = deque()
        self.estados_anteriores = deque()

    def jugada_legal(self, posicion):
        """
        Compueba si la jugada es legal, verifica si alguna
        de los 8 formas de voltear fichas se puede.

        * Horizontales: izquiera, derecha
        * Veticales:    arriba, abajo
        * Diagonales:   arriba a la izquierda, arriba a la derecha,
                        abajo a la izquierda, abajo a la derecha

        """
        def checa_ficha(posicion, iteracion, oponente):
            """
            Checa que esta en la posicion dada.
            Regresa: 0 si es cero o no hubo nada,
                     1 si es del oponente,
                     2 si es jugada legal
            """
            # si la ficha es del oponente, esta bien
            return (1 if estado[posicion] == oponente else
                    0 if estado[posicion] == 0 else
                    2 if iteracion>1 else
                    0)

        fila = posicion/8
        columna = posicion%8
        estado = self.x[:]
        jugador = self.jugador
        oponente = -1 * jugador
        # si donde se quiere poner una ficha hay algo
        # entonces la jugada no es legal
        if estado[posicion] != 0:
            return False
        # Horizontal izquierda
        if columna > 1:
            for i in range(1, columna+1):
                resultado = checa_ficha(posicion-i, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # Horizontal derecha
        if columna < 6:
            for i in range(1, 8-columna):
                resultado = checa_ficha(posicion+i, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # vertical arriba
        if fila > 1:
            for i in range(1, fila+1):
                resultado = checa_ficha(posicion-i*8, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # vertical abajo
        if fila < 6:
            for i in range(1, 8-fila):
                resultado = checa_ficha(posicion+i*8, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # diagonal arriba a la izquierda
        if columna > 1 and fila > 1:
            for i in range(1, min((columna, fila))+1):
                resultado = checa_ficha(posicion-i*9, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # diagonal arriba a la derecha
        if columna < 6 and fila > 1:
            for i in range(1, min(abs(columna-7), fila)+1):
                resultado = checa_ficha(posicion-i*7, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # diagonal abajo a la izquierda
        if columna > 1 and fila < 6:
            for i in range(1, min(columna, abs(fila-7))+1):
                resultado = checa_ficha(posicion+i*7, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break
        # diagonal abajo a la derecha
        if columna < 6 and fila < 6:
            for i in range(1, min(abs(columna-7), abs(fila-7))+1):
                resultado = checa_ficha(posicion+i*9, i, oponente)) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    return True
                else:
                    break

        return False

    def jugadas_legales(self):
        """
        Las jugadas legales son las posiciones donde se puede
        colocar una ficha y se volteen las fichas del oponente.
        """
        jugadas_permitidas = []

        for posicion in self.area_de_jugadas:
            # si es jugada legal se agrega a la lista
            if jugada_legal(posicion):
                jugadas_permitidas.append(posicion)
        
        return tuple(jugadas_permitidas)

    def terminal(self):
        """
        Revisa si hay jugadas legales para ambos jugadores
        """
        # si no hay jugadas legales para el jugador 1
        if len(self.jugadas_legales()) == 0:
            self.jugador *= -1
            # si no hay jugadas legales para el jugador -1    
            if len(self.jugadas_legales()) == 0:
                self.jugador *= -1
                negras, blancas = self.x.count(1), self.x.count(-1) 
                return ( 1 if negras > blancas else
                        -1 if blancas > negras else
                         0)
            self.jugador *= -1
            
        return None

    def hacer_jugada(self, jugada):
        pass

    def deshacer_jugada(self, ultima_jugada):
        pass
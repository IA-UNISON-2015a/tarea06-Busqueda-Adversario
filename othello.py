#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de othello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'José Roberto Salazar Espinoza'

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from random import shuffle
import os

class Othello(JuegoSumaCeros2T):
    def __init__(self):
        """
        Se inicializa el tablero como una matriz de 8x8
        donde llena de 0,1 y -1, donde 0 es un lugar vacío,
        1 es una pieza blanca y -1 es una pieza negra.
        """
        super().__init__((
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 1,-1, 0, 0, 0,
             0, 0, 0,-1, 1, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0
        ),-1)

    def terminal(self):
        negras = self.x.count(-1)
        blancas = self.x.count(1)

        if negras == 0 or blancas == 0:
            return 1 if blancas > negras else -1

        #se revisa si hay casillas vacias.
        if 0 in self.x:
            return None

        #1 si ganan las blancas -1 si ganan las negras 0 en empate.
        return 1 if blancas > negras else -1 if negras > blancas else 0

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
                tablero += " O " if self.x[ 8*reng + col ] == 1 else " X " if self.x[8*reng + col] == -1 else "   "
            tablero += "│\n"
            tablero += " ├───┼───┼───┼───┼───┼───┼───┼───┤\n" if reng < 7 else " └───┴───┴───┴───┴───┴───┴───┴───┘"
        
        print(tablero)

    def esta_fuera_tablero(self,reng,col):
        """
        Este método revisa si dados un renglón y un columna son coordenadas válidas para el tablero.

        @return: un booleano.
        """
        return (reng < 0 or reng >7 or col < 0 or col > 7) 

    def es_valido(self,reng,col):
        """
        este método dice si una casilla es válida para poner una pieza en ella.

        @param reng: renglon de la casilla
        @param col: columna de la casilla 
        @return: una lista con las direcciones en las cuales 
                 puede voltear piezas, vacía si es un movimiento 
                 incorrecto
        """
        #direcciones en las cuales puede voltear piezas
        direcciones = []

        #primero se revisa si ya hay una pieza en la posición o si está fuera del tablero
        if self.x[8*reng + col] != 0 or self.esta_fuera_tablero(reng,col):
            return direcciones
        
        #se revisan las ocho direcciones en las cuales se pueden voltear piezas
        for rStep,cStep in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]:

            #se revisa si la primera pieza en la dirección está en el tablero o si es diferente del otro jugador
            if self.esta_fuera_tablero(reng + rStep, col + cStep) or self.x[8*(reng + rStep) + (col + cStep)] != -self.jugador:
                continue
            
            #variables para moverte en la dirección
            rengTemp = reng + 2*rStep
            colTemp = col + 2*cStep

            #Ciclo para ver si se van a voltear piezas en la dirección
            while not self.esta_fuera_tablero(rengTemp, colTemp):
                if self.x[8*rengTemp + colTemp] == 0:
                    break
                if self.x[8*rengTemp + colTemp] == self.jugador:
                    direcciones.append((rStep,cStep)) #se agrega la dirección
                    break

                rengTemp += rStep
                colTemp += cStep

        return direcciones #se regresan las direcciones para el momento de hacer la jugada

    def jugadas_legales(self):
        """
        Método que calcula las jugadas legales de el estado actual del tablero.

        @return: una lista de jugadas que se pueden realizar.
        """
        legales = []
        for reng in range(8):
            for col in range(8):
                direcciones = self.es_valido(reng,col)
                #se agrega a las jugadas si tiene alguna dirección en la cual modificar
                if len(direcciones) > 0:
                    #se agregan las direcciones a la acción
                    legales.append( ((reng,col), direcciones) ) 

        return legales

    def hacer_jugada(self,jugada):
        """
        Método para hacer una jugada, recibe una jugada previamente validada por el método jugadas_legales.

        @param jugada: jugada a realizar.
        """
        #aquí se utilizan las direcciones que se sacan en el método es_valido.
        reng,col = jugada[0]
        direcciones = jugada[1]

        #es una lista con las casillas que se modifican para poder deshacer la jugada.
        casillas = [(reng,col)]
        
        #se pone la pieza en la posición
        self.x[8*reng + col] = self.jugador


        for rStep,cStep in direcciones:
            rengTemp = reng + rStep
            colTemp = col + cStep

            while self.x[8*rengTemp + colTemp] != self.jugador:
                #aquí se guardan las casillas al momento de modificarse.
                casillas.append( (rengTemp,colTemp) )
                self.x[8*rengTemp + colTemp] = self.jugador
                rengTemp += rStep
                colTemp += cStep
        
        #se agregan las casillas en el historial y se cambia de jugador.
        self.historial.append(casillas)
        self.jugador *= -1

    def deshacer_jugada(self):
        """
        Método para des hacer la última jugada que se realizó.
        """
        #se obtienen las casillas que se modificaron.
        casillas = self.historial.pop()
        reng,col = casillas[0]

        #se quita la pieza.
        self.x[8*reng + col] = 0

        #se regresan todas las demas casillas a su estado original.
        for i,j in casillas[1:]:
            self.x[8*i + j] = -self.x[8*i + j]

        self.jugador *= -1

def numero_piezas(x):
    """
    En este método solamente se cuentan cuantas negras y cuantas blancas hay
    se restan y luego se dividen entre la suma, una forma medio macana pero
    es el primer intento.
    """

    blancas,negras = x.count(1),x.count(-1)

    return (blancas - negras)/(blancas + negras)

def movilidad(x):
    juego = Othello()
    juego.x = x
    movilidad_negras = len(juego.jugadas_legales())
    juego.jugador = 1
    movilidad_blancas = len(juego.jugadas_legales())

    return (movilidad_blancas - movilidad_negras)/(movilidad_blancas + movilidad_negras)

def esquinas(X):
    esquinas_blancas,esquinas_negras = 0
    for i in (0,7,56,63):
        if x[i] == 1:
            esquinas_blancas += 1
        elif x[i] == -1:
            esquinas_negras += -1
    
    esquinas = 0 if esquinas_blancas + esquinas_negras == 0 else (esquinas_blancas - esquinas_negras)/(esquinas_blancas + esquinas_negras)
    
    return esquinas

def utilidad(x):
    return 0.4*esquinas(x) + 0.4*movilidad(x) + 0.2*numero_piezas(x)

def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    shuffle(jugadas)
    return jugadas

class JuegoOthello:
    def __init__(self):
        pass
    
    def jugar(self):
        juego = Othello()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Juego de othello contra una máquina con el algoritmo minimax.\n")
        print("En este juego siempre empiezan las negras: ")
        print("X: Piezas negras.")
        print("O: Piezas blancas.\n")
        res = ""

        while res != "s" and res != "n":
            res = input("¿Quieres ser primeras(s/n)?")

        if res == "n":
            os.system('cls' if os.name == 'nt' else 'clear')
            juego.dibuja_tablero()
            print("Esperando el movimiento de la máquina...")
            jugada = minimax(juego, dmax=6, utilidad=utilidad_2,
                                ordena_jugadas=ordena_jugadas,
                                transp={})

            juego.hacer_jugada(jugada)

        while(juego.terminal() == None):
            os.system('cls' if os.name == 'nt' else 'clear')
            juego.dibuja_tablero()

            jugadas = juego.jugadas_legales()
            if len(jugadas) > 0:
                print("Jugadas: ")
                for i in range(len(jugadas)):
                    print(i,":",jugadas[i][0],"  ",sep = '',end='')

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
                jugada = minimax(juego, dmax=5, utilidad=utilidad,
                                ordena_jugadas=ordena_jugadas,
                                transp={})

                juego.hacer_jugada(jugada)
            else:
                juego.jugador = -juego.jugador

        os.system('cls' if os.name == 'nt' else 'clear')
        juego.dibuja_tablero()

        mensaje = "Ganaron las blancas" if juego.terminal() == 1 else "Ganaron las negras" if juego.terminal() == -1 else "Empate D:"

        print(mensaje)

if __name__ == '__main__':
    juego = JuegoOthello()
    juego.jugar()
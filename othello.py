#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
import numpy as np
import copy

__author__ = 'Ricardo Holguin Esquer'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):

    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:
                                                         y
                        56  57  58  59  60  61  62  63  |0
                        48  49  50  51  52  53  54  55  |1
                        40  41  42  43  44  45  46  47  |2
                        32  33  34  35  36  37  38  39  |3
                        24  25  26  27  28  29  30  31  |4
                        16  17  18  19  20  21  22  23  |5
                         8   9  10  11  12  13  14  15  |6
                         0   1   2   3   4   5   6   7  |7
                        ________________________________
                      x  0   1   2   3   4   5   6   7

        Y las posiciones iniciales son en 35, 36, 27, 28
        """
        super().__init__(tuple([0 for _ in range(8*8)]), jugador=-1)
        # Yo manejare todo como una matriz pero acordamos todos usar un solo
        # vector de 8*8 que representa una matriz como el estado
        self.tablero = np.array([0 for i in range(8) for j in range(8)])
        self.tablero = np.reshape(self.tablero, (-1, 8))

        # 8 direcciones posibles
        self.dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1, 0, 0, 1, 1, 1]

        # Iniciar tablero
        # 1 = blancas, -1 = negras
        z = int((8-2)/2)
        self.tablero[z][z] = 1
        self.tablero[z+1][z+1] = 1
        self.tablero[z][z+1] = -1
        self.tablero[z+1][z] = -1

        xAux = []
        for i in self.tablero:
            xAux.extend(i)
        self.x = xAux

        # Pila para almacenar los tableros completos de cada jugada
        # porque no se me ocurrio una manera hackerosa para regresar
        # un estado atras cuando se deshace una jugada
        self.historialTablero = []

        # Tabla de transposición
        self.tablaTrans = {}

    def contarBlancas(self):
        val = 0
        for y in range(8):
            for x in range(8):
                if self.tablero[y][x] == 1:
                    val += 1
        return val

    def contarNegras(self):
        val = 0
        for y in range(8):
            for x in range(8):
                if self.tablero[y][x] == -1:
                    val += 1
        return val

    def imprimirTablero(self):
        """
        función para imprimir el tablero en consola de una manera "bonita"
        """
        n = 8
        m = len(str(n - 1))
        for y in range(n):
            renglon = ''
            for x in range(n):
                if len(str(self.tablero[y][x])) == 2:
                    renglon = renglon[:-1]
                    renglon += str(self.tablero[y][x])
                    renglon += '  ' * m
                else:
                    renglon += str(self.tablero[y][x])
                    renglon += '  ' * m
            print(renglon + '| ' + str(y))
        for y in range(len(renglon)):
            print("_", end='')
        renglon = ''
        print()
        for x in range(n):
            renglon += str(x).zfill(m) + '  '
        print(renglon + '\n')
        print("Blancas = " + str(self.contarBlancas()))
        print("Negras = " + str(self.contarNegras()))

    def hacer_jugada(self, jugada):
        """
        Esta funcion asume que la jugada es valida
        """
        # Se guarda el estado actual del juego antes de mover piezas
        self.historialTablero.append(copy.deepcopy(self.tablero))
        #piezasTomadas = 0
        x, y = jugada
        self.tablero[y][x] = self.jugador
        for d in range(8): # 8 direcciones
            ctr = 0
            for i in range(8): #El tamaño del tablero
                # Calcula la coordenada de la direccion en la que esta buscando
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                # Si se sale del tablero entonces se sale del ciclo
                if dx < 0 or dx > 7 or dy < 0 or dy > 7:
                    ctr = 0
                    break
                elif self.tablero[dy][dx] == self.jugador:
                    break
                elif self.tablero[dy][dx] == 0:
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                self.tablero[dy][dx] = self.jugador

        # Se copia los datos de self.tablero a x (para fines de compatibilidad)
        # con los otros othellos
        for y in range(8):
            for x in range(8):
                self.x[y*8 + x] = self.tablero[y][x]

        # Se actualiza el estado x0
        self.x0 = tuple(self.x)
        self.historial.append(jugada)
        self.jugador *= -1
        return None

    #def deshacer_jugada2(self):
        x,y = self.historial.pop()
        self.tablero[y][x] = 0
        for d in range(8): # 8 direcciones
            ctr = 0
            for i in range(8): #El tamaño del tablero
                # Calcula la coordenada de la direccion en la que esta buscando
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                # Si se sale del tablero entonces se sale del ciclo
                if dx < 0 or dx > 7 or dy < 0 or dy > 7:
                    ctr = 0
                    break
                elif self.tablero[dy][dx] == self.jugador:
                    break
                elif self.tablero[dy][dx] == 0:
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                self.tablero[dy][dx] = self.jugador

        # Se copia los datos de self.tablero a x (para fines de compatibilidad)
        # con los otros othellos
        for y in range(8):
            for x in range(8):
                self.x[y*8 + x] = self.tablero[y][x]

        # Se actualiza el estado x0
        self.jugador *= -1
        self.x0 = tuple(self.x)
        return None

    def deshacer_jugada(self):
        if self.historialTablero:
            #_ = self.historialTablero.pop()
            # Se saca un estado del tablero de la pila
            self.tablero = self.historialTablero.pop()

            # Se copia el nuevo tablero a la lista que representa el tablero
            # (Para fines de compatibilidad con los juegos de los demas)
            for y in range(8):
                for x in range(8):
                    self.x[y*8 + x] = self.tablero[y][x]
            # Se actualiza la tupla
            self.x0 = tuple(self.x)
            # Se saca de la pila del historial el juego (Aunque no se necesite)
            i,j = self.historial.pop()
            self.jugador *= -1
        return None


    def verificar_jugada(self, tablero, x, y):
        """
        Es exactamente igual que hacer_jugada pero esta no altera
        el tablero del juego y solo se usa para verificar si una jugada
        es valida
        """

        piezasTomadas = 0
        tablero[y][x] = self.jugador
        for d in range(8): # 8 direcciones
            ctr = 0
            for i in range(8): #El tamaño del tablero
                # Calcula la coordenada de la direccion en la que esta buscando
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                # Si se sale del tablero entonces se sale del ciclo
                if dx < 0 or dx > 7 or dy < 0 or dy > 7:
                    ctr = 0
                    break
                elif tablero[dy][dx] == self.jugador:
                    break
                elif tablero[dy][dx] == 0:
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + self.dirx[d]*(i+1)
                dy = y + self.diry[d]*(i+1)
                tablero[dy][dx] = self.jugador
            piezasTomadas += ctr

        return (tablero, piezasTomadas)

    def movimientoValido(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        if self.tablero[y][x] != 0:
            return False
        (_,piezasTomadas) = self.verificar_jugada(copy.deepcopy(self.tablero),
                                            x, y)
        if piezasTomadas == 0:
            return False
        return True

    def jugadas_legales(self):
        jugadasLegales=[]
        for y in range(8):
            for x in range(8):
                if self.movimientoValido(x,y):
                    jugadasLegales.append((x,y))
        return tuple(jugadasLegales)

    def terminal(self):
        for y in range(8):
            for x in range(8):
                if self.movimientoValido(x, y):
                    return None
        return self.contarQuienGano()

    def contarQuienGano(self):
        negro = blanco = 0
        for y in range(8):
            for x in range(8):
                if self.tablero[y][x] == 1:
                    blanco += 1
                elif self.tablero[y][x] == -1:
                    negro += 1
        if negro > blanco:
            return -1
        elif negro < blanco:
            return 1
        else:
            return 0

def utilidad1(tablero):
    """
    Calcula la utilidad de una posición del juego othello para el jugador
    blanco

    @param x: un arreglo de numpy en forma de matriz
    """
    jugador = 1
    total = 0
    for y in range(8):
        for x in range(8):
            if tablero[y*8 + x] == 1:
                if (x == 0 or x == 7) and (y == 0 or y == 7):
                    # Esquina. Que se tenga una posicion de esquina hace imposible
                    # que te quiten ese lugar, por lo que es mejor tener ese lugar
                    total += 4
                elif (x == 0 or x == 7) or (y == 0 or y == 7):
                    # Orilla. Que se tenga una posicion de esquina hace dificil
                    # que te quiten ese lugar, por lo que es mejor tener ese lugar
                    total += 2
                else:
                    # Cuando se tiene una ficha en cualquier otro lado
                    total += 1
    return total

def ordena_jugadas(juego):
    jugadasOrdenadas = []
    for i in juego.jugadas_legales():
        #verificar_jugada regresa una matriz y puntos
        (tableroTemp, puntos) = juego.verificar_jugada(copy.deepcopy(juego.tablero),
                                                        i[0], i[1])

        # pasar de matriz a vector
        aux = juego.x
        for y in range(8):
            for x in range(8):
                aux[y*8 + x] = tableroTemp[y][x]
        # utilidad1 recibe una lista
        jugadasOrdenadas.append((i, utilidad1(aux)))
    jugadasOrdenadas = sorted(jugadasOrdenadas, key=lambda nodo: nodo[1], reverse = True)
    jugadasOrdenadas = [nodo[0] for nodo in jugadasOrdenadas]
    return jugadasOrdenadas


def jugar():
    juego = Othello()
    print("El jugador son las bolas negras y el bot las blancas")

    while juego.terminal() is None:
        entradaCorrecta = False
        juego.imprimirTablero()

        # Mientras las entradas de x y y no sean correctas respecto al juego
        # se pediran otra vez las coordenadas
        while not entradaCorrecta:
            jugadasDisponibles = juego.jugadas_legales()
            print("Jugadas legales:")
            print(jugadasDisponibles, end="\n\n")
            x = int(input("Ingresa coordenada de x: "))
            y = int(input("Ingresa coordenada de y: "))

            if juego.movimientoValido(x,y):
                entradaCorrecta = True
            else:
                print("Ingresa una jugada valida\n")

        #El jugador hace su jugada
        juego.hacer_jugada((x,y))

        juego.imprimirTablero()

        if juego.terminal() != None:
            break

        jugada = minimax_t(juego, utilidad=utilidad1, ordena_jugadas=ordena_jugadas, transp=juego.tablaTrans)
        juego.hacer_jugada(jugada)

    if juego.contarNegras() > juego.contarBlancas():
        print("\nEl ganado es el jugador (negras)")
    elif juego.contarNegras() < juego.contarBlancas():
        print("\nEl ganado es el bot (blancas)")
    else:
        print("\nEs un empate lmao que maletas son los dos.")


if __name__ == '__main__':
    jugar()

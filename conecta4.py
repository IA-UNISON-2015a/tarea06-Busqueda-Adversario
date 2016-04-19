#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conecta4.py.py
------------

El juego de conecta 4

Este juego contiene una parte de la tarea 5, y otra parte
es la implementación desde 0 del juego de Otello.

"""
import juegos_cuadricula
import time
from random import shuffle

__author__ = 'juliowaissman'


class Conecta4(juegos_cuadricula.Juego2ZT):
    """
    Juego del conecta 4 utilizando la definición de juego utilizada
    en la clase juego_tablero.JuegoT2ZT. Todos los modulos se deben
    de reescribir en función del nuevo problema.

    """

    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego.

                         0   1   2   3   4   5   6
                         7   8   9  10  11  12  13
                        14  15  16  17  18  19  20
                        21  22  23  24  25  26  27
                        28  29  30  31  32  33  34
                        35  36  37  38  39  40  41
        """
        juegos_cuadricula.Juego2ZT.__init__(self,
                                            7, 6,
                                            tuple([0 for _ in range(42)]))

    def jugadas_legales(self, estado, jugador):
        """
        Encuentra todas las jugadaslegales, que son las
        posiciones arriba en cada columna

        @param estado: Una tupla con el estado del juego
        @param jugador: En este caso no importa ya que las jugadas son iguales

        @return: Una tupla de pares ordenados del tipo

                        ((None, a1), ..., (None, an))

                 donde ai es la posición donde se le puede agregar una ficha

        """
        def indice0(tupla):
            "Como index pero regresa None, si no hay lugares vacios"
            try:
                return tupla.index(0)
            except ValueError:
                return None

        def vacios(s):
            for base in range(35, 42):
                indice = indice0(estado[base::-7])
                yield None if indice is None else base - (7 * indice)

        return [(None, pos) for pos in vacios(estado) if pos is not None]

    def estado_terminal(self, estado):
        """
        Revisa si el estado es terminal, si no hay espacios para
        agregar una nueva ficha o si algun jugador completo 4 puntos

        """
        def p(renglon, columna):
            return 7 * renglon + columna

        def checa(s, p, inc):
            return abs(sum([s[p + i] for i in range(0, 4 * inc, inc)])) == 4

        def horiz(s, p):
            return checa(s, p, 1)

        def diag_izq(s, p):
            return checa(s, p, 8)

        def diag_der(s, p):
            return checa(s, p, 6)

        def vertical(s, p):
            return checa(s, p, 7)

        for r in range(6):
            for c in range(7):
                if ((c < 4 and horiz(estado, p(r, c))) or
                    (r < 3 and
                     ((vertical(estado, p(r, c))) or
                      (c < 4 and diag_izq(estado, p(r, c))) or
                      (c > 2 and diag_der(estado, p(r, c)))))):
                    return estado[p(r, c)]
        return None if 0 in estado else 0

    def hacer_jugada(self, estado, jugada, jugador):
        """
        Devuelve estado_nuevo que es el estado una vez que se
        realizó la juagada por el jugador.

        Hay que recordar que los juegos de tablero los estamos
        estandarizando para jugadas las cuales son (pini, pfinal)
        donde pini esla posicion inicial y pfinal es la posicion
        final de una ficha.

        Si el juego solamente implica poner fichas entonces pini
        no se toma en cuenta pero si tiene que ir para
        guardar homogeneidad entre los diferentes juegos y
        los diferentes métodos que desarrollaremos.

        """
        e = list(estado)
        e[jugada[1]] = jugador
        return tuple(e)


class JugadorConecta4(juegos_cuadricula.JugadorNegamax):
    """
    Un jugador Negamax ajustado a el juego conecta 4, solamente hay
    que modificar dos métodos (o uno solo si no
    estamos preocupados por el tiempo de búsqueda: ordena y utilidad.

    """
    def __init__(self, tiempo_espera=10):
        """
        Inicializa el jugador limitado en tiempo y no en profundidad
        """
        juegos_cuadricula.JugadorNegamax.__init__(self, d_max=1)
        self.tiempo = tiempo_espera
        self.maxima_d = 20

    def ordena(self, juego, estado, jugadas, jugador):
        """
        Ordena las jugadas en función de las más prometedoras a las menos
        prometedoras.

        Por default regresa las jugadas en el mismo orden que se generaron.

        """
        # ----------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        # ----------------------------------------------------------------------
        jugadas.sort(key=lambda j: self.threat(juego, juego.hacer_jugada(estado,j,jugador), jugador))
        return jugadas
        
        
        

    def utilidad(self, juego, estado):
        """
        El corazón del algoritmo, determina fuertemente
        la calidad de la búsqueda.

        Por default devuelve el valor de juego.estado_terminal(estado)

        """
        # ----------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        # ----------------------------------------------------------------------
        t = self.threat(juego, estado, self.jugador)
        return -1 if t >= 500 else 1 if t<=-500 else 0
        
    def threat(self, juego, estado, jugador):
        """
        Devuelve el nivel de amenaza que tiene un estado
        """
        t = [0,0,0,0,0,0,0,0,0] # [0,1,2,3,4,-4,-3,-2,-1]
        for r in range(5,-1,-1):
            for c in range(7):
                t[self.up(estado, r*7+c)] += 1 
                t[self.right(estado, r*7+c)] += 1 
                t[self.upright(estado, r*7+c)] += 1 
                t[self.upleft(estado, r*7+c)] += 1
        if t[-jugador*4] > 0:
            return 1000
        if t[jugador*4] > 0:
            return -1000
        if t[-jugador*3] > 0:
            return -500
        if t[jugador*3] > 0:
            return 500
        return sum([-jugador*t[i]*i for i in (-2,-1,1,2,3)])
    
    @staticmethod
    def up(estado, x):
        """
        Devuelve lo bueno que es la posicion x en el estado 'estado' en base
        a el numero de fichas (y de que jugador) que hay desde x hasta 3 
        fichas mas arriba. Devuelve 0 si no hay 3 filas mas arriba o si
        hay fichas mixtas en la trayectoria
        """
        if x/7 < 3:
            return 0 
        j = estado[x]
        total = j
        for i in range(1,4):
            u = estado[x-i*7]
            if j == 0 or u != -j:
                total += u
                j = u
            else:
                return 0
        return total
    
    @staticmethod
    def right(estado, x):
        """
        Devuelve lo bueno que es la posicion x en el estado 'estado' en base
        a el numero de fichas (y de que jugador) que hay desde x hasta 3 
        fichas mas a la derecha. Devuelve 0 si no hay 3 columnas mas a la 
        izquierda o si hay fichas mixtas en la trayectoria
        """
        if x%7 > 3:
            return 0
        j = estado[x]
        total = j
        for i in range(1,4):
            r = estado[x+i]
            if j == 0 or r != -j:
                total += r
                j = r
            else:
                return 0
        return total
        
    @staticmethod
    def upright(estado, x):
        """
        Devuelve lo bueno que es la posicion x en el estado 'estado' en base
        a el numero de fichas (y de que jugador) que hay desde x hasta 3 
        fichas mas en la diagonal superior derecha. Devuelve 0 si no hay 3 
        filas mas arriba o 3 columnas mas a la derecha; o si hay fichas 
        mixtas en la trayectoria
        """
        if x/7 < 3 or x%7 > 3:
            return 0
        j = estado[x]
        total = j
        for i in range(1,4):
            ur = estado[x-i*6]
            if j == 0 or ur != -j:
                total += ur
                j = ur
            else:
                return 0
        return total
        
    @staticmethod
    def upleft(estado, x):
        """
        Devuelve lo bueno que es la posicion x en el estado 'estado' en base
        a el numero de fichas (y de que jugador) que hay desde x hasta 3 
        fichas mas en la diagonal superior izquierda. Devuelve 0 si no hay 3 
        filas mas arriba o 3 columnas mas a la izquierda; o si hay fichas 
        mixtas en la trayectoria
        """
        if x/7 < 3 or x%7 < 3:
            return 0
        j = estado[x]
        total = j
        for i in range(1,4):
            ul = estado[x-i*8]
            if j == 0 or ul != -j:
                total += ul
                j = ul
            else:
                return 0
        return total
            
                    
            

    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        self.jugador = jugador
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego,
                                     estado,
                                     juego.jugadas_legales(estado, jugador),
                                     jugador),
                         key=lambda jugada: self.negamax(juego,
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
    juego = juegos_cuadricula.InterfaseTK(Conecta4(),
                                          juegos_cuadricula.JugadorHumano(),
                                          #JugadorConecta4(4),
                                          JugadorConecta4(4),
                                          1)
    juego.arranca()

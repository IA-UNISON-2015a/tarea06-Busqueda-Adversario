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
                    return estado[p(r, c)]*100
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

    def ordena(self, juego, estado, jugadas):
        """
        Ordena las jugadas en función de las más prometedoras a las menos
        prometedoras.

        Por default regresa las jugadas en el mismo orden que se generaron.

        """
        # ----------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        # ----------------------------------------------------------------------
        def en_medio(jugada):
            return abs(jugada[1]%7 -3)

        sorted(jugadas,key=en_medio)
        return jugadas

    def utilidad(self, juego, estado):

        def checa_columnas(estado,tipo):
            #tipo 0 = numero de fichas en el tope de las columnas pertenecientes al color
            #tipo 1 = 7 - numero de renglones ocupados
            utilidad = 7 if tipo == 1 else 0
            for i in range(7):
                for j in range(6):
                    if estado[7*j+i] != 0:
                        utilidad+= -1 if tipo == 1 else estado[7*j+i]
                        break
            return utilidad
        def en_medio(estado):
            return sum(estado[3+7*i] for i in xrange(6))


        """
        El corazón del algoritmo, determina fuertemente
        la calidad de la búsqueda.

        Por default devuelve el valor de juego.estado_terminal(estado)
        """
        
        # ----------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        # ----------------------------------------------------------------------
        val = juego.estado_terminal(estado)
        if val is None:
            a1 = 1.0
            a2 = 2.0
            a3 = 3.0
            return a1*checa_columnas(estado,0) + a2*checa_columnas(estado,1) + a3*en_medio(estado)
        return val

    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego,
                                     estado,
                                     juego.jugadas_legales(estado, jugador)),
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
    juego = juegos_cuadricula.InterfaseTK(Conecta4(),
                                          juegos_cuadricula.JugadorHumano(),
                                          JugadorConecta4(4),
                                          1)
    juego.arranca()

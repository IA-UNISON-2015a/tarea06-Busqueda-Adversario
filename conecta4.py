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
        # Bueno para empezar que significa una jugadora prometedora? cuando estuve jugando lo mejor que
        # podia tener es el siguiente caso supongamos que mis fichas se representan con X las del adversario
        # con Y y las casillas vacias como 0 una jugada prometedora para mi es 00XXX00 ya que el oponente 
        # al taparme una jugada queda la otra casilla vacia 0YXXXX0 y conecto cuatro. pero al atacar el 
        # problema la variable estado no solo me muestra las fichas que puse tambien me muestra las posibles
        # casillas en donde puedo poner y no diferen una de otra por lo que no se me ocurre como distinguirlas.
        # pero se me ocurrio hacer lo siguiente para empezar agregue un nuevo parametro a la funcion ordena el
        # cual es jugador despues hay una funcion que es hacer jugada lo que hice fue hacer un loop por cada jugada
        # y llamar a la funcion hacer_jugada mandando los parametros estado,jugada y jugador esto me da un nuevo estado
        # luego pense en evaluar ese estado como terminal muchas veces me arrojaba None pero otras veces me mandaba 1 o -1
        # lo que significa que es terminal pero esto no es cierto ya que evalua el estado e incluye las fichas puestas y 
        # las posibles casillas en donde puedo poner entonces se me ocurrio hacer una nueva funcion la cual se llama 
        # es_meta hace casi lo mismo que la funcion es_terminal pero en esta reviso el estado las lineas verticales,
        # horizontales y diagonales si encuentra cuatro casillas con el numero del jugador entonces es terminal como en 
        # la funcion ya programada pero ya sabemos que esto no es cierto, entonces puse un contador y cada vez que 
        # encuentra una solucion suma uno y al final regreso el nuevo estado con un numero el cual es el del contador 
        # entonces el estado que tenga el numero mas alto es el que tiene mas lugares posibles para poner una ficha 
        # y donde hay suficientes casillas posibles para dar con una solucion asi es como defino prometedor.

        jugadas_ordenadas = []

        for j in jugadas:

            jugada_temp = juego.hacer_jugada(estado, j, jugador)
            cont = self.es_meta(jugada_temp, jugador)

            if cont > 0:
                valor = tuple((cont, tuple(j)))
                jugadas_ordenadas.append(valor)
            else:
                valor = tuple((0, tuple(j)))
                jugadas_ordenadas.append(valor)

        jugadas_ordenadas.sort(key=lambda x: x[0], reverse=True)
        jugadas = [i[1] for i in jugadas_ordenadas]

        return jugadas

        """
        shuffle(jugadas)
        return jugadas

        """
    def utilidad(self, juego, estado, jugador):
        """
        El corazón del algoritmo, determina fuertemente
        la calidad de la búsqueda.

        Por default devuelve el valor de juego.estado_terminal(estado)

        """
        # ----------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        # ----------------------------------------------------------------------
        # En realidad es el corazon del algoritmo la verdad le di muchas vueltas a como
        # responder esto y todo lo que se me ocurria tenia que distinguir las fichas ya 
        # puestas pero al darme el estado las fichas ya puestas y las casillas donde puedo
        # poner opte por usar google .. encontre en un foro a un bato que tenia el mismo
        # problema aqui esta el link de el foro 
        # http://programmers.stackexchange.com/questions/263514/why-does-this-evaluation-function-work-in-a-connect-four-game-in-java
        # lo que proponen aqui es ver el tablero de la siguiente forma
        #
        # 3 4 5  7  5  4 3
        # 4 6 8  10 8  6 4
        # 5 8 11 13 11 8 5
        # 5 8 11 13 11 8 5
        # 4 6 8  10 8  6 4
        # 3 4 5  7  5  4 3
        # 
        # El primer numero el 3 representa el numero de posibles soluciones que lo contengan 
        # que seria la linea vertical, horizontal y una diagonal. el segundo numero que es el 4 que 
        # esta a la derecha del 3 que acabamos de mencionar, considera una linea vertical y una diagonal
        # entonces tenemos 2 las otras dos corresponden a la linea horizontal comenzando del 3 y a otra
        # horizontal comenzando de el mismo entonces hay 4 posibles soluciones que incluyen a esta casilla.
        # la misma idea se aplica a las demas casillas. 
        # La suma de todas las casillas con estos numeros da 276 y como el juego es uno a uno a cada jugador
        # le toca la mitad de la suma de las casillas que es 138 entonces la idea es ir revisando el tablero casilla 
        # por casilla si nos encontramos con una casilla con una de nuestras fichas o una posible a poner sumamos el valor
        # de la casilla a nuestra correspondiente suma que es 138 y si encontramos
        # una del adversario la restamos.
        # si el resultado de las sumas y restas presenta lo siguiente
        # total < 0 significa que nuestro oponente nos va ganando
        # total = 0 significa que esta parejo el juego equitativo
        # total > 0 significa que vamos ganando
        # 
        # De entrada me parecio una buena forma de evaluar la utilidad pero al momento de la practica es pesima
        # la maquina se apendeja mucho y es mejor la que usted propuso. Pero al final de cuentas es una forma de
        # obtener la utilidad ..

        def OI(columna, renglon):
            return columna + renglon * 7

        evaluacion_juego = [3, 4, 5, 7, 5, 4, 3,
                            4, 6, 8, 10, 8, 6, 4,
                            5, 8, 11, 13, 11, 8, 5,
                            5, 8, 11, 13, 11, 8, 5,
                            4, 6, 8, 10, 8, 6, 4,
                            3, 4, 5, 7, 5, 4, 3]

        utilidad = 138
        suma = 0

        for x in range(6):
            for y in range(7):
                temp = OI(y,x)
                if estado[temp] == jugador:
                    suma += evaluacion_juego[temp]
                if estado[temp] == -1 * jugador:
                    suma -= evaluacion_juego[temp]

        return utilidad + suma

        """
        val = juego.estado_terminal(estado)
        if val is None:
            return 0
        return val

        """

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

    def es_meta(self, estado, jugador):

        def OI(columna, renglon):
            return columna + renglon * 7

        cont = 0

        # horizontal
        for y in range(6):
            for x in range(7 - 3):
                if estado[OI(x, y)] == jugador and estado[OI(x + 1, y)] == jugador and estado[
                    OI(x + 2, y)] == jugador and estado[OI(x + 3, y)] == jugador:
                    cont += 1

        # vertical
        for x in range(7):
            for y in range(6 - 3):
                if estado[OI(x, y)] == jugador and estado[OI(x, y + 1)] == jugador and estado[
                    OI(x, y + 2)] == jugador and estado[OI(x, y + 3)] == jugador:
                    cont += 1

        # / diagonal
        for x in range(7 - 3):
            for y in range(3, 6):
                if estado[OI(x, y)] == jugador and estado[OI(x + 1, y - 1)] == jugador and estado[
                    OI(x + 2, y - 2)] == jugador and estado[OI(x + 3, y - 3)] == jugador:
                    cont += 1

        # \ diagonal
        for x in range(7 - 3):
            for y in range(6 - 3):
                if estado[OI(x, y)] == jugador and estado[OI(x + 1, y + 1)] == jugador and estado[
                    OI(x + 2, y + 2)] == jugador and estado[OI(x + 3, y + 3)] == jugador:
                    cont += 1

        return cont

if __name__ == '__main__':

    # Ejemplo donde empieza el jugador humano
    juego = juegos_cuadricula.InterfaseTK(Conecta4(),
                                          juegos_cuadricula.JugadorHumano(),
                                          JugadorConecta4(4),
                                          1)
    juego.arranca()
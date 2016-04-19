#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Jorge Carvajal'
import juegos_cuadricula
import time
import copy
from random import shuffle
# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class Othello(juegos_cuadricula.Juego2ZT):
    """
    Juego del conecta 4 utilizando la definición de juego utilizada
    en la clase juego_tablero.JuegoT2ZT. Todos los modulos se deben
    de reescribir en función del nuevo problema.

    """

    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego.

                         0   1   2   3   4   5   6  7
                         8   9   10  11  12  13  14 15 
                        14  15  16  17  18  19  20
                        21  22  23  24  25  26  27
                        28  29  30  31  32  33  34
                        35  36  37  38  39  40  41
        """
        a = [0 for _ in range(64)]
        a[27],a[28],a[35],a[36] = 1,-1,-1,1
        juegos_cuadricula.Juego2ZT.__init__(self,
                                            8, 8,
                                            tuple(a))

    def jugadas_legales(self, estado, jugador):
        def checa(est, pos, inc):
	    	try:
	        	pos+=inc
	    		while est[pos] == -jugador:
	    			if estado[pos+inc] == -jugador:
	    				pos+=inc
	    				continue
	    			else:
	    				if estado[pos+inc] == 0:
	    					return pos+inc
	    				else:
	    					break
	    	except:
	    		pass
	    	return -1

        def horizontal(est,pos,tipo):
        	#tipo 0 = izquierda, tipo 1 = derecha
        	return checa(est,pos,tipo*2-1)
        def vertical(est,pos,tipo):
        	#tipo 0 = arriba, tipo 1 = abajo
        	return checa(est,pos,tipo*16-8)
        def diagonal_abajo(est,pos,tipo):
        	#tipo 0 = positiva, tipo 1 = negativa
        	return checa(est,pos,7+2*tipo)
        def diagonal_arriba(est,pos,tipo):
        	#tipo 0 =positiva, tipo 1 = negativa
        	return checa(est,pos,-7-2*tipo)

        jugadas_legales = []
        #Buscamos en todas casillas
        for i in xrange(64):
        	#Si la casilla inspeccionada es del jugador..
            if(estado[i] == jugador):
            	#Buscamos en horizontal, vertical y las diagonales por todas las posibles jugadas
            	for j in xrange(2):
	            	a = horizontal(estado,i,j)
	            	if a > 0:
	            		jugadas_legales.append(a)
	            	a = vertical(estado,i,j)
	            	if a > 0:
	            		jugadas_legales.append(a)
	            	a = diagonal_abajo(estado,i,j)
	            	if a > 0:
	            		jugadas_legales.append(a)
	            	a = diagonal_arriba(estado,i,j)
	            	if a > 0:
	            		jugadas_legales.append(a)

	  	return tuple( (None,a) for a in jugadas_legales)

    

    def estado_terminal(self, estado):
    	try:
    		return estado.index(0) if False else None
    	except:
    		contador = sum(estado[i] for i in xrange(64))
    		return 100 if contador > 0 else -100 if contador < 0 else 0

       
    
    def hacer_jugada(self, estado, jugada, jugador):
        """
        Devuelve estado_nuevo que es el estado una vez que se
        realizó la juagada por el jugador.

        Checaremos desde la posicion 'jugada' (que es la que seleccion el jugador),
        y nos iremos en las 8 posibles direcciones para verificar si hay algun camino
        de fichas del otro jugador, terminando en una ficha del jugador actual;
        En caso de que esto pase, transformaremos todas las fichas en medio de la ruta
        a las fichas del jugador actual.
        """
        e = list(estado)
        
        finale = copy.copy(e)
        iteradores = {1,-1,8,-8,7,9,-7,-9}
        for i in iteradores:
            jaux = jugada[1] + i
            try:
                while e[jaux] == -jugador:
                    if e[jaux+i] == -jugador:
                        jaux+=i
                        continue
                    else:
                        if e[jaux+i] == jugador:
                            for j in xrange(abs( (jugada[1]-(jaux+i) ) //i)):
                                finale[jugada[1]+j*i] = jugador
                    	        print "ficha puesta"
                        else:
                            break
                	   
            except:
                pass
        return tuple(finale)

class JugadorOthello(juegos_cuadricula.JugadorNegamax):
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
            return abs(jugada[1]%8 -4)

        sorted(jugadas,key=en_medio)
        return jugadas

    def utilidad(self, juego, estado):

        def sumar_esquinas(estado):
            return estado[0]+estado[63]+estado[7]+estado[56]
        def num_fichas(estado):
            return sum(estado[i] for i in xrange(64))
        def sumar_centros(estado):
        	return estado[28]+estado[29]+estado[36]+estado[37]


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
            a1 = 4.0
            a2 = 1.0
            a3 = 2.0
            return a1*sumar_esquinas(estado) + a2*num_fichas(estado) + a3*sumar_centros(estado)
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
    juego = juegos_cuadricula.InterfaseTK(Othello(),
                                          juegos_cuadricula.JugadorHumano(),
                                          JugadorOthello(4),
                                          1)
    juego.arranca()


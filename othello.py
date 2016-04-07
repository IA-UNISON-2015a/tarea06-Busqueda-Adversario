#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
import juegos_cuadricula
__author__ = 'Ruben Dario Pineda'

class Othello(juegos_cuadricula.Juego2ZT):
	"""
	Juego del Othello utilizando la definición de juego utilizada
	en la clase juego_tablero.JuegoT2ZT. Todos los modulos se deben
	de reescribir en función del nuevo problema.

	"""
	def __init__(self):
		"""
		Inicializa el juego, esto es: el número de columnas y
		renglones y el estado inicial del juego.

		                 0   1   2   3   4   5   6   7   
		                 8   9  10  11  12  13  14  15
		                16  17  18  19  20  21  22  23
		                24  25  26  27  28  29  30  31
		                32  33  34  35  36  37  38  39
		                40  41  42  43  44  45  46  47
		                48  49  50  51  52  53  54  55
		                56  57  58  59  60  61  62  63
		El juego empieza con las piezas centrales 27 y 36 tomadas por el jugador 1
		Y las fichas 28 y 35 tomadas por el jugador -1

		"""
		estado_inicial = [0 for _ in range(64)]
		estado_inicial[27], estado_inicial[36] = -1
		estado_inicial[28], estado_inicial[35] = 1
		juegos_cuadricula.Juego2ZT.__init__(self,
		                                    8, 8,
		                                    tuple(estado_inicial))


    def jugadas_legales(self,estado,jugador):
    	"""
		Encuentra todas las jugadaslegales, que son las
        posiciones donde puede haber intercambio de fichas.

        @param estado: Una tupla con el estado del juego
        @param jugador: En este caso no importa ya que las jugadas son iguales

        @return: Una tupla valores con las jugadas legales
    	"""
    	jugadasleg = []

    	def busca_arriba(estado,pos,jugador):
    		if pos < 0 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_arriba(estado,pos - 8,jugador)
    	
    	def busca_izq(estado,pos,jugador):
    		if (pos + 1) % 8 == 0 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] = jugador * -1:
    			return busca_izq(estado,pos - 1,jugador)

    	def busca_der(estado,pos,jugador):
    		if pos % 8 == 0 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_der(estado,pos + 1,jugador)

    	def busca_abajo(estado,pos,jugador):
    		if pos >= 64 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_abajo(estado,pos + 8,jugador)

    	def busca_arriba_izq(estado,pos,jugador):
    		if (pos + 9) % 8 == 0 or pos + 9 < 8 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_arriba_izq(estado,pos - 9,jugador)

    	def busca_arriba_der(estado,pos,jugador):
    		if (pos + 8) % 8 == 0 or pos + 7 < 8 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_arriba_der(estado,pos - 7,jugador) 

    	def busca_abajo_izq(estado,pos,jugador):
    		if (pos - 7) % 8 == 0 or pos >= 64 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_abajo_izq(estado,pos + 7,jugador)

    	def busca_abajo_der(estado,pos,jugador):
    		if (pos - 8) % 8 == 0 or pos - 9 >= 56 or estado[pos] == jugador:
    			return None
    		else if estado[pos] == 0:
    			return pos
    		else if estado[pos] == jugador * -1:
    			return busca_abajo_der(estado,pos + 9,jugador)

    	for i in range(64):
    		if estado[i] != jugador:
    			pass
    		else:
    			# CHECO ARRIBA SI NO ESTOY EN LA PRIMERA FILA Y SI HAY UNA FICHA CONTRARIA ARRIBA 
    			if i-8 >= 0 and estado[i - 8] == (jugador * -1):
    				if pos = busca_arriba(estado,i - 8,jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    			# CHECA A LA IZQUIERDA SI NO ESTOY EN LA PRIMERA COLUMNA Y SI HAY UNA FICHA CONTRARIA A LA IZQUIERDA
    			if (i % 8) != 0 and estado[i - 1] == (jugador * -1):
    				if pos = busca_izq(estado,i - 1,jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    			# CHECA A LA DERECHA SI NO ESTOY EN LA ULTIMA COLUMNA Y SI HAY UNA FICHA CONTRARIA A LA DERECHA	
    			if ((i+1) % 8) != 0 and estado[i + 1] == jugador * -1:
    				if pos = busca_der(estado,i + 1,jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    			# CHECA ABAJO SI NO ESTOY EN LA ULTIMA FILA Y SI HAY UNA FICHA CONTRARIA ABAJO
    			if i+8 < 64 and estado[i + 8] == jugador * -1:
    				if pos = busca_abajo(estado,i + 8,jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    			# CHECA ARRIBA Y ALA IZQUIERDA EN DIAGONAL SI HAY UNA FICHA CONTRARIA EN ESA DIRECCION
    			if (i > 8 and (i % 8) != 0) and estado[i - 9] == jugador * -1:
    				if pos = busca_arriba_izq(estado,i - 9, jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    			# CHECA ARRIBA Y A LA DERECHA EN DIAGONAL, SI HAY UNA FICHA CONTRARIA EN ESA DIRECCION
    			if (i >= 8 and (i+1) % 8 != 0) and estado[i - 7] == jugador * -1:
    				if pos = busca_arriba_der(estado,i - 7,jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    			# CHECA ABAJO A LA IZQUIERDA EN DIAGONAL, SI HAY UNA FICHA CONTRARIA EN ESA DIRECCION
    			if (i <= 55 and i % 8 != 0) and estado[i + 7] == jugador * -1:
    				if pos = busca_abajo_izq(estado,i + 7,jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)
    			#CHECA EN DIAGONAL HACIA ABAJO-DERECHA SI HAY UNA FICHA CONTRARIA EN ESA DIRECCION
    			if (i <= 55 and (i+1) % 8 != 0) and estado[i + 9] == jugador * -1:
    				if pos = busca_abajo_der(estado,i + 9, jugador):
    					if pos not in jugadaslegales:
    						jugadaslegales.append(pos)

    	if jugadaslegales:
    		return [(None,i) for i in jugadaslegales]
    	else:
    		return None

    def estado_terminal(self,estado):
    	"""
    	Revisa las jugadas legales, si no hay jugadas legales para ningun
    	jugador se termina el juego

   		@param estado: una tupla con el estado del juego

   		@return: 1 si estado es terminal y gana jugador 1
                -1 si estado es terminal y gana jugador -1
                 0 si estado es terminal y es empate
                 None si estado no es terminal

    	"""
        def contar_puntos(estado):
            suma = 0
            for i in range(64):
                suma += estado[i]

    	if jugadaslegales(estado,1) or jugadaslegales(estado,-1):
    		return None
    	else:
            a =  contar_puntos(estado)
    	    if a == 0:
                return 0
            else if a > 0:
                return 1
            else if a < 0:
                return -1

	
	def hacer_jugada(self,estado,jugada,jugador):
		"""
		Devuelve estado_nuevo que es el estado una vez que se
        realizó la jugada.

        @param estado: una tupla con el estado actual
        @param jugada: una tupla con la jugada a realizar
        @param jugador: el jugador que realizara la jugada

        @return: regresa el estado nuevo con la jugada ya realizada
		""" 

		def checa_arriba(estado,jugada,jugador):
            if jugada < 0 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_arriba(estado,jugada - 8,jugador)

        def checa_izq(estado,jugada,jugador):
            if (jugada + 1) % 8 == 0 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_izq(estado,jugada - 1,jugador)

        def checa_der(estado,jugada,jugador):
            if jugada % 8 == 0 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_izq(estado,jugada + 1,jugador)

        def checa_abajo(estado,jugada,jugador):
            if jugada >= 64 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_abajo(estado,jugada + 8,jugador)

        def checa_arriba_izq(estado,jugada,jugador):
            if (jugada + 9) % 8 == 0 or jugada + 9 < 8 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_arriba_izq(estado, jugada - 9,jugador)

        def checa_arriba_der(estado,jugada,jugador):
            if (pos + 8) % 8 == 0 or pos + 7 < 8 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_arriba_der(estado,jugada - 7,jugador)

        def checa_abajo_izq(estado,jugada,jugador):
            if (jugada - 7) % 8 == 0 or jugada >= 64 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_abajo_izq(estado,jugada + 7,jugador)

        def checa_abajo_der(estado,jugada,jugador):
            if (jugada - 8) % 8 == 0 or jugada - 9 >= 56 or estado[jugada] == 0:
                return None
            else if estado[jugada] == jugador:
                return 1
            else if estado[jugada] == jugador * -1:
                return checa_abajo_der(estado,jugada + 9,jugador)

        def cambia_fichas(estado,jugada,incremento,jugador):
            """
            Cambia el valor de las fichas que esten entre la jugada elegida y la ficha de referencia

            @param estado: Es el estado actual del juego
            @param jugada: La posicion de la jugada que se realizara
            @param incremento: El incremento para realizar el cambio en el sentido que se desea
            @param jugador: El valor del jugador que realiza la jugada

            @return: Regresa el estado modificado con la jugada
            """
            i = jugada
            while estado[i[1]] != jugador:
                estado[i[1]] == jugador
                i += incremento

        estado_n = list(estado)

        #Cambiar Arriba
        if jugada[1] >= 8 and estado[jugada[1] - 8] == jugador * -1:
            if checa_arriba(estado,jugada[1] - 8,jugador):
                cambia_fichas(estado_n,jugada[1] - 8,-8,jugador)
        #Cambiar Izquierda
        if jugada[1] % 8 !=0 and estado[jugada[1] - 1] == jugador * -1:
            if checa_izq(estado,jugada[1] - 1,jugador):
                cambia_fichas(estado_n,jugada[1] - 1,-1,jugador)
        #Cambiar Derecha
        if (jugada[1] + 1) % 8 != 0 and estado[jugada[1] + 1] == jugador * -1:
            if checa_der(estado,jugada[1] + 1,jugador):
                cambia_fichas(estado_n,jugada[1] + 1, 1,jugador)
        #Cambiar Abajo
        if jugada[1] <= 55 and estado[jugada[1] + 8] == jugador * -1:
            if checa_abajo(estado,jugada[1] + 8,jugador):
                cambia_fichas(estado_n,jugada[1] + 8, 8,jugador)
        #Cambiar Arriba Izq
        if (jugada[1] >= 8 and jugada[1] % 8 != 0) and estado[jugada[1] - 9] == jugador * -1:
            if checa_arriba_izq(estado,jugada[1] - 9,jugador):
                cambia_fichas(estado_n,jugada[1] - 9, -9,jugador)
        #Cambiar Arriba Derecha
        if (jugada[1] >= 8 and (jugada[1] + 1) % 8 != 0) and estado[jugada[1] - 7] == jugador * -1:
            if checa_arriba_der(estado,jugada[1] - 7,jugador):
                cambia_fichas(estado_n,jugada[1] - 7, -7,jugador)
        #Cambiar Abajo Izq
        if (jugada[1] <= 55 and jugada[1] % 8 != 0) and estado[jugada[1] + 7] == jugador * -1:
            if checa_abajo_izq(estado,jugada[1] + 7,jugador):
                cambia_fichas(estado_n,jugada[1] + 7, 7,jugador)
        #Cambiar Abajo Derecha
    	if (jugada[1] <= 55 and (jugada[1] + 1) % 8 != 0) and estado[jugada[1] + 9] == jugador * -1:
            if checa_abajo_der(estado,jugada[1] + 9,jugador):
                cambia_fichas(estado_n,jugada[1] + 9, 9,jugador)		

        return tuple(estado_n)

class JugadorOthello(juegos_cuadricula.JugadorNegamax):
    """
    Un jugador Negamax ajustado a el juego Othello
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
        shuffle(jugadas)
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
        val = juego.estado_terminal(estado)
        if val is None:
            return 0
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

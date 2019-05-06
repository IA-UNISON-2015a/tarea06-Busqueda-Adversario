#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
timbiriche.py
------------

El juego de Timbiriche implementado por ustedes mismos, con jugador inteligente

"""

__author__ = 'Ricardo E. Alvarado Mata'

import random
from datetime import datetime
from busquedas_adversarios import JuegoSumaCeros2T, minimax

random.seed()

class Timbiriche(JuegoSumaCeros2T):
    """
    Juego de timbiriche o puntos y cajas ("dots and boxes" en ingles)
    descripcion del juego en wikipedia: https://es.wikipedia.org/wiki/Timbiriche_(juego)

    para manejar el estado se usa una tupla con los valores de las lineas pintadas, un
    1 si la puso el primer jugador y un -1 si la puso el segundo, primero se guardan
    todas las lineas horizontales empezando de izquierda a derecha y de arriba a abajo,
    luego todas las verticales de la misma manera.

    El tablero es de n^2 por lo que la longitud de la lista para guardar la informacion
    del estado es 2*n*(n+1)

    Se usa una matriz auxiliar para hacer el conteo de cuadros al final del juego.
    """

    def __init__(self, n):

        self.x0 = tuple(2*n*(n+1)*[0])
        self.x = list(self.x0)
        self.n = n

        # Lista auxiliar para ayudarnos a saber a 
        # quien le pertenece cada cuadro.
        self.cuadros = n*n * [0]
        # Otra lista auxiliar que nos sirve para conocer
        # cuantos lados tiene un cuadro.
        self.grados = n*n * [0]
        self.historial = []
        self.jugador = 1
        # Variable auxiliar para conocer cuando se cierra un cuadro
        self.cuadro_cerrado = False

    def jugadas_legales(self):
        if self.cuadro_cerrado:
            return [-1]
        return (posicion for posicion in range(len(self.x)) if self.x[posicion] == 0)
    
    def terminal(self):
        if 0 in self.x:
            return None
        return sum((1 for i in self.cuadros if i == 1))
            
    
    def hacer_jugada(self, jugada):
        self.historial.append(jugada)

        if jugada == -1:
            self.jugador *= -1
            self.cuadro_cerrado = False
            return

        self.x[jugada] = 1

        # Verificamos si el jugador completo un cuadro.
        mid = int(len(self.x)/2)

        # Se jugo una linea horizontal.
        if jugada < mid:
            ren = int(jugada / self.n)

            if ren < self.n:
                self.grados[jugada] += 1
                if self.grados[jugada] == 4:
                    self.cuadros[jugada] = self.jugador
                    self.cuadro_cerrado = True
            if ren > 0:
                self.grados[jugada-self.n] += 1
                if self.grados[jugada-self.n] == 4:
                    self.cuadros[jugada-self.n] = self.jugador
                    self.cuadro_cerrado = True
        # Se jugo una linea vertical.
        else:
            ren = int((jugada-mid) / (self.n+1))
            col = int((jugada-mid) % (self.n+1))

            if col < self.n:
                self.grados[jugada-mid-ren] += 1
                if self.grados[jugada-mid-ren] == 4:
                    self.cuadros[jugada-mid-ren] = self.jugador
                    self.cuadro_cerrado = True
            if col > 0:
                self.grados[jugada-mid-ren-1] += 1
                if self.grados[jugada-mid-ren-1] == 4:
                    self.cuadros[jugada-mid-ren-1] = self.jugador
                    self.cuadro_cerrado = True

        self.jugador *= -1

    def deshacer_jugada(self):
        jugada = self.historial.pop()
        if jugada == -1:
            self.jugador *= -1
            return

        self.cuadro_cerrado = False

        mid = int(len(self.x)/2)
       
       # Se jugo una linea horizontal.
        if jugada < mid:
            ren = int(jugada / self.n)

            if ren < self.n:
                self.grados[jugada] -= 1
                self.cuadros[jugada] = 0
                    
            if ren > 0:
                self.grados[jugada-self.n] -= 1
                self.cuadros[jugada-self.n] = 0
        # Se jugo una linea vertical.
        else:
            ren = int((jugada-mid) / (self.n+1))
            col = int((jugada-mid) % (self.n+1))

            if col < self.n:
                self.grados[jugada-mid-ren] -= 1
                self.cuadros[jugada-mid-ren] = 0
                
            if col > 0:
                self.grados[jugada-mid-ren-1] -= 1
                self.cuadros[jugada-mid-ren-1] = 0

        self.x[jugada] = 0
        self.jugador *= -1

# Heuristicas

# Distancia manhattan de las lineas con el centro.
def ordenamiento_manhattan(juego):
    def criterio(a):
        if a < len(juego.x)/2:
            ren, col = a / juego.n, a % juego.n
            return abs(ren - (juego.n+1) / 2) + abs(col - juego.n / 2)
        else:
            ren, col = a / (juego.n+1), a % (juego.n+1)
            return abs(ren - juego.n / 2) + abs(col - (juego.n+1) /2)
    
    return sorted(juego.jugadas_legales(), key=criterio)

def ordenamiento_aleatorio(juego):
    cplist = list(juego.jugadas_legales())
    random.shuffle(cplist)
    return cplist

def utilidad_fool(juego):
    if 4 in juego.grados:
        return sum((1 for i in juego.cuadros if i == 1))
    return random.randint(0, juego.n*2)

def utilidad_ingenua(juego):
    return sum(juego.cuadros) - (1 - juego.cuadro_cerrado) * sum((1 for i in juego.grados if i == 3))


def obtener_cadenas(juego):
    longitud_cadenas = []
    cuadros_cadenas = {}

    def sigue_cadena(indice, longitud_cadenas, cuadros_cadenas):
        n = juego.n
        mid = int(len(juego.x)/2)

        if indice//n > 0:
            if juego.grados[indice-n] >= 2 and juego.cuadros[indice-n] == 0:
                if indice-n not in cuadros_cadenas.keys() and juego.x[indice] == 0:
                    cuadros_cadenas[indice-n] = cuadros_cadenas[indice]
                    longitud_cadenas[-1] += 1
                    sigue_cadena(indice-n, longitud_cadenas, cuadros_cadenas)

        if indice%n > 0:
            if juego.grados[indice-1] >= 2 and juego.cuadros[indice-1] == 0:
                if indice-1 not in cuadros_cadenas.keys() and juego.x[indice+int(indice/n)+mid] == 0:
                    cuadros_cadenas[indice-1] = cuadros_cadenas[indice]
                    longitud_cadenas[-1] += 1
                    sigue_cadena(indice-1, longitud_cadenas, cuadros_cadenas)

        if indice%n < n-1:
            if juego.grados[indice+1] >= 2 and juego.cuadros[indice+1] == 0:
                if indice+1 not in cuadros_cadenas.keys() and juego.x[indice+int(indice/n)+mid+1] == 0:
                    cuadros_cadenas[indice+1] = cuadros_cadenas[indice]
                    longitud_cadenas[-1] += 1
                    sigue_cadena(indice+1, longitud_cadenas, cuadros_cadenas)
        
        if indice//n < n-1:
            if juego.grados[indice+n] >= 2 and juego.cuadros[indice+n] == 0:
                if indice+n not in cuadros_cadenas.keys() and juego.x[indice+n] == 0:
                    cuadros_cadenas[indice+n] = cuadros_cadenas[indice]
                    longitud_cadenas[-1] += 1
                    sigue_cadena(indice+n, longitud_cadenas, cuadros_cadenas)

    for i, (g, c) in enumerate(zip(juego.grados, juego.cuadros)):
        if g >= 2 and c == 0 and i not in cuadros_cadenas.keys():
            longitud_cadenas.append(1)
            cuadros_cadenas[i] = len(longitud_cadenas)-1
            sigue_cadena(i, longitud_cadenas, cuadros_cadenas)
    
    return (cuadros_cadenas, longitud_cadenas)

def calcular_cajas_muertas(juego, cuadros_cadenas, longitud_cadenas):
    jugador = juego.jugador * (-1 if juego.cuadro_cerrado else 1)
    cadenas_muertas = []
    
    num_cajas_muertas = 0
    for i in range(juego.n**2):
        if juego.grados[i] == 3 and cuadros_cadenas[i] not in cadenas_muertas:
            cadenas_muertas.append(cuadros_cadenas[i])
            num_cajas_muertas += longitud_cadenas[cuadros_cadenas[i]]
    
    return num_cajas_muertas * jugador


def utilidad_cadenas_parametrizadas(a,b,c):
    def utilidad_cadenas(juego):
        cuadros_cadenas, longitud_cadenas = obtener_cadenas(juego)
        cajas_estimadas = 0

        cajas_muertas = calcular_cajas_muertas(juego, cuadros_cadenas, longitud_cadenas)

        longitud_cadenas.sort()

        for i in range(len(longitud_cadenas)):
            if i%2 == len(longitud_cadenas)%2:
                cajas_estimadas += longitud_cadenas[i]

        return a*sum(juego.cuadros) + b*cajas_estimadas + c*cajas_muertas
    return utilidad_cadenas

# Jugadores

def jugador_humano(partida):
    if partida.jugadas_legales() == -1:
        return -1

    print("\nIngresa el renglon y la comluna del punto que quieras conectar "+
            "luego con que punto adyacente a este lo quieres conectar "+
            "{arr,abj,izq,der}\n")
    
    ren = 0
    col = 0
    direc = ''
    
    while True:
        while True:
            try:
                ren = int(input("\nrenglon[1,{}]: ".format(partida.n+1)))
                if ren not in range(1,partida.n+2):
                    raise Exception()
                break
            except:
                print("\nError: numero invalido.")
                continue

        while True:
            try:
                col = int(input("\ncolumna [1,{}]: ".format(partida.n+1)))
                if col not in range(1,partida.n+2):
                    raise Exception()
                break
            except:
                print("\nError: numero invalido.")
                continue
        
        while True:
            posibles_direcciones = set()

            if col < partida.n+1:
                posibles_direcciones.add('der')
            if col > 1:
                posibles_direcciones.add('izq')
            if ren > 1:
                posibles_direcciones.add('arr')
            if ren < partida.n+1:
                posibles_direcciones.add('abj')

            try:
                direc = input("\ndireccion {}: ".format(posibles_direcciones))
            
                if direc not in posibles_direcciones:
                    raise Exception()
                break
            except:
                print("\nDireccion invalida,\nlos posibles valores son: " +
                    " {}\n".format(posibles_direcciones))
                continue

        ren -= 1
        col -= 1

        mid = int(len(partida.x)/2)

        jugada = (ren*(partida.n+1) + col)
        jugada += (-ren - 1 if direc == 'izq' else
                    -ren  if direc == 'der' else
                    mid-partida.n-1 if direc == 'arr' else mid)
        if jugada not in partida.jugadas_legales():
            print("\nJugada ilegal: {}".format(jugada))
            print("Jugadas legales: {}".format(list(partida.jugadas_legales())))
            continue
        break

    return jugada
    
def jugador_minimax_raw(partida):
    return minimax(partida)

def jugador_minimax_ord_dist_l1(partida):
    return minimax(partida, ordena_jugadas=ordenamiento_manhattan)

def jugador_minmax_heuristica_fool(partida):
    return minimax(partida, utilidad=utilidad_fool, dmax=5)

def jugador_minmax_heuristica_fool_ord_dist_l1(partida):
    return minimax(partida, ordena_jugadas=ordenamiento_manhattan, utilidad=utilidad_fool, dmax=4)

def jugador_aleatorio(partida):
    return random.choice(list(partida.jugadas_legales()))

def generar_jugador_definitivo(a,b,c):
    def jugador_definitivo(partida):
        if len(partida.historial) < partida.n*partida.n/4:
            return minimax(partida, dmax=1,utilidad=utilidad_ingenua, ordena_jugadas=ordenamiento_aleatorio)
        elif len(partida.x) - sum(partida.x) <= 10:
            return minimax(partida, ordena_jugadas=ordenamiento_manhattan)
        else:
            #jug_restantes = 2*partida.n*(partida.n+1) - sum(partida.x)
            utilidad_cadenas = utilidad_cadenas_parametrizadas(a,b,c)
            return minimax(partida, dmax=4, utilidad=utilidad_cadenas, ordena_jugadas=ordenamiento_manhattan)
    return jugador_definitivo


def juega_timbiriche(jugador1, jugador2, n):
    partida = Timbiriche(n)
    pinta_tablero_timbiriche(partida)
    numero_jugada = 1
    while partida.terminal() == None:
        print("\nJugada numero: {}".format(numero_jugada))
        if partida.jugadas_legales() != [-1]:
            if partida.jugador == 1:
                print("\nTurno del jugador A:\n")
                partida.hacer_jugada(jugador1(partida))
                print("\nJugada del jugador A:")
                pinta_tablero_timbiriche(partida)
            else:
                print("\nTurno del jugador B:\n")
                partida.hacer_jugada(jugador2(partida))
                print("\nJugada del jugador B:")
                pinta_tablero_timbiriche(partida)
                
            numero_jugada += 1
        else:
            partida.hacer_jugada(-1)
    
    puntos_jugador1 = partida.terminal()
    puntos_jugador2 = partida.n*partida.n - puntos_jugador1

    if puntos_jugador1 > puntos_jugador2:
        print("\nHa ganado el jugador 1.\n")
    elif puntos_jugador1 < puntos_jugador2:
        print("\nHa ganado el jugador 2.\n")
    else:
        print("\nHa sido un empate.\n")


# Funciones de utileria para probar las IAs

def juega_timbiriche_simulacion(jugador1, jugador2, n):
    partida = Timbiriche(n)
    numero_jugada = 1
    while partida.terminal() == None:
        if partida.jugadas_legales() != [-1]:
            if partida.jugador == 1:
                partida.hacer_jugada(jugador1(partida))
            else:
                partida.hacer_jugada(jugador2(partida))
            numero_jugada += 1
        else:
            partida.hacer_jugada(-1)
    
    puntos_jugador1 = partida.terminal()
    puntos_jugador2 = partida.n*partida.n - puntos_jugador1

    if puntos_jugador1 > puntos_jugador2:
        return 1
    elif puntos_jugador1 < puntos_jugador2:
        return -1
    return 0

def prueba_jugadores_maquina(jugador1, jugador2, n, num_juegos=100):
    puntage_jugador1 = 0
    puntage_jugador2 = 0
    empates = 0
    print("progress: [          ] 0%...", end='')
    for i in range(num_juegos):
        ganador = juega_timbiriche_simulacion(jugador1, jugador2, n)
        if ganador > 0:
            puntage_jugador1 += 1
        elif ganador < 0:
            puntage_jugador2 += 1
        else:
            empates += 1

        dunno = int(((i+1)/num_juegos)*10)
        some_var = '*'*dunno + ' '*(10-dunno)
        print("\rprogress:[{}] {}%...".format(some_var, 10*dunno), end='')
    
        print("\nEl jugador1 gano {} juegos\nEl jugador2 gano {} juegos\nHubo {} empates".format(puntage_jugador1, puntage_jugador2, empates))



def pinta_tablero_timbiriche(partida):
    tablero = ''
    mid = int(len(partida.x)/2)
    for i in range(partida.n):
        tablero += '■'
        for j in range(partida.n):
            tablero += ' ─ ' if partida.x[i*partida.n+j] == 1 else '   '
            tablero += '■'

        tablero += '\n'

        for j in range(partida.n):
            tablero += '│' if partida.x[i*partida.n+j+i+mid] == 1 else ' '
            tablero += {-1:' B ', 0:'   ', 1:' A '}[partida.cuadros[i*partida.n+j]]

        tablero += '│\n' if partida.x[(i+1)*partida.n+i+mid] == 1 else '\n'

    tablero += '■'

    for i in range(partida.n):
        tablero += ' ─ ' if partida.x[i+partida.n*partida.n] != 0 else '   '
        tablero += '■'
    
    print('\n\n'+tablero+'\n')

if __name__ == '__main__':
    jugador_maquina1 = generar_jugador_definitivo(4,1,2)
    jugador_maquina2 = generar_jugador_definitivo(1,1,2)
    juega_timbiriche(jugador1=jugador_humano, jugador2=jugador_maquina2, n=3)

    #prueba_jugadores_maquina(jugador_maquina1, jugador_maquina2, 3, 20)


        


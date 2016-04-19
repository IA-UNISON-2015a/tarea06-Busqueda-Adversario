#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Nan'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
import juegos_cuadricula
import time

class Othello(juegos_cuadricula.Juego2ZT):
    
    def __init__(self):
        ini = [0]*64
        ini[27], ini[36], ini[28], ini[35] = 1,1,-1,-1
        juegos_cuadricula.Juego2ZT.__init__(self,8,8, ini)
        
    def jugadas_legales(self, estado, jugador):
        legales = [(None, i*8+j) for i in range(8) for j in range(8) 
                    if estado[i*8+j] == 0 and [x for x in 
                    self.para_donde_y_hasta_cuando(estado, i, j, jugador)] != []]
        return legales if len(legales) > 0 else [(None, -1)]
                
    def estado_terminal(self, estado):
        if (self.jugadas_legales(estado, 1)[0][1] > -1 or
                self.jugadas_legales(estado,-1)[0][1] > -1):
            return None
        
        s = sum(estado)
        
        return 1 if s > 0 else -1 if s < 0 else 0
        
    def hacer_jugada(self, estado, jugada, jugador):
        if jugada[1] == -1:
            return estado
        s = list(estado)
        for (x,y,m) in self.para_donde_y_hasta_cuando(
                estado, jugada[1]/8, jugada[1]%8, jugador):
            for i in range(m+1):
                s[jugada[1] + x*i + 8*y*i] = jugador
        return tuple(s)
    
    @staticmethod
    def para_donde_y_hasta_cuando(estado, i, j, jugador):
        for (x,y) in Othello.direcciones():
            if Othello.inBounds(i+y, j+x) and estado[(i+y)*8+j+x] == -jugador:
                dist = 1
                while Othello.inBounds(i+y*dist, 
                        j+x*dist):
                    if estado[(i+y*dist)*8+j+x*dist] == jugador:
                        yield (x, y, dist)
                        break
                    elif estado[(i+y*dist)*8+j+x*dist] == 0:
                        break
                    dist += 1
        
                
    @staticmethod
    def direcciones():
        for d in [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]:
            yield d
        
    @staticmethod
    def inBounds(x,y):
        return x>=0 and x<8 and y>=0 and y<8
                    
class JugadorOthello(juegos_cuadricula.JugadorNegamax):
    
    def __init__(self, tiempo_espera):
        juegos_cuadricula.JugadorNegamax.__init__(self, d_max=1)
        self.tiempo = tiempo_espera
        self.maxima_d = 20
    
    def ordena(self, juego, estado, jugadas, jugador): 
        jugadas.sort(key=lambda j: -self.chilometro(juego, estado, j, jugador))
        return jugadas
        
    def utilidad(self, juego, estado):
        s = (estado[0]+estado[7]+estado[56]+estado[63])
        return (self.jugador if s > 0 else -self.jugador if s < 0 else 0)
                
    @staticmethod
    def chilometro(juego, estado, jugada, jugador):
        s = juego.hacer_jugada(estado, jugada, jugador)
        r = sum([s[i]-estado[i] for i in [0,7,56,63]])
        if r != 0 :
            return r*jugador
        return 0
        
            
                
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
    juego = juegos_cuadricula.InterfaseTK(Othello(),
                                        #JugadorOthello(4),
					                    juegos_cuadricula.JugadorHumano(),
                                        JugadorOthello(4),
                                        1)
                                        
    juego.arranca()

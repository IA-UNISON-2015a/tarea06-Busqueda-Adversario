#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
timbiriche.py
------------

El juego de Timbiriche implementado por ustedes mismos, con jugador inteligente

"""

__author__ = 'Lizeth Soto Félix'

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
from busquedas_adversarios import minimax_t
from random import shuffle
class DotsAndBoxes(JuegoSumaCeros2T):
    """
    El juego del DotsAndBoxes para ilustrar los modelos de juegos

    """
    def __init__(self, jugador=1, n=3):
        """
        Inicializa el juego del DotsAndBoxes

        """
        self.n = n
        self.x0 = n * [0]
        for _ in range (n):
            self.x0 += (n+1) * [0]
            self.x0 += n * [0]
        
        
        self.x = n * [0]
        for _ in range (n):
            self.x += (n+1) * [0]
            self.x += n * [0]

        self.historial = []
        self.jugador = 1
        self.rayas_a_cuadros = {}
        self.cuadros_a_rayas= {}
        k=0
        for i in range (n):
            for j in range (n):
                self.cuadros_a_rayas[i*n+j]= [j+k,j+n+k,j+n+1+k,j+2*n+1+k]
            k+=2*n +1

        for k,v in self.cuadros_a_rayas.items():
            for x in v:
                self.rayas_a_cuadros.setdefault(x,[]).append(k)
        
            

    def jugadas_legales(self):
         if len(self.historial) is 0 or self.jugador*-1 not in self.historial[-1][1]:
            return (posicion for posicion in range(len(self.x)) if self.x[posicion] == 0)
         else:
            return [-1]

    def terminal(self):
        if 0 in self.x:
            return None
        cuadrados_completos = self.historial[-1][-1][:]
        if 0 in cuadrados_completos:
            return None
      
        j1 = cuadrados_completos.count(1)
        j2 = cuadrados_completos.count(-1)
        if j1 == j2:
            return 0
        elif j1 > j2:
            return 1
        elif j2 > j1:
            return -1

        
    

    def hacer_jugada(self, jugada):
        if jugada != -1:
            self.x[jugada] = self.jugador
            cuadrados_terminados_esta_jugada,cuadrados_terminados_array_ordenado = self.cuadrado_terminado(jugada)
        else:
            _,cuadrados_terminados_esta_jugada,cuadrados_terminados_array_ordenado = self.historial[-1][:]
        self.historial.append((jugada,cuadrados_terminados_esta_jugada,cuadrados_terminados_array_ordenado))
        #if jugada is 11:
            #print(self.x)
        self.jugador *= -1

    def deshacer_jugada(self):
        jugada,_,_ = self.historial.pop()
        if jugada != -1:
            self.x[jugada] = 0     
        self.jugador *= -1

        
    def cuadrado_terminado(self,jugada):
        flag = 0
        cuadrados_terminados = []
        cuadrados_terminados_array_ordenado = self.historial[-1][-1][:] if len(self.historial) > 0 else (self.n*self.n) * [0]
        for i in self.rayas_a_cuadros.get(jugada):
            for j in self.cuadros_a_rayas.get(i):
                if self.x[j] == 0:
                    break
            else:
                cuadrados_terminados.append(self.jugador)
                cuadrados_terminados_array_ordenado[i] = self.jugador
                flag+=1
            if len(cuadrados_terminados) is 2:
                break              
        return cuadrados_terminados,cuadrados_terminados_array_ordenado[:]
     
def utilidad_t(juego):
    flag =0
    if len(juego.historial) is not 0:
        flag+= juego.historial[-1][-1].count(juego.jugador*-1)
        flag-= juego.historial[-1][-1].count(juego.jugador)
    for cuadrado in juego.cuadros_a_rayas:
        if juego.rayas_a_cuadros.get(cuadrado).count(0) is 1:
            flag-=1
    utilidad = flag / (juego.n*juego.n)
    
    return utilidad


def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    #Random al incio
    if juego.x.count(0)>(len(juego.x)*2)/3:
        shuffle(jugadas)
        return jugadas
    else:
        #Despues por utilidad
        utilidades = []
        for jugada in jugadas:
            juego.hacer_jugada(jugada)
            utilidades.append(utilidad_t(juego))
            juego.deshacer_jugada()
    
        return [x for (_, x) in sorted(zip(utilidades, jugadas))]
            

    
def juega_DotsAndBoxesSolis(jugador="X"):
    def hacer_jugada(juego, jugada):
        juego.x[jugada] = juego.jugador
        cuadrados_terminados_esta_jugada,cuadrados_terminados_array_ordenado = juego.cuadrado_terminado(jugada)
        juego.historial.append((jugada,cuadrados_terminados_esta_jugada,cuadrados_terminados_array_ordenado))

        if len(cuadrados_terminados_esta_jugada) is 0:
            juego.jugador *= -1
        
    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = DotsAndBoxes()

    print("El juego del DotsAndBoxes".center(60))
    print("las 'X' siempre empiezan".center(60))
    print("y tu juegas con {}".format(jugador).center(60))

    if jugador is 'O':
        jugada = minimax(juego)
        hacer_jugada(juego,jugada)

    acabado = False
    while not acabado:
        pprint_DotsAndBoxes(juego)
        print("Escoge tu jugada (uno de los números que quedan en el DotsAndBoxes)")

        try:
            jugada = int(input("Jugador {}: ".format(juego.jugador)))
            print(jugada)
        except:
            print("Num pls")
            continue
        if jugada < 0 or jugada > len(juego.x)-1 or juego.x[jugada] != 0 :
            print("Num valido pls")
            continue

        hacer_jugada(juego,jugada)
        pprint_DotsAndBoxes(juego)
        if juego.terminal() is not None:
            acabado = True
        else:
            try:
                jugada = int(input("Jugador {}: ".format(juego.jugador)))
                print(jugada)
            except:
                print("Num pls")
                continue
            if jugada < 0 or jugada > len(juego.x)-1 or juego.x[jugada] != 0:
                print("Num valido pls")
                continue
    
            hacer_jugada(juego,jugada)
            if juego.terminal() is not None:
                acabado = True

    pprint_DotsAndBoxes(juego)
    ganador = juego.terminal()
    if ganador == 0:
        print("Empate".center(60))
    elif (ganador < 0 and jugador is 'X') or (ganador > 0 and jugador is 'O'):
        print("Gano yo".center(60))
    else:
        print("Tambien gano yo")
    print("\n\nFin del juego")
    
    
def juega_DotsAndBoxes(jugador='X'):

    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = DotsAndBoxes()

    print("El juego del DotsAndBoxes".center(60))
    print("las 'X' siempre empiezan".center(60))
    print("y tu juegas con {}".format(jugador).center(60))

    if jugador is 'O':
        jugada = minimax_t(juego,ordena_jugadas=ordena_jugadas,utilidad=utilidad_t, tmax = 60)
        #jugada = minimax(juego)
        print("sali del minimax")
        juego.hacer_jugada(jugada)


    acabado = False
    compu_completo = False
    while not acabado:
        if not compu_completo:
            pprint_DotsAndBoxes(juego)
            print("Escoge tu jugada (uno de los números que quedan en el DotsAndBoxes)")
            
            try:
                jugada = int(input("Jugador {}: ".format(jugador)))
                print(jugada)
            except:
                print("Tiene que ser número.")
                continue
            if jugada < 0 or jugada > len(juego.x)-1 or juego.x[jugada] != 0 :
                print("Tiene que ser un número de los que quedan libres.")
                continue
    
            juego.hacer_jugada(jugada)
        else:
            print("no puedo hacer nada")
            #juego.hacer_jugada(-1)
            compu_completo = False
        if juego.terminal() is not None:
            acabado = True
        else:
            #jugada = minimax(juego)
            jugada = minimax_t(juego,ordena_jugadas=ordena_jugadas,utilidad=utilidad_t,tmax = 60)
            juego.hacer_jugada(jugada)
            if jugada != -1:
                cuadrados_terminados,_ = juego.cuadrado_terminado(jugada)
                if len(cuadrados_terminados) > 0:
                    compu_completo = True

            if juego.terminal() is not None:
                acabado = True

    pprint_DotsAndBoxes(juego)
    ganador = juego.terminal()
    if ganador == 0:
        print("Empate".center(60))
    elif (ganador < 0 and jugador is 'X') or (ganador > 0 and jugador is 'O'):
        print("Gana compu".center(60))
    else:
        print("Gano yo.")
    print("\n\nFin del juego")


def pprint_DotsAndBoxes(juego):
    x= juego.x
    n= juego.n
    #print(juego.historial)
    c2 = juego.historial[-1][-1] if len(juego.historial) > 0 else (n*n)*[0]
    y = [('------' if x[i] > 0 else '~~~~~~' if x[i] < 0 else str(i))
         for i in range(len(x))]
    y2 = [('|' if x[i] > 0 else '(' if x[i] < 0 else str(i))
         for i in range(len(x))]
    c = [('X' if c2[i] > 0 else 'O' if c2[i] < 0 else " ")
         for i in range(len(c2))]
    cad_aux = ""
    carry = 0
    carry2 = 0
    #print(x)
    for i in range(n*2+1):
        cad_aux += "\n\n"
        if i % 2 is 0:
            for j in range(n):
                if len(y[i*n+j+carry]) == 6:
                    cad_aux+="°"+" "
                    cad_aux+="{}".format(y[i*n+j+carry])
                    cad_aux+=" "
                else:
                    cad_aux+="°"+" "*3
                    cad_aux+="{}".format(y[i*n+j+carry])
                    cad_aux+=" "*(5-len(y[i*n+j+carry]))
            cad_aux+="°"
            carry+=1
        else:
            for j in range(n+1):
                cad_aux+="{}   ".format(y2[i*n+j+carry2])
                if j is not n:
                    cad_aux+="{}".format(c[carry2*n+j])
                cad_aux+=" "*(5-len(y2[i*n+j+carry2]))
            carry2 += 1
        
    print(cad_aux)






if __name__ == '__main__':
    #juega_DotsAndBoxesSolis('X')
    juega_DotsAndBoxes('X')
    #DotsAndBoxesTK().arranca()
# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
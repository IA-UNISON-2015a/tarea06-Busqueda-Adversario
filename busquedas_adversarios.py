#!/usr/bin/env python
# coding: utf-8

"""
busquedas_adversarios.py
------------------------

Modulo con las funciones genericas para la búsqueda con adversarios

Para hacerlo orientado a objetos y pasar toda la información por
referencia (y hacer un poco más rápido el juego) vamos a mantener
el estado del juego y el jugador actual dentro del juego.

Se ilustra con el juego del gato

"""

from time import perf_counter


class JuegoSumaCeros2T:
    """
    Clase abstracta para juegos de suma cero, por turnos para 2 jugadores.

    Tiene al menos las siguientes propiedades

    1. x0: Estado con la posición inicial (el la mayoría de los juegos es fija)
           Una tupla (muy importante, para evitar modificar como efecto
           colateral)

    2. estado: El estado como lista para poder modificarlo rápido.

    2. historial: Notación de los cambios en los estados conforme las acciones
                  se realizan (en ajedrez es notación estandar). En algunos
                  juegos, como el otello, es necesario agregar información
                  extra para poder deshacer una jugada.

    Tiene al menos los siguientes métodos

    1. jugadas_legales(): Devueve un generador con las
       jugadas que puede realizar el jugador actual en el estado
       actual del juego

    2. terminal(): Devuelve None si no es terminal el estado actual,
       en otro caso devuelve la ganancia para el jugador 1.

    3. hacer_jugada(jugada): Realiza la jugada, modifica el estado.

    """
    def __init__(self, x0, jugador=1):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza (típicamente el primero)

        """
        self.x0 = x0
        self.x = list(x0)
        self.historial = []
        self.jugador = jugador

    def jugadas_legales(self):
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def terminal(self):
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def hacer_jugada(self, jugada):
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def deshacer_jugada(self, ultima_jugada):
        raise NotImplementedError("Hay que desarrollar este método, pues")


def minimax(juego, dmax=100, utilidad=None, ordena_jugadas=None, transp=None):
    """
    Escoje una jugada legal para el jugador en turno, utilizando el
    método de minimax a una profundidad máxima de dmax, con una función de
    utilidad (para el jugador 1) definida por utilidad y un método
    de ordenación de jugadas específico

    """
    if ordena_jugadas is None:
        def ordena_jugadas(juego):
            return juego.jugadas_legales()
    
    if utilidad is None:
        def utilidad(juego):
            return juego.terminal()
        dmax = 100
    
    
    if not ordena_jugadas(juego):
        return None
        
    return max((a for a in ordena_jugadas(juego)),
               key=lambda a: min_val(juego, a, dmax, utilidad, ordena_jugadas,
                                     -1e10, 1e10, juego.jugador, transp))
    

    

def min_val(juego, jugada, d, utilidad, ordena_jugadas,
            alfa, beta, primero, transp):
    
    print("entre min_val, hacer jugada,..", jugada)
    juego.hacer_jugada(jugada)
    #pprint_othello(juego.x)
    #input()
    

    ganancia = juego.terminal()
    #print("ganancia:", ganancia)
    
    if ganancia is not None:
        #print("des-hacer_jugada")
        juego.deshacer_jugada()
        #pprint_othello(juego.x)
        #input()
        return primero * ganancia

    #print(jugada,d, primero)
    if d == 0:
        u = utilidad(juego.x)
        #print("des-hacer_jugada")
        juego.deshacer_jugada()
        #pprint_othello(juego.x)
        #input()
        return primero * u

    if transp is not None and tuple(juego.x) in transp:
        val_tt, d_tt, tipo_tt = transp[tuple(juego.x)]
        if d_tt >= d and tipo_tt is 'beta':
            beta = min(alfa, val_tt)

    
    for jugada_nueva in ordena_jugadas(juego):
        #print("PROFUNDIDAD", d)
        beta = min(beta, max_val(juego, jugada_nueva, d - 1, utilidad,
                                 ordena_jugadas, alfa, beta, primero, transp))
        #print("Regrese de max_val")
        if beta <= alfa:
            break
    else:
        if transp is not None:
            transp[tuple(juego.x)] = (d, beta, 'beta')
    juego.deshacer_jugada()
    return beta


def max_val(juego, jugada, d, utilidad, ordena_jugadas,
            alfa, beta, primero, transp):
    
    print("entre max_val, hacer jugada", jugada)
    juego.hacer_jugada(jugada)
    #pprint_othello(juego.x)
    #input()
    
    ganancia = juego.terminal()
    #print("ganancia:", ganancia)
    
    if ganancia is not None:
        #print("des-hacer_jugada")
        juego.deshacer_jugada()
        #pprint_othello(juego.x)
        #input()
        return primero * ganancia

        
    #print(jugada,d, primero)
    if d == 0:
        u = utilidad(juego.x)
        #print("des-hacer_jugada")
        juego.deshacer_jugada()
        #pprint_othello(juego.x)
        #input()
        return primero * u

    if transp is not None and tuple(juego.x) in transp:
        val_tt, d_tt, tipo_tt = transp[tuple(juego.x)]
        if d_tt >= d and tipo_tt is 'alfa':
            alfa = max(alfa, val_tt)

    for jugada_nueva in ordena_jugadas(juego):
        #print("PROFUNDIDAD", d)
        alfa = max(alfa, min_val(juego, jugada_nueva, d - 1, utilidad,
                                 ordena_jugadas, alfa, beta, primero, transp))
        #print("Regrese de min_val")
        if beta <= alfa:
            break
    else:
        if transp is not None:
            transp[tuple(juego.x)] = (d, alfa, 'alfa')
    juego.deshacer_jugada()
    return alfa


def minimax_t(juego, tmax=5, utilidad=None, ordena_jugadas=None, transp=None):

    bf = len(list(juego.jugadas_legales()))
    t_ini = perf_counter()
    for d in range(2, 50):
        ta = perf_counter()
        jugada = minimax(juego, d, utilidad, ordena_jugadas, transp=None)
        tb = perf_counter()
        if bf * (tb - ta) > t_ini + tmax - tb:
            return jugada

            
            
def pprint_othello(x):
    y = [('X' if x[i] > 0 else 'O' if x[i] < 0 else str(i))
         for i in range(64)]
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[0],y[1],y[2],y[3],y[4],y[5],y[6],y[7] ).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[8],y[9],y[10],y[11],y[12],y[13],y[14],y[15] ).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[16],y[17],y[18],y[19],y[20],y[21],y[22],y[23]).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[24],y[25],y[26],y[27],y[28],y[29],y[30],y[31]).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[32],y[33],y[34],y[35],y[36],y[37],y[38],y[39]).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[40],y[41],y[42],y[43],y[44],y[45],y[46],y[47]).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[48],y[49],y[50],y[51],y[52],y[53],y[54],y[55]).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
    print(" {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} \t| {} ".format(y[56],y[57],y[58],y[59],y[60],y[61],y[62],y[63]).center(60))
    print("+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+------\t+".center(60))
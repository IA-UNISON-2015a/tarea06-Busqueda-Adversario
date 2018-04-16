#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
from busquedas_adversarios import JuegoSumaCeros2T, minimax, minimax_t
from collections import deque
from random import shuffle
import tkinter as tk

__author__ = 'Raul Perez'

# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):
    """
    Clase para el juego de Othello donde la representacion
    del estado es el siguiente:

        0   1   2   3   4   5   6   7
        8   9   10  11  12  13  14  15
        16  17  18  19  20  21  22  23
        24  25  26  27  28  29  30  31
        32  33  34  35  36  37  38  39
        40  41  42  43  44  45  46  47
        48  49  50  51  52  53  54  55
        56  57  58  59  60  61  62  63

    """

    def __init__(self):
        """
        Inicializa el Othello con el siguiente estado

            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0  -1   1   0   0   0
            0   0   0   1  -1   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0

        """
        # estado inicial
        x = [0 for _ in range(64)]
        x[27] = x[36] = -1
        x[28] = x[35] = 1
        super().__init__(tuple(x))
        self.historial = deque()
        self.estados_anteriores = deque()

    def checa_ficha(self, ficha, iteracion, oponente):
        """
        Checa que esta en la posicion dada.
        Regresa: 0 si es cero o no hubo nada,
                    1 si es del oponente,
                    2 si es jugada legal
        """
        # si la ficha es del oponente, esta bien
        return (1 if ficha == oponente else
            0 if ficha == 0 else
            2 if iteracion > 1 else
            0)

    def obtener_volteos(self, posicion):
        """
        Compueba si la jugada es legal, verifica si alguna
        de los 8 formas de voltear fichas se puede.

        * Horizontales: izquiera, derecha
        * Veticales:    arriba, abajo
        * Diagonales:   arriba a la izquierda, arriba a la derecha,
                        abajo a la izquierda, abajo a la derecha

        """
        estado = self.x[:]
        # si donde se quiere poner una ficha hay algo
        # entonces la jugada no es legal
        if estado[posicion] != 0:
            return [False]*8
        
        fila, columna = posicion//8, posicion%8
        jugador, oponente = self.jugador, -1 * self.jugador
        volteos = [False] * 8
        # Horizontal izquierda
        if columna > 1:
            for i in range(1, columna+1):
                resultado = self.checa_ficha(estado[posicion-i], i, oponente) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[0] = True
                    break
                else:
                    break
        # Horizontal derecha
        if columna < 6:
            for i in range(1, 8-columna):
                resultado = self.checa_ficha(estado[posicion+i], i, oponente)
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[1] = True
                    break
                else:
                    break
        # vertical arriba
        if fila > 1:
            for i in range(1, fila+1):
                resultado = self.checa_ficha(estado[posicion-i*8], i, oponente)
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[2] = True
                    break
                else:
                    break
        # vertical abajo
        if fila < 6:
            for i in range(1, 8-fila):
                resultado = self.checa_ficha(estado[posicion+i*8], i, oponente) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[3] = True
                    break
                else:
                    break
        # diagonal arriba a la izquierda
        if columna > 1 and fila > 1:
            for i in range(1, min((columna, fila))+1):
                resultado = self.checa_ficha(estado[posicion-i*9], i, oponente) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[4] = True
                    break
                else:
                    break
        # diagonal arriba a la derecha
        if columna < 6 and fila > 1:
            for i in range(1, min(abs(columna-7), fila)+1):
                resultado = self.checa_ficha(estado[posicion-i*7], i, oponente)
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[5] = True
                    break
                else:
                    break
        # diagonal abajo a la izquierda
        if columna > 1 and fila < 6:
            for i in range(1, min(columna, abs(fila-7))+1):
                resultado = self.checa_ficha(estado[posicion+i*7], i, oponente) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[6] = True
                    break
                else:
                    break
        # diagonal abajo a la derecha
        if columna < 6 and fila < 6:
            for i in range(1, min(abs(columna-7), abs(fila-7))+1):
                resultado = self.checa_ficha(estado[posicion+i*9], i, oponente) 
                if resultado == 1:
                    continue
                elif resultado == 2:
                    volteos[7] = True
                    break
                else:
                    break

        return volteos

    def obtener_area_de_jugadas(self):
        """
        Devuelve una tupla con las posibles posiciones
        donde se puede colocar una ficha.
        """
        estado = self.x[:]
        area_de_jugadas = set()
        for i in range(64):
            # si hay una ficha, revisa alrededor
            if estado[i] != 0:
                fila, columna = i//8, i%8
                if columna > 0:
                    # agrega el area de la iquierda
                    area_de_jugadas.add(i-1)
                    if fila > 0:
                        # agrega el area arriba a la izquierda
                        area_de_jugadas.add(i-9)
                    if fila < 7:
                        # agrega el area abajo a la izquierda
                        area_de_jugadas.add(i+7)
                if columna < 7:
                    # agrega el area a la derecha
                    area_de_jugadas.add(i+1)
                    if fila > 0:
                        # agrega el area arriba a la derecha
                        area_de_jugadas.add(i-7)
                    if fila < 7:
                        # agrega el area abajo a la derecha
                        area_de_jugadas.add(i+9)
                if fila > 0:
                    # agrega el area de arriba
                    area_de_jugadas.add(i-8)
                if fila < 7:
                    # agrega el area de abajo
                    area_de_jugadas.add(i+8)
                # revisa si en la posiciones hay ficha, si hay ficha entonces se elimina
                for lugar in tuple(area_de_jugadas):
                    if estado[lugar] != 0:
                        area_de_jugadas.remove(lugar)

        return tuple(area_de_jugadas)
        
    def jugadas_legales(self):  
        """
        Las jugadas legales son las posiciones donde se puede
        colocar una ficha y se volteen las fichas del oponente.
        """
        jugadas_permitidas = []

        for posicion in self.obtener_area_de_jugadas():
            # si es jugada legal se agrega a la lista
            if True in self.obtener_volteos(posicion):
                jugadas_permitidas.append(posicion)
        
        return tuple(jugadas_permitidas)

    def terminal(self):
        """
        Revisa si hay jugadas legales para ambos jugadores
        """
        # si no hay jugadas legales para el jugador 1
        if len(self.jugadas_legales()) == 0:
            self.jugador *= -1
            # si no hay jugadas legales para el jugador -1    
            if len(self.jugadas_legales()) == 0:
                self.jugador *= -1
                negras, blancas = self.x.count(1), self.x.count(-1) 
                return ( 1 if negras > blancas else
                        -1 if blancas > negras else
                         0)
            self.jugador *= -1
            
        return None

    def hacer_jugada(self, jugada):
        """
        Actualiza el estado del juego, dependiendo de la jugada
        """
        # si el jugador paso de turno
        if jugada is None:
            self.historial.append(jugada)
            self.jugador *= -1
            return None
        # guardamos los estados actuales y la jugada
        self.historial.append(jugada)
        self.estados_anteriores.append(self.x[:])
        # Proceso para voltear las fichas del oponente 
        jugador, oponente = self.jugador, -1*self.jugador
        fila, columna = jugada//8, jugada%8
        estado = list(self.x[:])
        # coloca la ficha del jugador en la jugada
        estado[jugada] = jugador
        # checa si hay posibilidades de voltear
        # izquierda, derecha, arriba, abajo, arriba izquierda
        # arriba derecha, abajo izquierda, abajo derecha
        volteos = self.obtener_volteos(jugada)
        for volteo, df in zip(volteos, (-1, 1, -8, 8, -9, -7, 7, 9)):
            if volteo:
                # volteo las fichas del oponente
                for i in range(1, 8):
                    if estado[jugada+i*df] == oponente:
                        estado[jugada+i*df] = jugador
                    else:
                        break
        # hacemos los cambios
        self.x = tuple(estado[:])
        self.jugador = oponente
 
    def deshacer_jugada(self):
        """
        Cambia el estado actual al estado anterior, al igual
        que el area de jugadas
        """
        jugada = self.historial.pop()
        if jugada is not None:   
            self.x = self.estados_anteriores.pop()
        self.jugador *= -1

def utilidad(x):
    return x.count(1) + x.count(-1)

def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    shuffle(jugadas)
    return jugadas

def pintar_othello(juego):
    x = juego.x[:]
    area = juego.obtener_area_de_jugadas()

    y = [('X' if x[i] == 1 else 'O' if x[i] == -1 else str(i)) for i in range(64)]

    print("\n\n")
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
    print("\n\n")

    for lugar in area:
        if True in juego.obtener_volteos(lugar):
            y[lugar] = 'SI'
        else:
            y[lugar] = 'NO'
    
    print("\n\n")
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
    print("\n\n")


class OthelloTK:
    def __init__(self, escala=2):
        self.app = app = tk.Tk()
        self.app.title("Othello")
        self.L = L = int(escala) * 30

        tmpstr = "Escoge, X siempre empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=8 * L)
        self.anuncio.pack()
        
        barra = tk.Frame(app)
        barra.pack()
        
        self.userpoints = tk.Label(barra, bg='light grey', text="X: ")
        self.userpoints.grid(column=0, row=0)
       
        botonX = tk.Button(barra,
                           command=lambda x=1: self.jugar(x),
                           text='(re)Iniciar con X')

        botonX.grid(column=1, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=-1: self.jugar(x),
                           text='(re)Iniciar con O')

        botonO.grid(column=2, row=0)
        self.Mpoints = tk.Label(barra, bg='light grey',  text="O: ")
        self.Mpoints.grid(column=3, row=0)
        
        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.4 * L), 'bold')
        for i in range(64):
            self.tablero[i] = tk.Canvas(ctn, height=L, width=L, bg='light grey', borderwidth=0)
            self.tablero[i].grid(row=i//8, column=i%8)
            self.textos[i] = self.tablero[i].create_text( L//2, L//2, font=letra, text=' ')
            self.tablero[i].val = 0
            self.tablero[i].pos = i

    def actualizar_puntaje(self, x, primero):
        self.userpoints['text'] = "YO: {} ".format(x.count(primero))
        self.userpoints.update()
        self.Mpoints['text'] = "M: {} ".format(x.count(-1*primero))
        self.Mpoints.update()

    def jugar(self, primero):
        juego = Othello()

        self.anuncio['text'] = "Turno del jugador {}".format('X' if juego.jugador == 1 else 'O')
        
        while juego.terminal() is None:
            self.actualiza_tablero(juego.x)
            pintar_othello(juego)
            if len(juego.jugadas_legales()) > 0:
                jugada = (self.escoge_jugada(juego) if juego.jugador == primero else 
                    minimax_t(juego, 10, utilidad, ordena_jugadas))
                
            else:
                jugada = None
        
            juego.hacer_jugada(jugada)
            self.actualizar_puntaje(juego.x, primero)
            self.anuncio['text'] = "Turno del jugador {}".format('X' if juego.jugador == 1 else 'O')
                
        self.actualiza_tablero(juego.x)
        resultado = juego.terminal()
        fin = ["Empate lo que falta...",
               "¡Gané! ¡Juar, juar, juar!, ¿Quieres perder otra vez?",
               "Ganaste (Me deje ganar)" ]
        
        print("\n\nFin del juego")
        self.anuncio['text'] = (fin[0] if resultado == 0 else
                                fin[1] if (primero == -1 and resultado>0) or (primero == 1 and resultado<0) else
                                fin[2])
        self.anuncio.update()

    def escoge_jugada(self, juego):
        jugadas_posibles = juego.jugadas_legales()
        
        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')
        
        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'green'

        def salida(evento):
            evento.widget['bg'] = 'light grey'

        def presiona_raton(evento):
            evento.widget['bg'] = evento.widget.color_original
            seleccion.set(evento.widget.pos)

        for jugada in jugadas_posibles:
            self.tablero[jugada].bind('<Enter>', entrada)
            self.tablero[jugada].bind('<Leave>', salida)
            self.tablero[jugada].bind('<Button-1>', presiona_raton)

        self.tablero[0].master.wait_variable('seleccion')

        for jugada in jugadas_posibles:
            self.tablero[jugada].unbind('<Enter>')
            self.tablero[jugada].unbind('<Leave>')
            self.tablero[jugada].unbind('<Button-1>')

        return seleccion.get()

    def actualiza_tablero(self, x):
        for i in range(64):
            if self.tablero[i].val != x[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text=' xo'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()

if __name__ == '__main__':
    OthelloTK().arranca()
    
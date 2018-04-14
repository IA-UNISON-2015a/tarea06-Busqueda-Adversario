#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustedes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
from busquedas_adversarios import minimax_t
from random import shuffle
from collections import deque
import tkinter as tk

__author__ = 'luis fernando'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):

    """
    Inicializa el juego, esto es: el número de columnas y
    renglones y el estado inicial del juego. Cuyas posiciones
    estan dadas como:
    8x8

     0   1   2   3   4   5   6   7
     8   9  10  11  12  13  14  15
    16  17  18  19  20  21  22  23
    24  25  26  27  28  29  30  31
    32  33  34  35  36  37  38  39
    40  41  42  43  44  45  46  47
    48  49  50  51  52  53  54  55
    56  57  58  59  60  61  62  63
    """
    def __init__(self):
        board = [0 for _ in range(8 * 8)]
        board[27] = 1
        board[36] = 1

        board[28] = -1
        board[35] = -1

        super().__init__(tuple(board))
        self.historial = deque()

    """
    Una jugada legal es un indice del tablero (vacio) donde el jugador de
    turno puede poner una ficha.
    """
    def jugadas_legales(self):
        return (i + 8*j for i in range(8) for j in range(8)
                if self.x[i + 8*j] == 0 and self.jugada_legal((i,j)))

    """
    Una jugada legal es un indice del tablero (vacio) donde el jugador de
    turno puede poner una ficha.

    @param pos: Tupla (x,y) indicando el lugar en el tablero
    """
    def jugada_legal(self, pos):
        direcciones = ((-1,-1), (0,-1), (1,-1),
                       (-1,0),          (1,0),
                       (-1,1),  (0,1),  (1,1))


        for direccion in direcciones:
            if any(self.fichas_seguidas(pos, direccion) for direccion in direcciones):
                return True

        return False

    """
    Si poner una ficha en la tupla indicada por pos es legal, esto regresa todas
    un diccionario con todas las direcciones que hacen a la posicion legal.

    @param pos: Tupla (x,y) indicando el lugar en el tablero

    @return Diccionario con llaves la direccion en donde poner la ficha voltearia
            fichas del oponente y valores una tupla de direcciones.
    """
    def voltea_dir(self, pos):
        direcciones = ((-1,-1), (0,-1), (1,-1),
                       (-1,0),          (1,0),
                       (-1,1),  (0,1),  (1,1))

        return [direccion for direccion in direcciones if self.fichas_seguidas(pos, direccion)]

    """
    Recibe una tupla de la forma (x,y), indicando una posicion en el tablero
    """
    def dentro_tablero(self, pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    """
    Revisa si desde la posicion recibida, hay fichas del que no es turno en
    la direccion recibida y que terminan en una ficha del jugador de turno.

    @param pos: Posicion en el tablero. Tupla que indica la posicion
    @param direccion: Tupla que indica una direccion
    """
    def fichas_seguidas(self, pos, direccion):
        aux = pos[0] + direccion[0], pos[1] + direccion[1]

        if self.dentro_tablero(aux) and self.x[aux[0] + 8*aux[1]] == self.jugador*-1:
            aux = aux[0] + direccion[0], aux[1] + direccion[1]

            while self.dentro_tablero(aux) and self.x[aux[0] + 8*aux[1]] != 0:
                if self.x[aux[0] + 8*aux[1]] == self.jugador:
                    return True

                aux = aux[0] + direccion[0], aux[1] + direccion[1]

        return False

    """
    Devuelve None si no es terminal el estado actual,
    en otro caso devuelve la ganancia para el jugador 1.
    """
    def terminal(self):
        jugadas = list(self.jugadas_legales())
        if not jugadas:
            self.jugador *= -1
            jugadas = list(self.jugadas_legales())
            if jugadas:
                self.jugador *= -1
            else:
                negras = self.x.count(1)
                blancas = self.x.count(-1)
                return 1 if negras > blancas else -1 if blancas > negras else 0

        return None

    """
    Realiza la jugada, modifica el estado. La jugada es que el jugador de turno ponga
    una ficha en el indice indicado por la variable jugada y se voltean todas las fichas
    correspondientes del contrincante.
    """
    def hacer_jugada(self, jugada):
        self.historial.append(self.x[:]) #guarda todo el estado
        self.x[jugada] = self.jugador

        direcciones = self.voltea_dir((jugada%8, int(jugada/8)))


        for direccion in direcciones:
            dir_lineal = direccion[0] + 8*direccion[1]
            aux = jugada + dir_lineal

            while self.x[aux] != self.jugador:
                self.x[aux] = self.jugador
                aux += dir_lineal

        self.jugador *= -1

    """
    Deshace la ultima jugada hecha.
    """
    def deshacer_jugada(self):
        self.x = self.historial.pop()
        self.jugador *= -1

"""
Ordena las jugadas legales.
Unicamente pone primero las jugadas de las esquinas y
pone al final las jugadas en las casi esquinas.
Si no hay en ninguno, es el mismo que el orden de generacion
de jugadas.
"""
def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    esquinas = {0, 7, 56, 63}
    casi_esquinas = {9, 14, 49, 54}

    return sorted(jugadas,
                  key=lambda x: 1 if x in esquinas else -1 if x in casi_esquinas else 0,
                  reverse=True)

"""
Implementacion copiada de belen y ligeramente cambiada.
"""
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

        self.userpoints = tk.Label(barra, bg='light grey', text="J1: ")
        self.userpoints.grid(column=0, row=0)

        botonX = tk.Button(barra,
                           command=lambda x=1: self.jugar(x),
                           text='(re)iniciar con X')
        botonX.grid(column=1, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=-1: self.jugar(x),
                           text='(re)iniciar con O')
        botonO.grid(column=2, row=0)
        self.Mpoints = tk.Label(barra, bg='light grey',  text="J2: ")
        self.Mpoints.grid(column=3, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.4 * L), 'bold')
        for i in range(64):
            self.tablero[i] = tk.Canvas(ctn, height=L, width=L,
                                        bg='light grey', borderwidth=0)
            self.tablero[i].grid(row=i // 8, column=i % 8)
            self.textos[i] = self.tablero[i].create_text(L // 2, L // 2,
                                                         font= letra, text=' ')
            self.tablero[i].val = 0
            self.tablero[i].pos = i

    def jugar(self, primero):

        juego = Othello()

        #funciones de utilidad definidas aqui porque necesitan conocer el juego
        """
        El numero de jugadas que un jugador puede hacer entre el
        numero de casillas vacias que quedan.
        """
        def movilidad_inmediata(x):
            return len(list(juego.jugadas_legales())) / juego.x.count(0)

        """
        Recompensa poner las fichas en las esquinas y penaliza poner en
        lugares que podrian dar las esquinas que no esten tomadas.
        """
        def contar_esquinas(x):
            esquinas = [0, 7, 56, 63]
            esquina_j1 =  sum(1 for esquina in esquinas if x[esquina] == juego.jugador)
            esquina_j2 =  sum(-1 for esquina in esquinas if x[esquina] == -juego.jugador)

            casi_esquinas = [9, 14, 49, 54]
            casi_esquina_j1 = sum(1 for casi_esquina, esquina in zip(casi_esquinas, esquinas)
                                  if x[casi_esquina] == juego.jugador and
                                  x[esquina] == 0)
            casi_esquina_j2 = sum(1 for casi_esquina, esquina in zip(casi_esquinas, esquinas)
                                  if x[casi_esquina] == -juego.jugador and
                                  x[esquina] == 0)

            return (esquina_j1 + casi_esquina_j2 - esquina_j2 - casi_esquina_j1) / 8

        """
        Cuenta la diferencia de piezas en el tablero de los jugadores.
        Como solamente importa el numero de piezas al final, solo cuenta cuando
        quedan 10 o menos turnos.
        """
        def contar_piezas(x):
            if x.count(0) > 10:
                return 0

            return (x.count(juego.jugador) - x.count(-juego.jugador)) / 64

        """
        Toma en cuentas las esquinas, la movilidad inmediata y el numero de piezas
        cuando el juego esta por acabar
        """
        def utilidad(x):
            return 0.6*contar_esquinas(x) + 0.3*contar_piezas(x) + 0.1*movilidad_inmediata(x)

        self.anuncio['text'] = "Turno jugador {}".format(1 if juego.jugador == 1 else 2)

        while juego.terminal() is None:
            self.actualiza_tablero(juego.x)
            if list(juego.jugadas_legales()):

                if juego.jugador == primero:
                    jugada = self.escoge_jugada_humano(juego)
                    #jugada = minimax_t(juego, 30, utilidad, ordena_jugadas, {})
                else:
                    #jugada = self.escoge_jugada_humano(juego)
                    jugada = minimax_t(juego, 30, utilidad, ordena_jugadas, {})

                juego.hacer_jugada(jugada)

                self.actualizar_puntos(juego, primero)

            else:
                print("No hay jugadas para ti...")
                juego.jugador = -1*juego.jugador

            self.anuncio['text'] = "Turno jugador {}".format(1 if juego.jugador == 1 else 2)

        self.actualiza_tablero(juego.x)
        u = juego.terminal() #regresa la utilidad del jugador 1
        if u == 0:
            fin = "UN ASQUEROSO EMPATE"
        elif (primero<0 and u>0) or (primero>0 and u<0):
            fin ="¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?"
        else:
            fin ="Ganaste, bye."

        print("\n\nFin del juego")
        self.anuncio['text'] = fin
        self.anuncio.update()

    def escoge_jugada_humano(self, juego):
        jugadas_posibles = list(juego.jugadas_legales())
        if len(jugadas_posibles) == 1:
            return jugadas_posibles[0]

        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')

        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'blue'

        def salida(evento):
            evento.widget['bg'] = evento.widget.color_original

        def presiona_raton(evento):
            evento.widget['bg'] = evento.widget.color_original
            seleccion.set(evento.widget.pos)

        for i in jugadas_posibles:
            self.tablero[i].bind('<Enter>', entrada)
            self.tablero[i].bind('<Leave>', salida)
            self.tablero[i].bind('<Button-1>', presiona_raton)

        self.tablero[0].master.wait_variable('seleccion')

        for i in jugadas_posibles:
            self.tablero[i].unbind('<Enter>')
            self.tablero[i].unbind('<Leave>')
            self.tablero[i].unbind('<Button-1>')
        return seleccion.get()


    """
    Actualiza los puntos del tablero
    """
    def actualizar_puntos(self, juego, primero):
        self.userpoints['text'] = "J1: {} ".format(juego.x.count(primero))
        self.userpoints.update()
        self.Mpoints['text'] = "J2: {} ".format(juego.x.count(-primero))
        self.Mpoints.update()


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


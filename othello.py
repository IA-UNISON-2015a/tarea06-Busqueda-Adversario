#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------


El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk

__author__ = 'Patricia Quiroz'

"""
	Inicializa el juego, esto es: el número de columnas y
	renglones y el estado inicial del juego. Cuyas posiciones
	estan dadas como:

    56  57  58  59  60  61  62  63		
    48  49  50  51  52  53  54  55
    40  41  42  43  44  45  46  47
    32  33  34  35  36  37  38  39
    24  25  26  27  28  29  30  31
    16  17  18  19  20  21  22  23
    8   9   10  11  12  13  14  15
    0   1   2   3   4   5   6   7

"""
class Othello(JuegoSumaCeros2T):
  
    def __init__(self):
    	x=[]
		for i in range(8*8):
			if i==35 or i==28 :
  				x.append(1)
			elif i== 36 or i==27:
  				x.append(-1)
			else:
  				x.append(0)
  		"""
 		0	0	0	 0	 0	 0	 0	 0
		0	0	0	 0	 0	 0	 0	 0
		0	0	0	 0	 0	 0	 0	 0
		0	0	0	 1	-1	 0	 0	 0
		0	0	0	-1	 1	 0	 0	 0
		0	0	0	 0	 0	 0	 0	 0
		0	0	0	 0	 0	 0	 0	 0
		0	0	0	 0	 0	 0	 0	 0
  		"""
        super().__init__(tuple(x),-1)

    def validar_posicion(posicion):
    	"""
    	NOTA: TODAVIA LE FALTA PERO AHI VA LA IDEA
    	
        Método para validar si es posible usar la posicion para poner una ficha y asi realizar una jugada.
        @return: una lista con las direcciones en las cuales puede realizar un movimiento.
        """
        mov=[]
        #Revisar si la casilla no esta ocupada
        #Revisar posibles direcciones al colocar la ficha 
        aux=[1,6,7,8,-1,-6,-7,-8] #8 formas de moverte respecto a la posicion
        #Se empieza a mover por las direcciones
        for i in aux:
        	#nos movemos en la direccion tomando en cuenta nuesta posicion actual(indice)
        	aux2+=posicion+aux
        	while(still_in_tablero(self.x[aux2])): #mientras no se salga del tablero
        		aux2+=posicion+aux #Nos seguimos moviendo en la direccion
		    	#se va checando si en la direccion en que se camina existen fichas contrarias
		    	if self.x[aux2]!= 1 or self.x[aux2] == self.jugador: 
		    		break #no existen al menos una ficha contraria que voltear
		    	#si llega a un espacio
		    	if self.x[aux2] == 0:
		    		mov.append(i) #se agrega la direccion a la lista
       	return mov

    def jugadas_legales(self):
    	return None
    	"""
        Las jugadas legales son las posiciones donde se puede colocar una ficha 
        del propio color en una casilla vacía. Entre la ficha recién colocada y otra
		del mismo color (previamente en el tablero) debe haber fichas del color contrario en la misma
		línea (ya sea en dirección diagonal, horizontal o vertical).

		@return: una lista de jugadas que se pueden realizar
		"""
        jugadas_legales = []
        for i in range(64):
           direcciones = self.validar_posicion(i)
           jugadas_legales.append( ((reng,col), direcciones) ) 
        return jugadas_legales


    def terminal(self):
        """
		La partida acaba cuando nadie puede mover (normalmente cuando el tablero está lleno o casi
		lleno) y gana quien en ese momento tenga más fichas sobre el tablero.
		****Existe un caso especial donde se le terminan las fichas a un jugador.****

		@return: quien gano
        """
        f_negras = self.x.count(-1) #se obtiene el numero de fichas negras en el tablero
        f_blancas = self.x.count(1) #se obtiene el numero de fichas blancas en el tablero
        if 0 not in x:
            return 0

        if f_blancas>f_negras:
        	ganador=1
        elif f_negras > f_blancas:
        	ganador=-1
        else: #EMPATE
        	ganador=0

        return ganador

    def hacer_jugada(self, jugada):
    	#MODIFICAR, FALTAN DETALLES DE OTHELLO
    	"""
    	Metodo para hacer una jugada, recibe una jugada previamente validada por jugadas_legales.

    	Voltear las fichas del color contrario que quedan entre la ficha recién colocada y cualquier
		otra del mismo color ya colocada. De esta forma, cambian de color.
       	"""

    	#Me muevo a traves del tablero 
   		#Si existe una ficha de color y de manera tanto vertical, diagonal y horizontal existe
   		#una o mas fichas de mi oponente, entonces, pongo una de mis fichas
   		#¿como checar si existen una serie fichas del oponente?
   		#primero checamos si existe ficha de oponente de manera horizontal
	   for i in range(0, 41, 7):
    	if self.x[i + jugada] == 0:
        self.x[i + jugada] = self.jugador
        self.historial.append(jugada) #Se guarda la jugada en el historial
        self.jugador *= -1#Cambio mis ficha"""
        return None

    def deshacer_jugada(self):
    	#MODIFICAR, FALTAN DETALLES DE OTHELLO
        pos = self.historial.pop() #Saco la ultima jugada realizada
    	for i in range(64): #Me muevo a traves del tablero
            if self.x[i + pos] != 0: #Si la casilla esta ocupada
                self.x[i + pos] = 0 #Cambiamos la posicion a estar disponible de nuevo
                self.jugador *= -1 #Cambio mi ficha
                return None

def utilidad_othello(x):

def movimiento_valido(reng,col): #SE VA A ESTAR MOVIENDO POR EL TABLERO
	"""
	este método dice si una casilla es válida para poner una pieza en ella.
	@param reng: renglon de la casilla
    @param col: columna de la casilla 
    @return: una lista con las direcciones en las cuales puede voltear piezas, vacía si es un movimiento incorrecto """
    
    #lista de posibles direcciones donde se colocara la pieza 
    direcciones=[]

    for i in 

def ordena_jugadas(juego):
    """
    Ordena las jugadas de acuerdo al jugador actual, en función
    de las más prometedoras.
    """
    jugadas = list(juego.jugadas_legales())
    shuffle(jugadas)
    return jugadas	

def pprint_gato(x):
	y = [('X' if x[i] > 0 else 'O' if x[i] < 0 else str(i)) for i in range(64)]
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[8], y[9], y[10], y[11], y[12], y[13], y[14], y[15]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[16], y[17], y[18], y[19], y[20], y[21], y[22], y[23]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[24], y[25], y[26], y[27], y[28], y[29], y[30], y[31]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[32], y[33], y[34], y[35], y[36], y[37], y[38], y[39]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[40], y[41], y[42], y[43], y[44], y[45], y[46], y[47]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[48], y[49], y[50], y[51], y[52], y[53], y[54], y[55]).center(60))
	print("---+---+---".center(60))
	print(" {} | {} | {} | {} | {} | {} | {} | {} ".format(y[56], y[57], y[58], y[59], y[60], y[61], y[62], y[63]).center(60))

class OthelloTK:
    def __init__(self, escala=2):

        self.app = app = tk.Tk()
        self.app.title("Othello")
        self.L = L = int(escala) * 25

        tmpstr = "Escoge, X siempre empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=3 * L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonX = tk.Button(barra,
                           command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con X')
        botonX.grid(column=0, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con O')
        botonO.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.9 * L), 'bold')
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

        if not primero:
            jugada = minimax(juego)
            juego.hacer_jugada(jugada)

        self.anuncio['text'] = "A ver de que cuero salen más correas"
        for _ in range(64):
            self.actualiza_tablero(juego.x)
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            ganador = juego.terminal()
            if ganador is not None:
                break
            jugada = minimax(juego)
            juego.hacer_jugada(jugada)
            ganador = juego.terminal()
            if ganador is not None:
                break

        self.actualiza_tablero(juego.x)
        finstr = ("UN ASQUEROSO EMPATE, aggggg" if ganador == 0 else
                  "Ganaste, bye"
                  if (ganador > 0 and primero) or (ganador < 0 and not primero)
                  else "¡Gané¡  Juar, juar, juar.")
        self.anuncio['text'] = finstr
        self.anuncio.update()

    def escoge_jugada(self, juego):
        jugadas_posibles = list(juego.jugadas_legales())
        if len(jugadas_posibles) == 1:
            return jugadas_posibles[0]

        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')

        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'grey'

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
    # juega_gato('X')
    OthelloTK().arranca()

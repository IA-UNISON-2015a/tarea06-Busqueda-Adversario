#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
import tkinter as tk
from random import shuffle
from collections import deque

__author__ = 'Cesar Salazar'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(JuegoSumaCeros2T):
    """
    Estado inicial del tablero:
        0   0   0   0   0   0   0   0 
        0   0   0   0   0   0   0   0
        0   0   0   0   0   0   0   0
        0   0   0   -1  1   0   0   0
        0   0   0   1  -1   0   0   0
        0   0   0   0   0   0   0   0
        0   0   0   0   0   0   0   0
        0   0   0   0   0   0   0   0
    Las posiciones del tablero son :
        0   1   2   3   4   5   6   7
        8   9   10  11  12  13  14  15
        16  17  18  19  20  21  22  23
        24  25  26  27  28  29  30  31
        32  33  34  35  36  37  38  39
        40  41  42  43  44  45  46  47
        48  49  50  51  52  53  54  55
        56  57  58  59  60  61  62  63
    Las posiciones del centro son las iniciales: 27, 28, 35, 36
    """
    def __init__(self):
        x = [0 for _ in range(64)]
        x[27] = x[36] =-1
        x[28] = x[35] =1
        x=[1,-1,0,-1,-1,-1,-1,1,1,1,1,-1,-1,1,1,1,1,1,1,-1,-1,-1,1,1,1,1,1,-1,-1,-1,-1,-1,1,-1,1,1,1,1,1,-1,1,1,1,1,1,1,-1,-1,-1,0,1,1,1,-1,-1,-1,1,1,1,1,0,-1,-1,-1]
        super().__init__(tuple(x))
        self.historial = deque()
        self.x_anterior = deque()
        #son las casillas que se descartan en las jugadas legales para cada direccion
        self.derecha=[6,7,14,15,22,23,30,31,38,39,46,47,53,55,62,63]
        self.izquierda=[0,1,8,9,16,17,24,25,32,33,40,41,48,49,56,57]
        self.abajo=[i for i in range(48,64)]
        self.arriba=[i for i in range(0,16)]
        #para las diagonales combino las listas dependiendo de que ocupe
        self.dDAbajo=combinarListas(self.derecha,self.abajo)
        self.dIAbajo=combinarListas(self.izquierda,self.abajo)
        self.dDArriba=combinarListas(self.derecha,self.arriba)
        self.dIArriba=combinarListas(self.izquierda,self.arriba)
    #pintar en consola el tablero
    def imprimirTablero(self):
        """
        nomas pa la lista en forma de tablero 
        """
        #tablero=np.reshape(self.x.copy(),(8,8))
        #print(tablero)
        tablero = "┌───┬───┬───┬───┬───┬───┬───┬───┐\n"
        for renglon in range(8):
            for col in range(8):
                tablero += "│"
                tablero += " o " if self.x[ 8*renglon + col ] == 1 else " * " if self.x[8*renglon + col] == -1 else "   "
            tablero += "│\n"
            tablero += "├───┼───┼───┼───┼───┼───┼───┼───┤\n" if renglon < 7 else "└───┴───┴───┴───┴───┴───┴───┴───┘\n"
        
        blancas,negras = self.x.count(-1),self.x.count(1)

        tablero += "*: " + str(blancas) + "\n"
        tablero += "o: " + str(negras) + "\n"

        print(tablero)
    #funcion para ver si se puede poner en esa casilla
    def esValida(self,casilla):
        #se modifico para que regresara en que direcciones podria voltear para usar en "hacer_jugada"
        jugador=self.jugador
        rival=jugador*-1
        fila=casilla//8
        finalFila=8*fila+7
        inicioFila=8*fila
        columna = casilla%8
        arriba,abajo,derecha,izquierda,dIAbajo,dIArriba,dDArriba,dDAbajo=False,False,False,False,False,False,False,False
        #Horizontal
        #hacia la derecha
        #si tiene casilla del rival a la derecha
        if casilla not in self.derecha: 
            if self.x[casilla+1] == rival:
                for i in range(casilla+2, finalFila+1):
                    #si encuenta un -1 es valido hacer el movimiento
                    if self.x[i]==jugador: 
                        derecha= True
                        break 
                    elif self.x[i]==0: 
                        derecha= False
                        break 
        #hacia la izquierda
        #si tiene casilla del rival a la izquierda
        if casilla not in self.izquierda: 
            if self.x[casilla-1] == rival:
                for i in range(2,columna+1):
                    if self.x[casilla-i]==jugador: 
                        izquierda= True
                        break 
                    elif self.x[casilla-i]==0: 
                        izquierda= False
                        break
        #Vertical
        #hacia abajo
        #si tiene casilla del rival abajo
        if casilla not in self.abajo: 
            if self.x[casilla+8] == rival:
                for i in range(2,8-fila):
                    if self.x[casilla+i*8]==jugador: 
                        abajo= True
                        break 
                    elif self.x[casilla+i*8]==0: 
                        abajo= False
                        break
        #hacia arriba
        #si tiene casilla del rival abajo
        if casilla not in self.arriba: 
            if self.x[casilla-8] == rival:
                for i in range(2,8+fila):
                    if self.x[casilla-i*8]==jugador: 
                        arriba= True
                        break 
                    elif self.x[casilla-i*8]==0: 
                        arriba= False
                        break
        #diagonales
        #diagonal hacia abajo-derecha
        if casilla not in self.dDAbajo: 
            if self.x[casilla+8+1] == rival:
                for i in range(1,8-fila-1):
                    if self.x[casilla+(8*i)+i]==jugador: 
                        dDAbajo= True 
                        break
                    elif self.x[casilla+(8*i)+i]==0 or (casilla+(8*i)+i)%8==0: 
                        dDAbajo= False
                        break
        #diagonal hacia abajo-izquierda
        if casilla not in self.dIAbajo: 
            if self.x[casilla+8-1] == rival:
                for i in range(2,8-fila):
                    if self.x[casilla+(8*i)-i]==jugador: 
                        dIAbajo= True
                        break 
                    elif self.x[casilla+(8*i)-i]==0 or (casilla+(8*i)-i)%8==0: 
                        dIAbajo= False
                        break
        #diagonal hacia arriba-derecha
        if casilla not in self.dDArriba: 
            if self.x[casilla-8+1] == rival:
                for i in range(2,fila):
                    if self.x[casilla-(8*i)+i]==jugador: 
                        dDArriba =True 
                        break
                    elif self.x[casilla-(8*i)+i]==0 or (casilla-(8*i)+i)%8==7: 
                        dDArriba= False
                        break
        #diagonal hacia arriba-izquierd
        if casilla not in self.dIArriba: 
            if self.x[casilla-8-1] == rival:
                for i in range(2,fila):
                    if self.x[casilla-(8*i)-i]==jugador: 
                        dIArriba= True 
                        break
                    elif self.x[casilla-(8*i)-i]==0 or (casilla-(8*i)-i)%8==0: 
                        dIArriba= False
                        break
        puedeVoltear=[dDAbajo,abajo,dIAbajo,derecha,izquierda,dDArriba,arriba,dIArriba]  
        return puedeVoltear
    def jugadas_legales(self):
        legales=[]
        for casilla in range(64):
            if self.x[casilla]==0:
                if True in self.esValida(casilla): legales.append(casilla)
        #print("\n\nJUGADAS LEGALES PARA :",self.jugador," :",legales,"\n\n")            
        return tuple(legales)
    def terminal(self):
        asteriscos = self.x.count(-1)
        os = self.x.count(1)
        jugadas1=len(self.jugadas_legales())
        self.jugador*=-1
        jugadas2=len(self.jugadas_legales())
        self.jugador*=-1
        if asteriscos == 0 or os == 0:
            return 1 if asteriscos < os else -1

        #si ningun jugador tiene movimientos
        if jugadas1==0 and jugadas2==0:
            return 1 if os > asteriscos else -1 if asteriscos > os else 0

        return None

    def hacer_jugada(self, jugada):
        """self.x_anterior.append(self.x[:])
        jugador, rival = self.jugador, -1*self.jugador
        #guarda quein es cada quien
        #obtener la fila y columna
        #si el jugador paso turno por no tener jugada disp
        if jugada is None:
            print("la jugada es none")
            self.historial.append(jugada)
            self.jugador *= -1
            return None
        fila=jugada//8 
        columna = jugada%8
        estado = list(self.x[:])
        #pone ficha
        self.historial.append(jugada)
        estado[jugada]=jugador"""
        # si el jugador paso de turno
        if jugada is None:
            self.historial.append(jugada)
            self.jugador *= -1
            return None
        # guardamos los estados actuales y la jugada
        self.historial.append(jugada)
        self.x_anterior.append(self.x[:])
        # Proceso para voltear las fichas del oponente 
        jugador=self.jugador
        rival = -1*self.jugador
        fila, columna = jugada//8, jugada%8
        estado = list(self.x[:])
        # coloca la ficha del jugador en la jugada
        estado[jugada] = jugador
        #obtiene para donde volteara
        voltear=self.esValida(jugada)
        #VOLTEA LAS FICHAS
        #derecha
        if voltear[3] :
            for i in range(1,7-columna):
                if estado[jugada+i]==jugador: break
                estado[jugada+i]=jugador
        #izquierda
        if voltear[4] :
            for i in range(1,columna):
                if estado[jugada-i]==jugador: break
                estado[jugada-i]=jugador
        #abajo
        if voltear[1] :
            for i in range(1,7-fila-1):
                if estado[jugada+i*8]==jugador: break
                estado[jugada+i*8]=jugador
        #arriba
        if voltear[6] :
            for i in range(1,fila):
                if estado[jugada-i*8]==jugador: break
                estado[jugada-i*8]=jugador
        #d arriba der
        if voltear[5] :
            for i in range(1,fila):
                if estado[jugada-i*8+i]==jugador: break
                estado[jugada-i*8+i]=jugador
        #d arriba izq
        if voltear[7] :
            for i in range(1,fila):
                if estado[jugada-i*8-i]==jugador: break
                estado[jugada-i*8-i]=jugador
        #d abajo der
        if voltear[0] :
            for i in range(1,7-fila):
                if estado[jugada+i*8+i]==jugador: break
                estado[jugada+i*8+i]=jugador
        #d abajo izq
        if voltear[2] :
            for i in range(1,7-fila):
                if estado[jugada+i*8-i]==jugador: break
                estado[jugada+i*8-i]=jugador
        self.x=tuple(estado[:])
        self.jugador= rival

    def deshacer_jugada(self):
        casilla = self.historial.pop()
        if casilla is not None:   
            self.x = self.x_anterior.pop()
        self.jugador *= -1

def utilidad(x):
    #cuenta las esquinas ocupadas
    contador = 0
    for i in (0,7,56,63):
        if x[i] != 0:
            contador+=1  
    return contador

def ordena_jugadas(juego):
    jugadasOrdenadas=[]
    jugadas = list(juego.jugadas_legales())
    for jugada in (0,7,56,63):
        if jugada in jugadas: 
            jugadasOrdenadas.append(jugada)
            jugadas.remove(jugada)
    shuffle(jugadas)
    
    return combinarListas(jugadasOrdenadas,jugadas)
    
#para combinar las listas d eno posibles en la diagonal
def combinarListas(lista1,lista2):
    lista=lista1.copy()
    lista.extend([element for element in lista2 if element not in lista1])
    return lista

def puntos(x, jugador):
    cont=0
    for i in range(64):
        if x[i]==jugador:
            cont+=1
    return cont
class OthelloTK:
    def __init__(self, escala=2):

        self.app = app = tk.Tk()
        self.app.title("Otello")
        self.L = L = int(escala) * 30

        tmpstr = "Elige fichas, 'o' siempre empiezan"
        self.anuncio = tk.Message(app, bg='lightgreen', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=8 * L)
        self.anuncio.pack()
        
        

        barra = tk.Frame(app)
        barra.pack()
        
        self.userpoints = tk.Label(barra, bg='light grey', text="Persona: ")
        self.userpoints.grid(column=0, row=0)
       
        
        botonX = tk.Button(barra,fg="white",bg="black",
                           command=lambda x=1: self.jugar(x),
                           text='Iniciar con o')
        botonX.grid(column=1, row=0)
        botonO = tk.Button(barra,fg="white",bg="black",
                           command=lambda x=-1: self.jugar(x),
                           text='Iniciar con *')
        botonO.grid(column=2, row=0)
        self.Mpoints = tk.Label(barra, bg='light grey',  text="Agente: ")
        self.Mpoints.grid(column=3, row=0)
        

        ctn = tk.Frame(app, bg='gray')
        ctn.pack()
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Arial', -int(0.4 * L), 'bold')
        for i in range(64):
            self.tablero[i] = tk.Canvas(ctn, height=L, width=L,
                                        bg='#614646', borderwidth=0)
            self.tablero[i].grid(row=i // 8, column=i % 8)
            self.textos[i] = self.tablero[i].create_text(L // 2, L // 2,
                                                         font= letra, text=' ')
            self.tablero[i].val = 0
            self.tablero[i].pos = i

    def actualizar_puntaje(self, x, primero):
        self.userpoints['text'] = "Persona: {} ".format(x.count(primero))
        self.userpoints.update()
        self.Mpoints['text'] = "Agente: {} ".format(x.count(-1*primero))
        self.Mpoints.update()
    
    def jugar(self, primero):
        juego = Othello()

        self.anuncio['text'] = "Turno del jugador {} - Jugadas Legales: {}".format('o' if juego.jugador == 1 else '*',juego.jugadas_legales())
        
        while juego.terminal() is None:
            self.actualiza_tablero(juego.x)
            if len(juego.jugadas_legales()) >= 0:
                jugada = (self.escoge_jugada(juego) if juego.jugador == primero else 
                    minimax_t(juego, 10, utilidad, ordena_jugadas))
            else:
                jugada = None
        
            juego.hacer_jugada(jugada)
            self.actualizar_puntaje(juego.x, primero)
            self.anuncio['text'] = "Turno del jugador {} - Jugadas Legales: {}".format('o' if juego.jugador == 1 else '*',juego.jugadas_legales())
                
        self.actualiza_tablero(juego.x)
        resultado = juego.terminal()
        fin = ["Empate °_°",
               "Gané :v",
               "Ganaste -_-" ]
        
        print("\n\nFin del juego")
        self.anuncio['text'] = (fin[0] if resultado == 0 else
                                fin[1] if (primero == -1 and resultado>0) or (primero == 1 and resultado<0) else
                                fin[2])
        self.anuncio.update()
    
    def escoge_jugada(self, juego):
        jugadas_posibles = list(juego.jugadas_legales())
        if len(jugadas_posibles) == 1:
            return jugadas_posibles[0]

        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')
        
        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'black'

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
                                              text=' o*'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()

if __name__ == '__main__':
    juego=Othello()
    juego.imprimirTablero()
    print(juego.jugadas_legales())
    print(juego.terminal())
    OthelloTK().arranca()
    #juego=Othello()
    #juego.imprimirTablero()
    #juego.jugadas_legales()
    
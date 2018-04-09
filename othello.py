#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Belen Chavarría'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk
from random import shuffle
import time


class othello(JuegoSumaCeros2T):
    
    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:

                        0   1   2   3   4   5   6   7
                        8   9   10  11  12  13  14  15
                        16  17  18  19  20  21  22  23
                        24  25  26  27  28  29  30  31
                        32  33  34  35  36  37  38  39
                        40  41  42  43  44  45  46  47
                        48  49  50  51  52  53  54  55
                        56  57  58  59  60  61  62  63
        """
        
        x= [0 for _ in range(64)]
        x[27]=-1
        x[36]=-1
        x[28]=1
        x[35]=1
        
        super().__init__(tuple(x))
        
        self.x_anterior=[] #pila de estados anteriores
        
        
    def jugadas_legales(self):
        #cualquier espacio vacío
        #return (j for j in range(64) if self.x[j] == 0)
        
        jugadas = []
        
        
        #solo donde encierra a las fichas contrincantes (self.jugador*-1)
        for i in range(64):
            if self.x[i]==0:
                if i<46 and i%8<6 and i+9<64 and self.x[i+9]== -1*self.jugador:
                    #si enciera en diagonal abajo derecha
                    flag, index = False, i+18
                    while not flag and index <64:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index+=9                            
                            
                if i<48 and i%8>1 and i+7<64 and self.x[i+7]== -1*self.jugador:
                    #si enciera en diagonal abajo izquierda
                    flag, index = False, i+14
                    while not flag and index <64:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index+=7
                    
                if i>15 and i%8<6 and i-7>=0 and self.x[i-7]== -1*self.jugador:
                    #si enciera en diagonal arriba derecha
                    
                    
                    flag, index = False, i-14
                    
                    while not flag and index>=0:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            #print("jugadas" , jugadas)
                            flag=True
                        index-=7
                    
                if i>17 and i%8>1 and i-9>=0 and self.x[i-9]== -1*self.jugador:
                    #si enciera en diagonal arriba izquierda
                    flag, index = False, i-18
                    while not flag and index>=0:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index-=9
                    
                
                if i%8>1 and self.x[i-1]== -1*self.jugador:
                    #si encierra en renglones izquierda
                    flag, index = False, i-2
                    while not flag and index>= int(i/8)*8:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index-=1
                        
                if i%8<6  and self.x[i+1]== -1*self.jugador:
                    #si encierra en renglones derecha
                    flag, index, cota= False, i+2, int(i/8)*8+8
                    while not flag and index < cota:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index+=1
                        
                if i<48 and i+8<64 and self.x[i+8]== -1*self.jugador:
                    #si encierra en columna abajo
                    flag, index = False, i+16
                    while not flag and index<64:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index+=8
                        
                if i>15  and self.x[i-8]== -1*self.jugador:
                    #si encierra en columna arriba
                    flag, index = False, i-16
                    while not flag and index>=0:
                        if self.x[index]==0:
                            flag=True
                        elif self.x[index]==self.jugador:
                            jugadas.append(i)
                            flag=True
                        index-=8
                                
        return tuple(set(jugadas))
            
    def terminal(self):
        """
        Devuelve None si no es terminal el estado actual,
        en otro caso devuelve la ganancia para el jugador 1.
        """
        if 0 not in self.x:
            return utilidad(self.x)
            
            
        if not self.jugadas_legales():
            self.jugador=-1*self.jugador
            if not self.jugadas_legales():
                self.jugador=-1*self.jugador
                return utilidad(self.x)
            self.jugador=-1*self.jugador
            
            
        return None
        
        
    def hacer_jugada(self, jugada):
        
        self.x_anterior.append(self.x[:])
        self.historial.append(jugada)
        self.x[jugada] = self.jugador
        self.cambiar(jugada)
        self.jugador *= -1

    def deshacer_jugada(self):
        jugada = self.historial.pop()
        #print(self.x_anterior)
        self.x = self.x_anterior.pop()
        self.x[jugada] = 0
        self.jugador *= -1
        
    def cambiar(self,i):
        self.x[i] = self.jugador


        def hacerCambio(L):
            for i in L:
                self.x[i]=self.jugador

        def agregarCambio(i,lc,pasos, cota, fun):
            
            index = i + pasos
            lc.append(index)
            cambio,flag, index = False,False, index + pasos
            while not flag and not cambio and fun(index,cota):
                if self.x[index]==0:
                    flag=True
                elif self.x[index]==self.jugador:
                    cambio=True
                else:
                    lc.append(index)
                index+=pasos
                
            return cambio
            
            
        lcambios=[]
        if i<46 and i%8<6 and i+9<64 and self.x[i+9]== -1*self.jugador:
            #si enciera en diagonal abajo derecha
            cambio = agregarCambio(i,lcambios,9, 64, lambda x,y : x<y)
            if cambio:
                hacerCambio(lcambios)
        
                                     
        lcambios=[]                    
        if i<48 and i%8>1 and i+7<64 and self.x[i+7]== -1*self.jugador:
            #si enciera en diagonal abajo izquierda
            cambio = agregarCambio(i,lcambios,7, 64, lambda x,y : x<y)
            if cambio:
                hacerCambio(lcambios)
                    
        lcambios=[]
        if i>15 and i%8<6 and i-7>=0 and self.x[i-7]== -1*self.jugador:
            #si enciera en diagonal arriba derecha
            cambio = agregarCambio(i,lcambios,-7, 0, lambda x,y : x>=y)
            if cambio:
                hacerCambio(lcambios)
        
        lcambios=[]
        if i>17 and i%8>1 and i-9>=0 and self.x[i-9]== -1*self.jugador:
            #si enciera en diagonal arriba izquierda
            cambio = agregarCambio(i,lcambios,-9, 0, lambda x,y : x>=y)
            if cambio:
                hacerCambio(lcambios)
        
        lcambios=[]
        if i%8>1 and self.x[i-1]== -1*self.jugador:
            #si encierra en renglones izquierda
            cambio = agregarCambio(i,lcambios,-1, int(i/8)*8, lambda x,y : x>=y)
            if cambio:
                hacerCambio(lcambios)
        
        lcambios=[]
        if i%8<6  and self.x[i+1]== -1*self.jugador:
            #si encierra en renglones derecha
            cambio = agregarCambio(i,lcambios,1, int(i/8)*8+8, lambda x,y : x<y)
            if cambio:
                hacerCambio(lcambios)
        
        lcambios=[]
        if i<48 and i+8<64 and self.x[i+8]== -1*self.jugador:
            #si encierra en columna abajo
            cambio = agregarCambio(i,lcambios,8, 64, lambda x,y : x<y)
            if cambio:
                hacerCambio(lcambios)
                       
        lcambios=[]
        if i>15  and self.x[i-8]== -1*self.jugador:
            #si encierra en columna arriba
            cambio = agregarCambio(i,lcambios,-8, 0, lambda x,y : x>=y)
            if cambio:
                hacerCambio(lcambios)

                        
                        
        

def utilidad(x):
    cont=0
    """
    for i in range(64):
        if x[i]==jugador:
            cont+=1
    return cont
    """
    for i in range(64):
        cont+=x[i]

    return cont
       
def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    jugadas2 = []
    #primero esquinas
    for thing in [0,7,56,63]:
        if thing in jugadas: jugadas.remove(thing), jugadas2.append(thing)
    #despues marcos de la cuadricula, entre más cercanos a la orilla, mayor prioridad
    for i in range(4):
        if jugadas:
            for j in jugadas:
                if j%8==i and j not in jugadas2: jugadas2.append(j)
                elif j%8==7-i and j not in jugadas2: jugadas2.append(j)
                elif int(j/8) == i and j not in jugadas2: jugadas2.append(j)
                elif int(j/8)==7-i and j not in jugadas2: jugadas2.append(j)
                
    return jugadas2
    
def juega_othello(jugador=1):
    
    juego = othello()

    tipo= 'X' if jugador==1 else 'O'
    print("las 'X' siempre empiezan".center(60))
    print("y tu juegas con {}".format(tipo).center(60))

    if jugador is -1: #si empieza la computadora "O"
        jugada = minimax(juego,10,utilidad)
        juego.hacer_jugada(jugada)

    acabado = False

    for _ in range(64):
        pprint_othello(juego.x)
        legales = juego.jugadas_legales()
        print("yo" ,legales)
        
        if legales: # si puede jugar
            print("Escoge tu jugada (uno de los números que quedan en el tablero)")
    
            try:
                jugada = int(input("Jugador {}: ".format(jugador)))
                print(jugada)
            except:
                print("¡No seas macana y pon un número!")
                continue
            if jugada not in legales:
                print("¡No seas macana, pon un número válido!")
                continue

            juego.hacer_jugada(jugada)
            
            #if juego.terminal(jugador) is None:
            #   acabado = True

        else: #si pasa de turno
            juego.jugador = -1 * juego.jugador
        
        
        
        legales = juego.jugadas_legales()
        print("maquina" ,legales)
        print(utilidad)
        jugada = minimax(juego,10, utilidad)
            
        if jugada:
            print("jugada M", jugada)
            juego.hacer_jugada(jugada)
            #if juego.terminal(jugador) is None:
            #    acabado = True
        else:
            juego.jugador = -1 * juego.jugador

                
    pprint_othello(juego.x)
    u = utilidad(juego.x)
    if u == 0:
        print("UN ASQUEROSO EMPATE".center(60))
    elif (primero<0 and u>0) or (primero>0 and u<0):
        print("¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?".center(60))
    else:
        print("Ganaste, bye.")
    print("\n\nFin del juego")
  
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
    
def puntos(x, jugador):
    cont=0
    for i in range(64):
        if x[i]==jugador:
            cont+=1
    return cont
    
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
        
        self.userpoints = tk.Label(barra, bg='light grey', text="YO: ")
        self.userpoints.grid(column=0, row=0)
       
        
        botonX = tk.Button(barra,
                           command=lambda x=1: self.jugar(x),
                           text='(re)iniciar con X')
        botonX.grid(column=1, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=-1: self.jugar(x),
                           text='(re)iniciar con O')
        botonO.grid(column=2, row=0)
        self.Mpoints = tk.Label(barra, bg='light grey',  text="Máquina: ")
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
        juego = othello()

        
        if  primero == -1:
            jugada = minimax(juego,5, utilidad, ordena_jugadas)
            juego.hacer_jugada(jugada)

        self.anuncio['text'] = "A ver de que cuero salen más correas"
        for _ in range(64):
            self.actualiza_tablero(juego.x)
            if juego.jugadas_legales():
                
                jugada = self.escoge_jugada(juego)
                juego.hacer_jugada(jugada)
                
                #actualiza los puntos
                self.userpoints['text'] = "YO: {} ".format(puntos(juego.x, primero))
                self.userpoints.update()
                self.Mpoints['text'] = "M: {} ".format(puntos(juego.x, -1*primero))
                self.Mpoints.update()
                #actualiza tablero
                self.actualiza_tablero(juego.x)
                ganador = juego.terminal()
                if ganador is not None:
                    break
            else:
                print("No hay jugadas para ti...")
                juego.jugador = -1*juego.jugador
                
            if juego.jugadas_legales():
                jugada = minimax(juego,5, utilidad, ordena_jugadas)
                juego.hacer_jugada(jugada)
                #actualiza los puntos
                self.userpoints['text'] = "YO: {} ".format(puntos(juego.x, primero))
                self.userpoints.update()
                self.Mpoints['text'] = "M: {} ".format(puntos(juego.x, -1*primero))
                self.Mpoints.update()
                
                ganador = juego.terminal()
                if ganador is not None:
                    break
            else:
                print("No hay jugadas para la máquina...")
                juego.jugador = -1*juego.jugador

        self.actualiza_tablero(juego.x)
        u = utilidad(juego.x)
        if u == 0:
            fin = "UN ASQUEROSO EMPATE"
        elif (primero<0 and u>0) or (primero>0 and u<0):
            fin ="¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?"
        else:
            fin ="Ganaste, bye."
            
        print("\n\nFin del juego")
        self.anuncio['text'] = fin
        self.anuncio.update()

    def escoge_jugada(self, juego):
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
    #juega_othello()
    OthelloTK().arranca()
    
    """
    o = othello()
    print(o.jugador)
    print(o.jugadas_legales())
    pprint_othello(o.x)
    jugada = minimax(o,7,utilidad,ordena_jugadas)
    print(jugada)
    o.hacer_jugada(jugada)
    pprint_othello(o.x)
    """
    
    
    
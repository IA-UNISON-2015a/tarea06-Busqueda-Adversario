#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Adrian Emilio Vazquez Icedo'

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk
from copy import deepcopy
from collections import deque
# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
"""

    Pruebas vs aplicacion a maximo nivel(nivel 10)
    
    Empezo el programa y gano la aplicacion.
    Empiezo la aplicacion y gano este programa.
    Empiezo la aplicacion y gano la aplicacion.
    Empezo el programa y gano la aplicacion.
    
    De cuatro partidas quedamos 3-1 :(

    Pero considerando que mi funcion de utilidad es muy simple ganar 1 ya es algo.
    
"""
class othello(JuegoSumaCeros2T):
    """
    El juego del othello.
         0   1   2   3   4   5   6  7
         8   9  10  11  12  13  14  15 
        16  17  18  19  20  21  22  23
        24  25  26  27  28  29  30  31
        32  33  34  35  36  37  38  39
        40  41  42  43  44  45  46  47
        48  49  50  51  52  53  54  55
        56  57  58  59  60  61  62  63
         
    """
    def __init__(self, jugador=1):
        """
        Inicializa el juego del othello
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0  -1   1   0   0   0
            0   0   0   1  -1   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            0   0   0   0   0   0   0   0
            
        """
        
        x=[0 for _ in range(64)]
        
        x[27]=x[36]=-1
        x[28]=x[35]=1
        
        super().__init__(x)
        
        #historial de estados, jugadas y fronteras en el tablero
        self.x_anterior=deque()
        self.historial=deque()
        self.frontera_anterior=deque()
        
        #la frontera almacena las casillas pegadas horizontal, vertical o esquiniadas o una casilla con piezas
        self.frontera = set()
        #Se guardan las primeras casillas en la frontera
        for casilla in (18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45):
            self.frontera.add(casilla)
    
    
    def jugadas_legales(self):
        
        #almacena las jugadas donde podra poner el jugador actual
        jugadas = []
        
        #se revisa la frontera ya que son las unicas casillas donde podria haber un movimiento legal
        for jugada in self.frontera:
            
            valida = self.revisar_capturas(jugada, 0) 
            #Si tubo almenos una forma de capturar fichas se agrega a las jugadas validas
            if True in valida:
                jugadas.append(jugada)                       

        return jugadas
    
    
    def terminal(self):

        #Si se lleno el tablero 
        if 0 not in self.x:
            return utilidad(self.x)
            
        #Si ya no es posible realizar un movimiento por parte de los dos jugadores    
        if not self.jugadas_legales():
            self.jugador=-1*self.jugador
            if not self.jugadas_legales():
                self.jugador=-1*self.jugador
                return utilidad(self.x)
            self.jugador=-1*self.jugador
            
            
        return None
    
    def deshacer_jugada(self):
        
        #Reviso la ultima jugada que se realizo
        jugada = self.historial.pop()
        
        #Si jugo el jugador contrario, significa que sera su turno
        if self.x[jugada] == -1*self.jugador:
            self.jugador *= -1
            
        #Regreso al estado anterior
        self.x = self.x_anterior.pop() 
        #Regreso a la frontera anterior
        self.frontera = self.frontera_anterior.pop()
        
    
    def revisar_capturas(self, jugada, cambiar=0):
    
        """
            Direccion en que se revisan los cambio
            
            7   0   1
              7 0 1
            6 6 J 2 2 
              5 4 3
            5   4   3
        """
        
        cambio=0
        cambios=[False for i in range(8)] #revisar cambio en las 8 direcciones
        
        
        if jugada//8>1: #Revisar cambios hacia arriba
            if self.x[(jugada-8)]==self.jugador*-1:
                renglon = [self.x[i] for i in range(jugada-16, -1, -8)]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[0]=True


        if jugada%8<6 and jugada//8>1: #Revisar cambios hacia arriba derecha
            if self.x[(jugada-7)]==self.jugador*-1:
                renglon = [self.x[jugada-i*7] for i in range(2, (8-jugada%8)) if jugada-i*7>0]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[1]=True

        if jugada%8<6: #Revisar cambios hacia derecha
            if self.x[(jugada+1)]==self.jugador*-1:
                renglon = [self.x[i] for i in range(jugada+2, jugada+8-jugada%8)]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[2]=True

        if jugada%8<6 and jugada//8<6: #Revisar cambios hacia abajo derecha
            if self.x[(jugada+9)]==self.jugador*-1:
                renglon = [self.x[jugada+i*9] for i in range(2, (8-jugada%8)) if jugada+i*9<=63]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[3]=True

        if jugada//8<6: #Revisar cambios hacia abajo
            if self.x[(jugada+8)]==self.jugador*-1:
                renglon = [self.x[i] for i in range(jugada+16, 64, 8)]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[4]=True
  
        if jugada%8>1 and jugada//8<6: #Revisar cambios hacia abajo izquierda
            if self.x[(jugada+7)]==self.jugador*-1:
                renglon = [self.x[jugada+i*7] for i in range(2, jugada%8+1) if jugada+i*7<63]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[5]=True

        if jugada%8>1: #Revisar cambios hacia izquierda 
            if self.x[(jugada-1)]==self.jugador*-1:
                renglon = [self.x[i] for i in range(jugada-2, jugada-jugada%8-1, -1)]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[6]=True
                    

        if jugada%8>1 and jugada//8>1: #Revisar cambios hacia arriba izquierda
            if self.x[(jugada-9)]==self.jugador*-1:
                renglon = [self.x[jugada-i*9] for i in range(2, jugada%8+1) if jugada-i*9>=0]
                cambio=False#Por si toda la columna esta completa de fichas contrarias
                for i in renglon:
                    
                    if i == self.jugador:
                        cambio=True
                        break
                    elif i == 0:
                        cambio=False
                        break
                if cambio==True:
                    cambios[7]=True

        if cambiar==1:#Si se indica que se deben cambiar las fichas 
            for (direccion, distancia) in zip(cambios, (-8, -7, 1, 9, 8, 7, -1, -9)):
                    # Si una fila fue capturada, voltea todas las fichas del oponente
                    # que estén entre dos fichas del jugador actual.
                    if direccion:
                        ficha = jugada + distancia
                        while(self.x[ficha] != self.jugador):
                            self.x[ficha] = self.jugador
                            ficha += distancia
        return cambios
                         
            
                        
    def hacer_jugada(self, jugada):

        
        self.x_anterior.append(self.x[:])#guardamos el estado actual
        self.frontera_anterior.append(deepcopy(self.frontera))#Guardamos la frontera actual
        self.x[jugada] = self.jugador#realizamos la jugada en el estado actual

        #Cambios en el tablero probocados por la jugada actual
        self.revisar_capturas(jugada, 1)
        
        
        #actualizar frontera
        nuevosV=[]

        if jugada%8>0: #izquierda
            nuevosV.append(jugada-1)
            if jugada//8>0: #izquierda-arriba
                nuevosV.append(jugada-9)   
            if jugada//8<7: #izquiera-abajo
                nuevosV.append(jugada+7)
                
        if jugada%8<7: #derecha
            nuevosV.append(jugada+1)     
            if jugada//8>0: #derecha-arriba
                nuevosV.append(jugada-7)   
            if jugada//8<7:  #derecha-abajo
                nuevosV.append(jugada+9)
                
        if jugada//8>0: #arriba
            nuevosV.append(jugada-8)   
        if jugada//8<7:  #abajo
            nuevosV.append(jugada+8)
        
        for i in nuevosV:
            if self.x[i]==0:
                self.frontera.add(i)
                
        self.frontera.remove(jugada)#remover movimiento actual              
        self.jugador *= -1#cambiamos el turno  
        self.historial.append(jugada)#registramos la jugada en el historial

        return None




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


class othelloTK:
    def __init__(self, escala=2):
        self.app = app = tk.Tk()
        self.app.title("El juego del othello")
        self.L = L = int(escala) * 35

        tmpstr = "Escoge con que ficha juegas(empiezan las negras):"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=3 * L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()

        self.userpoints = tk.Label(barra, bg='white', text="Jugador: 2")
        self.userpoints.grid(column=0, row=0)

        botonX = tk.Button(barra,
                           command=lambda x=True: self.jugar(x),
                           text='Jugar con negras')
        botonX.grid(column=1, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=False: self.jugar(x),
                           text='Jugar con blancas')
        botonO.grid(column=2, row=0)

        self.Mpoints = tk.Label(barra, bg='white',  text="Máquina: 2")
        self.Mpoints.grid(column=3, row=0)

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
                                                         font=letra, text=' ')
            self.tablero[i].val = 0
            self.tablero[i].pos = i
    def limpiar_jugada(self, juego):
        for i in range(64):
            self.tablero[i].unbind('<Enter>')
            self.tablero[i].unbind('<Leave>')
            self.tablero[i].unbind('<Button-1>')
        
    def jugar(self, primero):
        
        juego = othello()
        """
            El metodo limpiar_jugada lo agregue ya que al reiniciar una partida sin terminar
            me salian de color cuadros donde no debia poder poner por lo cual le quito esa propiedad
            a todos para que vuelva a ejecutarse como la primera vez
        """
        self.limpiar_jugada(juego)
        print(juego.frontera)
        self.actualiza_tablero(juego.x)
        
        #Inicializar marcador
        self.userpoints['text'] = "Jugador: 2 "
        self.userpoints.update()
        self.Mpoints['text'] = "Máquina: 2 "
        self.Mpoints.update()
        
        if not primero:
            primero=-1
            jugada = minimax(juego,5, utilidad, ordena_jugadas)

            juego.hacer_jugada(jugada)
        else:
            primero=1
        self.anuncio['text'] = "Que gane el mejor"
        
        for _ in range(64):
                self.actualiza_tablero(juego.x)

                if juego.jugadas_legales():
                    
                    jugada = self.escoge_jugada(juego)
                    juego.hacer_jugada(jugada)
                    
                    #actualiza los puntos
                    self.userpoints['text'] = "Jugador: {} ".format(puntos(juego.x, primero))
                    self.userpoints.update()
                    self.Mpoints['text'] = "Máquina: {} ".format(puntos(juego.x, -1*primero))
                    self.Mpoints.update()
                    #actualiza tablero
                    self.actualiza_tablero(juego.x)
                else:
                    print("No hay jugadas para ti...")
                    juego.jugador = -1*juego.jugador#cambio de turno 
                    
                    
                ganador = juego.terminal()
                if ganador is not None:break#revisa si finalizo el juego
            
                if juego.jugadas_legales():
                    jugada = minimax(juego,5, utilidad, ordena_jugadas)
                    juego.hacer_jugada(jugada)
                    #actualiza los puntos
                    self.userpoints['text'] = "Jugador: {} ".format(puntos(juego.x, primero))
                    self.userpoints.update()
                    self.Mpoints['text'] = "Máquina: {} ".format(puntos(juego.x, -1*primero))
                    self.Mpoints.update()
                    
                    
                else:
                    print("No hay jugadas para la máquina...")
                    juego.jugador = -1*juego.jugador#cambio de turno 
                
                ganador = juego.terminal()
                if ganador is not None:break#revisa si finalizo el juego
    
        
        u = utilidad(juego.x)
        if u == 0:
           fin = "UN ASQUEROSO EMPATE"
        elif (primero<0 and u>0) or (primero>0 and u<0):
           fin ="GG EZ"
        else:
           fin ="Ganaste, bye."
        self.actualiza_tablero(juego.x)
        print("\n\nFin del juego")
        self.anuncio['text'] = fin
        self.anuncio.update()
            

    def escoge_jugada(self, juego):
        
        jugadas_posibles = juego.jugadas_legales()

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
            if self.tablero[i].val != x[i]:#revisa si hubo un combio en la casilla
                if x[i]==-1:
                    self.tablero[i].itemconfigure(self.textos[i],
                                              text='o', fill="white")
                elif x[i]==1:
                    self.tablero[i].itemconfigure(self.textos[i],
                                              text='o', fill="black")
                else:
                    self.tablero[i].itemconfigure(self.textos[i],
                                              text=' ')
                self.tablero[i].val = x[i]
                self.tablero[i].update()


    def arranca(self):
        self.app.mainloop()
     



def utilidad(x):
    
    """
        Valor en el tablero
        5   4   4   4   4   4   4   5
        4   3   3   3   3   3   3   4
        4   3   2   2   2   2   3   4
        4   3   2   1   1   2   3   4
        4   3   2   1   1   2   3   4
        4   3   2   2   2   2   3   4
        4   3   3   3   3   3   3   4
        5   4   4   4   4   4   4   5
        
    """
    cont=0
    for i in range(64):#las fichas valen de 1 a 4 dependiendo que tan al brode estan
        
        if i%8==0 or i%8==7 or i//8==0 or i//8==7:
            cont+=x[i]*4
        elif i%8==1 or i%8==6 or i//8==1 or i//8==6:
            cont+=x[i]*3
        elif i%8==2 or i%8==5 or i//8==2 or i//8==5:
            cont+=x[i]*2   
        else:
            cont+=x[i]  
        
    for i in [0,7,56,63]:#Si estan en la esquina reciben un punto mas
        cont+=x[i]
        
    return cont

def ordena_jugadas(juego):
    jugadas = list(juego.jugadas_legales())
    jugadasOrden = []
    
    for i in [0,7,56,63]:#Primero se agregan las esquinas si es posible jugar es esa posicion
        if i in jugadas: jugadas.remove(i), jugadasOrden.append(i)
    
    for i in range(4):#Despues se van agregando entre mas cercanas al borde del tablero esten.
        if jugadas:
            for j in jugadas:
                if j%8==i and j not in jugadasOrden: jugadasOrden.append(j)
                elif j%8==7-i and j not in jugadasOrden: jugadasOrden.append(j)
                elif int(j/8) == i and j not in jugadasOrden: jugadasOrden.append(j)
                elif int(j/8)==7-i and j not in jugadasOrden: jugadasOrden.append(j)
    
    return jugadasOrden

def puntos(x, jugador):
    cont=0
    for i in range(64):
        if x[i]==jugador:
            cont+=1
    return cont

if __name__ == '__main__':
    # juega_gato('X')
    othelloTK().arranca()

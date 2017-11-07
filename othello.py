#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
from busquedas_adversarios import JuegoSumaCeros2T
from copy import deepcopy
from random import choice
import tkinter as tk
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from win32evtlog import EvtGetEventInfo
from lxml.html.defs import tags
from sklearn import __check_build
from random import shuffle


__author__ = 'Jorge Adrian Olmos Morales'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class Othello(JuegoSumaCeros2T):
    
    def __init__(self, jugador=1):
        
        self.historial = []
        #El estado del juego se representa por una matriz (tal vez usar una lista de listas no sea los más optimo)
        self.tablero = [ [0 for _ in range(8)] for _ in range(8) ]
        self.tablero[3][3] = 1
        self.tablero[4][3] = 1
        self.tablero[3][4] = -1
        self.tablero[4][4] = -1
        
        self.x = [] 
        for row in self.tablero:
            for x in row:
                self.x.append(x)
        self.x = tuple(self.x)
        self.jugador = jugador
                    
    def jugadas_legales(self):

        jugadas = []
        for i in range(8):
            for j in range(8):
                if(self.tablero[i][j] == 0):
                    if(self.check_vecinos(i,j)):
                        patterns = self.check_patterns((i,j))
                        for pattern in patterns:
                            if(len(pattern) > 1 ):
                                jugadas.append((i,j))
        return jugadas
    
    def check_positive_position(self, place):
        patterns = self.check_patterns(place)
        for pattern in patterns:
            if(len(pattern) > 1 ):
                return True
        else:
            return False
    
    def check_vecinos(self, i,j):
        
        aux_i,aux_j = i-1,j-1
        if(aux_i >= 0 and aux_j >= 0 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i-1,j
        if(aux_i >= 0 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i-1,j+1
        if(aux_i >= 0 and aux_j <= 7 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i,j-1
        if(aux_j >= 0 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i,j+1
        if(aux_j <= 7 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i+1,j-1
        if(aux_i <= 7 and aux_j >= 0 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i+1,j
        if(aux_i <= 7 and self.tablero[aux_i][aux_j] != 0):
            return True
        aux_i,aux_j = i+1,j+1
        if(aux_i <= 7 and aux_j <=7 and self.tablero[aux_i][aux_j] != 0):
            return True
    
    #Recoge todas aquellas casillas para las cuales se posiblemente se cambiara el color
    def check_patterns(self, jugada):
        patterns = []
        
        aux = []
        i,j = jugada[0],jugada[1]
        
        aux_i,aux_j = i-1,j-1
        while(aux_i >= 0 and aux_j >= 0):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_i, aux_j = aux_i-1, aux_j-1
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
            
        aux = []
        aux_i,aux_j = i-1,j
        while(aux_i >= 0):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_i = aux_i-1
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
        
        aux = []
        aux_i,aux_j = i-1,j+1
        while(aux_i >= 0 and aux_j <= 7):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_i,aux_j = aux_i-1,aux_j+1       
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
        
        aux = []
        aux_i,aux_j = i,j-1
        while(aux_j >= 0):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_j = aux_j-1       
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
        
        aux = []
        aux_i,aux_j = i,j+1
        while(aux_j <= 7):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_j = aux_j+1       
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
       
        aux = []
        aux_i,aux_j = i+1,j-1
        while(aux_i <=7 and aux_j >= 0):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_i, aux_j = aux_i+1, aux_j-1       
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
         
        aux = []
        aux_i,aux_j = i+1,j
        while(aux_i <=7):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_i = aux_i+1     
        if(len(aux) > 0 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
       
        aux = []
        aux_i,aux_j = i+1,j+1
        while(aux_i <=7 and aux_j <= 7):
            if(self.tablero[aux_i][aux_j] != 0 and self.tablero[aux_i][aux_j] != self.jugador):
                aux.append((aux_i,aux_j))
            else:
                aux.append((aux_i,aux_j))
                break
            aux_i, aux_j = aux_i+1, aux_j+1     
        if(len(aux) > 1 and self.tablero[aux[-1][0]][aux[-1][1]] == self.jugador): 
            patterns.append(deepcopy(aux))
    
        return patterns
      
    def terminal(self):
        #El estado del juego es terminal cuando no hay movimientos legales para ambos jugadores
        player1 = self.jugadas_legales()
        self.jugador *= -1
        player2 = self.jugadas_legales()
        self.jugador *= -1
        if((len(player1) == 0 and len(player2) == 0)):
            cont = 0
            cont2 = 0
            for row in self.tablero:
                cont += row.count(1)
                cont2 += row.count(-1)
            return cont - cont2
        else:
            
            return None
        
    def hacer_jugada(self, jugada):
        self.tablero[jugada[0]][jugada[1]] = self.jugador
        
        patterns = self.check_patterns(jugada) #recoge las casillas a cambiar
        
        cambiar = []
        cambiar.append((jugada))
        #En esta parte se decide finalmente que casillas del tablero se modificaran
        for pattern in patterns:
            aux_cambiar = []
            if(len(pattern) > 0 and self.tablero[pattern[0][0]][pattern[0][1]] != self.jugador and self.tablero[pattern[0][0]][pattern[0][1]] != 0):
                aux_cambiar.append(pattern[0])
                for i in range(len(pattern)-1):
                        if(self.tablero[pattern[i+1][0]][pattern[i+1][1]] == self.jugador):
                            break
                        if(self.tablero[pattern[i+1][0]][pattern[i+1][1]] == 0):
                            del aux_cambiar[:]
                            break
                        if(self.tablero[pattern[i+1][0]][pattern[i+1][1]] == -1*self.jugador):
                            aux_cambiar.append(pattern[i+1])     
                cambiar.extend(aux_cambiar)
        
        self.historial.append(cambiar)
        #Altera la matriz del juego (tablero/estado) de acuerdo a las pieza que se capturaron
        for tupla in cambiar:
            self.tablero[tupla[0]][tupla[1]] = self.jugador
           
    def deshacer_jugada(self):
        jugada_deshacer = self.historial.pop()
        self.tablero[jugada_deshacer[0][0]][jugada_deshacer[0][1]] = 0
        del jugada_deshacer[0]
        for tupla in jugada_deshacer:
            self.tablero[tupla[0]][tupla[1]] *= -1
            


def utilidad_othello(tablero):
    #numero de fichas rojas - numero de fichas negras
    cont = 0
    cont2 = 0
    for row in tablero:
        if(row is list):
            cont += row.count(1)
            cont2 += row.count(-1)
    return cont-cont2


def ordena_jugadas(juego):
    
    #ordena las jugadas de acuedo al numero de fichas rojas despues del movimento
    jugadas = list(juego.jugadas_legales())
    jugadas_ordenadas = []
    for jugada in jugadas:
        juego.hacer_jugada(jugada)
        jugadas_ordenadas.append(((jugada), utilidad_othello(juego.tablero)))
        juego.deshacer_jugada()
    jugadas_ordenadas.sort(key=lambda tupla: tupla[1], reverse=True)
    jugadas = []
    for jugada in jugadas_ordenadas:
        jugadas.append(jugada[0])
    return jugadas
    


class OthelloGUI():
    def __init__(self, tmax=10, escala=1):
        
        # La tabla de transposición
        self.tr_ta = {}

        # Máximo tiempo de búsqueda
        self.tmax = tmax

        self.app = app = tk.Tk()
        self.app.title("Othello")
        self.L = L = int(escala) * 50
        
        tmpstr = "Escoge color, rojas empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=7*L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonR = tk.Button(barra, command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con rojas', width=22)
        botonR.grid(column=0, row=0)
        botonN = tk.Button(barra, command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con negras', width=22)
        botonN.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        
        self.can = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                self.can[i][j] = tk.Canvas(ctn, height=L, width=L,
                                    bg='light grey', borderwidth=0)
                self.can[i][j].grid(row=i, column=j)
                self.can[i][j].create_oval(5, 5, L, L,fill='white', width=2, tags=(str(i)+str(j)))
                self.can[i][j].val = [0,i,j]
        
                
    def jugar(self, primero):
        
        
        
        juego = Othello()
        self.actualizar_tablero(juego)
        
        if not primero:
            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            jugada = minimax(juego, dmax=6, utilidad=utilidad_othello,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualizar_tablero(juego)
            juego.jugador *= -1
        
        def check_i_j(event):
            if((event.widget.val[1],event.widget.val[2]) in self.posibles):
                juego.hacer_jugada((event.widget.val[1],event.widget.val[2]))
                self.actualizar_tablero(juego)
                self.var.set(0)
        self.var = tk.IntVar()   
        
        while(juego.terminal() == None):
            self.anuncio['text'] = "Te toca jugar"
            self.anuncio.update()
            self.posibles = []
            for i in range(8):
                for j in range(8):
                    if(juego.tablero[i][j] == 0 and juego.check_positive_position((i,j))):
                        self.can[i][j].bind("<Button 1>", check_i_j)
                        self.posibles.append((i,j))          
            if(juego.terminal() != None):
                break;
            self.anuncio.wait_variable(self.var)
            juego.jugador *= -1
            
            if(len(juego.jugadas_legales()) == 0):
                juego.jugador *= -1
            else:
                self.posibles = []
                self.anuncio['text'] = "Ahora juega Python"
                self.anuncio.update()
                jugada = minimax(juego, dmax=3, utilidad=utilidad_othello,
                                 ordena_jugadas=ordena_jugadas,
                                 transp=self.tr_ta)
                juego.hacer_jugada(jugada)
                self.actualizar_tablero(juego)
                if(juego.terminal() != None):
                    break;
                juego.jugador *= -1
                
            # esta parte permite jugar sin la maquina
        """ self.posibles = []
            for i in range(8):
                for j in range(8):
                    if(juego.tablero[i][j] == 0 and juego.check_positive_position((i,j))):
                        self.can[i][j].bind("<Button 1>", check_i_j)
                        self.posibles.append((i,j))          
            if(juego.terminal() != None):
                break;
            self.anuncio.wait_variable(self.var)
            juego.jugador *= -1
        
            if(len(juego.jugadas_legales()) == 0):
                juego.jugador *= -1 """       
           
            
        str_fin = ("Ganaron las rojas" if juego.terminal() > 0 else
                   "Ganaron las negras" if juego.terminal() < 0 else
                   "Un asqueroso empate")
        self.anuncio['text'] = str_fin
        self.anuncio.update()
         
    def arranca(self):
        self.app.mainloop()
        
    def actualizar_tablero(self,juego):
        for i in range(8):
            for j in range(8):
                self.can[i][j].val[0] = juego.tablero[i][j]
                if(self.can[i][j].val[0] == 0):
                    self.can[i][j].itemconfigure(1, fill='white')
                elif(self.can[i][j].val[0] == 1):
                    self.can[i][j].itemconfigure(1, fill='red')
                elif(self.can[i][j].val[0] == -1):
                    self.can[i][j].itemconfigure(1, fill='black')
    
    
if __name__ == '__main__':
    
    #ya que la IA tarda en responder (se congela despues de algunas jugadas, supongo debido a ineficiencias en el código)
    #no se pudo comprobar si esta IA seria un buen contrincante en othello
    OthelloGUI(tmax=10).arranca()

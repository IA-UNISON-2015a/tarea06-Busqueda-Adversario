# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 20:28:42 2019

@author: Ariana
"""

def arranca(x, y):
    t = crear_tablero(x, y)
    jugar(t)


def entrada():
    try:
        x, y = eval(input('Ingrese jugada (x,y),(j,v)'))

    except:
        print("Error al ingresar jugada")

    return x, y

def validar(tab, jugada):

    cord1, cord2 = jugada
    x, y = cord1
    j, v = cord2

    try:
        x = x * 2
        y = y * 2
        j = j * 2
        v = v * 2
    except:
        return False

    distX = x - j
    distY = y - v

    cordX = (x + j) / 2
    cordY = (y + v) / 2

    try:
        if tab[x][y] == '+' and tab[j][v] == '+':
            if distX == 2 or distX == -2 or distX == 0:
                if distY == 2 or distY == -2 or distY == 0:
                    if tab[int(cordX)][int(cordY)] == 1 or tab[int(cordX)][int(cordY)] == '1':
                        return True
                    return False
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False

def atualizar(tab, play):
    cord1, cord2 = play
    x, y = cord1
    j, v = cord2

    x = x * 2
    y = y * 2
    j = j * 2
    v = v * 2

    cordX = (x + j) / 2
    cordY = (y + v) / 2

    if cordY % 2 != 0:
        tab[int(cordX)][int(cordY)] = "-"
    else:
        tab[int(cordX)][int(cordY)] = "|"

    return tab


def jugar(tab, jugador="A"):

    imprimir_tablero(tab)

    print("Jugador ", jugador, ":")
    
    jugada = entrada()
    if validar(tab, jugada):
        print("Jugada inválida")
    
    tab = atualizar(tab, jugada)
    tab, hit = cuadrado(tab, jugador)

    if fin_juego(tab):
        a, b = puntos(tab)
        imprimir_tablero(tab)
        print("Fin del juego. Puntos: A ", a, "  B ", b)

        hit = 0
        return

    if hit:
        jugar(tab, jugador)

    jugar(tab, cambiar_jugador(jugador))

    jugar(tab, jugador)


def puntos(tab):
    puntosA = 0
    puntosB = 0

    for x in tab:
        for y in x:
            if y == "A":
                puntosA = puntosA + 1
            elif y == "B":
                puntosB = puntosB + 1

    return puntosA, puntosB

def cambiar_jugador(jugador):
    if jugador == "A":
        return "B"
    return "A"

def fin_juego(tab):
    
    for x in tab:
        for y in x:
            if y == 1 or y == '1':
                return False
    return True

def crear_tablero(renglones, columnas):
    tablero = []
    for x in range(renglones):
        c = []

        for i in range(columnas):
            c.append('.')

            if i == columnas - 1:
                pass
            else:
                c.append(1)

        tablero.append(c)

        c = []

        if x == renglones - 1:
            return tablero

        for i in range(columnas):
            if i == 0:
                c.append(1)
            elif int(i) % 2 == 0:
                c.append(1)
            else:
                c.append(1)

            if i == columnas - 1:
                pass
            else:
                c.append(' ')

        tablero.append(c)

    return tablero

def cuadrado(tab, player):
    hit = False
    for x in range(0, len(tab), 2):
        for y in range(0, len(tab[x]), 2):
            try:

                if tab[x][y + 1] != 1 \
                        and tab[x + 1][y] != 1 \
                        and tab[x + 1][y + 2] != 1 \
                        and tab[x + 2][y + 1] != 1 \
                        and tab[x][y + 1] != '1' \
                        and tab[x + 1][y] != '1' \
                        and tab[x + 1][y + 2] != '1' \
                        and tab[x + 2][y + 1] != '1':
                    if tab[x + 1][y + 1] == " ":
                        tab[x + 1][y + 1] = player
                        hit = True
            except:
                pass

    return tab, hit

def imprimir_tablero(tab):

    print(" ", end = " ")
    
    for x in range(len(tab[0])):
        if x % 2 != 0:
            print(" ", end = " ")
        else:
            print(x // 2, end = " ")
    print()

    cont = 0

    for linea in tab:
        if cont % 2 != 0:
            print(" ", end = " ")
        else:
            print(cont // 2, end = " ")

        for colun in linea:
            if colun == 1 or colun == "1":
                print(" ", end = " ")
            else:
                print(colun, end = " ")
        print()
        cont = cont + 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    print("Tablero Dots and Boxes:")
    arranca(5,5)
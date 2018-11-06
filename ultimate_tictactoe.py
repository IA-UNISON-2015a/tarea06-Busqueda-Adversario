#!/usr/bin/env python
# coding: utf-8


"""
Juego Ultimate Tic-Tac-Toe, al cual vamos a llamar "MetaGato"

Es una especie de gato de 81 casillas que se juega mucho en el centro de
cómputo de la LCC/UNISON. Básicamente es un gato compuesto de gatos

Las reglas se pueden consultar en
https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe

"""

from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
from busquedas_adversarios import minimax_t
import tkinter as tk


class MetaGato(JuegoSumaCeros2T):
    """
    El juego del Meta gato, en el cual vamos a codificarlo
    como una lista donde cada estado representa un gato diferente.

    La codificación la vamos a realizar como:

    0   1  2     9 10 11    18 19 20
    3   4  5    12 13 14    21 22 23
    6   7  8    15 16 17    24 25 26

    27 28 29    36 37 38    45 46 47
    30 31 32    39 40 41    48 49 50
    33 34 35    42 43 44    51 52 53

    54 55 56    63 64 65    72 73 74
    57 58 59    66 67 68    75 76 77
    60 61 62    69 70 71    78 79 80

    """
    def __init__(self, jugador=1):
        """
        Inicializa el juego del gato

        """
        self.x0 = 81 * [0] + [None]
        self.x = 81 * [0] + [None]
        self.metagato = 9 * [0]
        self.historial = []
        self.jugador = 1

    def jugadas_legales(self):
        gato = self.x[-1]
        if gato is None:
            return range(81)
        if self.metagato[gato] == 0 and 0 in self.x[gato*9: gato*9+9]:
            return [i for i in range(9*gato, 9*gato + 9) if self.x[i] == 0]
        return ([i for i in range(81) if self.x[i] == 0 and
                    self.metagato[i//9] == 0])

    def terminal(self):
        if 0 not in self.x:
            return 0
        gato = self.historial[-1][1]

        x = self.x[9 * gato: 9 * gato + 9]
        if self.metagato[gato] == 0:
            self.metagato[gato] = self.final_gato(x)
        res = self.final_gato(self.metagato)
        return None if res == 0 else res

    # Supongo que final_gato dictamina si hay metagato
    # Si hay empate, regresa 2. Es lo que se conoce como "lo gano el gato"
    @staticmethod
    def final_gato(x):
        if x[4] != 0 and (x[0] == x[4] == x[8] or x[2] == x[4] == x[6]):
            return x[4]
        for i in range(3):
            if x[3 * i] != 0 and x[3 * i] == x[3 * i + 1] == x[3 * i + 2]:
                return x[3 * i]
            if x[i] != 0 and x[i] == x[i + 3] == x[i + 6]:
                return x[i]
        if all(a != 0 for a in x):
            return 2
        return 0

    def hacer_jugada(self, jugada):
        if self.x[-1] is None:
            self.x[-1] = jugada // 9
        self.historial.append((jugada, jugada//9))
        self.x[jugada] = self.jugador
        self.x[-1] = jugada % 9
        self.jugador *= -1


    def deshacer_jugada(self):
        jugada, gato = self.historial.pop()
        self.x[jugada] = 0
        self.x[-1] = gato
        self.jugador *= -1
        self.deshacer_meta()

    def deshacer_meta(self):
        l = []
        for i in range(9):
            l.append(self.final_gato(self.x[i*9:i*9+9]))
            if l[i] != self.metagato[i]:
                self.metagato[i] = l[i]

    def semifinal_gato(self, x, j):
        for i in range(9):
            #manera medio bonita de checar si hay semifinal con la de en medio
            if x[4] == j and x[8 - i] == x[4] and i != 4 and x[i] == 0:
                return x[4]

            # Checa verticalmente
            if x[i] == j and ((x[(i + 3) % 9] == x[i] or x[(i + 6) % 9] == x[i])
                and (x[(i + 3) % 9] == 0 or x[(i + 6) % 9] == 0)):
                return x[i]
        #Checo horizontalmente
        for i in [0,3,6]:
            if x[i] == j and ((x[i + 1] == x[i] or x[i + 2] == x[i])
                and (x[i + 1] == 0 or x[i + 2] == 0)):
                return x[i]
            if x[i + 1] == j and ((x[i + 1] == x[i] or x[i + 1] == x[i + 2])
                and (x[i] == 0 or x[i + 2] == 0)):
                return x[i]
            if x[i + 2] == j and ((x[i + 2] == x[i + 1] or x[i + 2] == x[i])
                and (x[i + 1] == 0 or x[i] == 0)):
                return x[i]
        return 0

def utilidad_uttt(juego):
    """
    Resultados y comentarios generales de esta funcion de utilidad:

    Con una profundidad igual a 4 y dando el primer turno a la IA, no vimos
    que perdiera ni una sola vez. Probe esta madre en el centro de computo
    con alrededor de 10 personas y dos lograron empatarla. En el caso de que
    no empiece ella, yo logre ganarle 1 vez, y las demas veces perdi.

    Es bastante curioso hacer este juego con minimax, ya que los malos movim-
    ientos no afectan bastante al arbol que se hace en minimax.

    Con profundidad igual a 3 tambien nos gana, pero es mucho mas rapida.
    Si se llegara a optimizar aun mas, podriamos dejarla en 4 para que sea el
    nivel mas complicado. Por eso recomiendo dejarla en 3.

    @param juego: objeto juego del gato. Es necesario ya que necesitamos informa
    cion del juego, como el jugador en turno, los metagatos, etc. Si yo
    la optimizara, haria que los semifinal_gato sean atributos del objeto
    juego, para no tener que calcularlos.

    @return: una utilidad entre 0 y 1
    """
    #sf es semi finales
    mal_mov = 0
    if juego.metagato[juego.x[-1]] != 0:
        mal_mov = -1 * juego.jugador

    sf_circ = [0 for _ in range(9)]
    sf_equis = sf_circ[:]
    for i in range(9):
        sf_equis[i] = juego.semifinal_gato(juego.x[9 * i: 9 * i + 9], 1)
        sf_circ[i] = juego.semifinal_gato(juego.x[9 * i: 9 * i + 9], -1)
    st_equis = juego.semifinal_gato(juego.metagato, 1)
    st_circ = juego.semifinal_gato(juego.metagato, -1)

    return ((3 * sum(juego.metagato) + mal_mov + sum(sf_circ) + sum(sf_equis) +
        5 * st_circ + 5 * st_equis + juego.x[40])/100)
class MetaGatoTK:
    def __init__(self, escala=1):

        self.app = app = tk.Tk()
        self.app.title("El juego del meta gato")
        self.L = L = int(escala) * 50

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
        gatos = [None for _ in range(9)]
        self.tablero = [None for _ in range(81)]
        self.textos = [None for _ in range(81)]
        letra = ('Helvetica', -int(0.9 * L), 'bold')

        for meta in range(9):
            gatos[meta] = tk.Frame(ctn, bg='black', borderwidth=3)
            gatos[meta].grid(row=meta // 3, column=meta % 3)

            for i in range(9):
                ind = meta * 9 + i
                self.tablero[ind] = tk.Canvas(
                    gatos[meta], height=L, width=L,
                    bg='light grey', borderwidth=0
                )
                self.textos[ind] = self.tablero[ind].create_text(
                    L // 2, L // 2, font=letra, text=' '
                )
                self.tablero[ind].grid(row=i // 3, column=i % 3)
                self.tablero[ind].val = 0
                self.tablero[ind].pos = ind

    def jugar(self, primero):
        juego = MetaGato()
        self.actualiza_tablero(juego.x)

        if not primero:
            jugada = minimax(juego, dmax=0, utilidad=utilidad_uttt)
            juego.deshacer_meta()
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)

        self.anuncio['text'] = "A ver de que cuero salen más correas"
        for _ in range(81):
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)
            ganador = juego.terminal()
            if ganador is not None:
                break
            # Profundidad 3: tiempos muy buenos en todos los escenarios
            # Profundidad 4: tiempos buenos en la mayoria de los escenarios.
            # cuando hay muchos gatos ganados, y muchas jugadas legales
            # puede tardarse hasta 5 seg en una computadora "estandar"
            jugada = minimax(juego, dmax=3, utilidad=utilidad_uttt)
            juego.deshacer_meta()
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(juego.x)
            ganador = juego.terminal()
            if ganador is not None:
                break

        finstr = ("UN ASQUEROSO EMPATE, aggggg" if ganador == 2 else
                  "Ganaste, bye"
                  if (ganador == 1 and primero) or (ganador < 0 and not primero)
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
        for i in range(81):
            if self.tablero[i].val != x[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text=' xo'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    MetaGatoTK().arranca()

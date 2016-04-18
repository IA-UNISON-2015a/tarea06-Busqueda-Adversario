import juegos_cuadricula
import time

class JuegoInventado(juegos_cuadricula.Juego2ZT):
    
    def __init__(self):
        juegos_cuadricula.Juego2ZT.__init__(self, 0,0,None)
    
    def jugadas_legales(self, estado, jugador):
        m = [
            [1,2],      #0
            [3,4],      #1
            [5,6,7],    #2
            [8,9,10],   #3
            [11,12],    #4
            [13],       #5
            [14,15],    #6
            [],         #7
            [16,17],    #8
            [18,19],    #9
            [20,21],    #10
            [],         #11
            [22,23],    #12
            [24,25,26], #13
            [7],        #14
        ] + ([[]] * 13) #15-27
        
        return m[estado]
        
    def estado_terminal(self, estado):
        t = {
            7: 30,
            11: -3,
            15: 0,
            16: 16,
            17: 32,
            18: 11,
            19: -2,
            20: 13,
            21: -37,
            22: 99,
            23: 5,
            24: 2,
            25: -2,
            26: -6,
            27: 7 
        }
        if estado not in t:
            return None
            
        return t[estado]
        
    def hacer_jugada(self, estado, jugada, jugador):
        return jugada
        
class JugadorInventado(juegos_cuadricula.JugadorNegamax):
    
    
    def ordena(self, juego, estado, jugadas, jugador):
        return jugadas
        
    def utilidad(self, juego, estado):
        return 0
        
    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        self.jugador = jugador
        self.tiempo = 4
        self.maxima_d = 6
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego,
                                     estado,
                                     juego.jugadas_legales(estado, jugador),
                                     -jugador),
                         key=lambda jugada: self.negamax(juego,
                                                          estado=juego.hacer_jugada(estado, jugada, jugador),
                                                          jugador=-jugador,
                                                          alpha=-1e10,
                                                          beta=1e10,
                                                          profundidad=self.dmax))
            print "A profundad ", self.dmax, " la mejor jugada es ", jugada
            self.dmax += 1
        return jugada
        
if __name__ == '__main__':
    print JugadorInventado().decide_jugada(JuegoInventado(),
        0, 1, None)
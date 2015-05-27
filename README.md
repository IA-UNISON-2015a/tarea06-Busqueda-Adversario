# Tarea 6: Búsquedas con adversarios

**Fecha de entrega: 23 de mayo de 2015**

## Objetivos

1. Reforzar los conocimientos de los métodos de búsquedas por adversarios, en particular 
   el algoritmo Minimax con poda alpha-beta en su versión para dos jugadores por turnos, conocida 
   como `negamax`.

2. Desarrollar habilidades para establecer heurísticas de ordenamiento de jugadas con el fin de reducr los
   tiempos de búsqueda.
   
3. Desarrollar habilidades y conocimientos para establecer medidas de estimación de utilidad, al aprender a 
   generar funciones de características y establecer pesos entre estos.
   
4. Desarrollar un juego simple (Othello) con motor de IA desde cero.

Adicionalmente, en los programas se intenta mostrar un punto de vista más orientado al paradigma funcional en Python,
utilizando a las clases únicamente como contenedores de funciones para un tipo de datos particulares (el juego).

Si bien se proporcionan las herramientas y ejemplos necesarios para comprender los rudimentos básicos de programación 
de interfases en TCL, de ninguna manera se considera como un conocimiento práctico adicional que se espera
reforzar con la tarea.

## Instrucciones

1. En el archivo `juegos_cuadricula.py` se ofrecen clases para juego de tablero por turnos, interfase gráfica, jugador
   humano y jugador minimax. Revisa el código y procura entender a grandes razgos como funciona. El archivo `gato.py`
   es un ejemplo de uso sencillo con el juego del gato. Es importante aclarar que este es un ejemplo con fines didácticos y 
   toda posible optimización en tiempo o uso dememoria se evitó siempre que eso implicara obscurecer el proceso de
   búsqueda con adversarios, por lo que el entorno es bastante ineficiente en estos términos.
   
2. En el archivo `conecta4.py` se incluye el juego de conecta 4, el cual es bastante conocido, y si quieres información
   de como se juega la puedes consultar [aqui](http://en.wikipedia.org/wiki/Connect_Four). En el archivo se ofrece el 
   juego programado, así como un agente computacional que utiliza una búsqueda por profundidad iterativa en un periodo 
   de tiempo finito. Esto con el fin de reducir los tiempo de espera y hacer el algoritmo más cercano a un algoritmo
   que se emplee de forma práctica. Dentro de la clase `JugadorConecta4` se tiene el método `ordena`, el cual solamente
   reacomoda las jugadas legales al azar. Desarrolla tu propio mñetodo con el fin de lograr mejores búsquedas a mayor
   profundidad (20 puntos).

   Listo.
   
3. En el mismo archivo `juegos_cuadricula.py` y el mismo método `JugadorConecta4` se tiene el método `utilidad` en 
   el cual por el momento la utilidad se calcula asignando un valor de 1 (-1 respectivamente) si un estado es terminal
   y gana el jugador 1 (-1 respectivamente), mientras que en cualquier otro caso responde un 0 (total ignorancia). 
   Desarrolla tu porpio método de utilidad. Para esto posiblemente tendras que desarrollar varias funciones de 
   características, y devolver como utilidad una combinacion lineal de estas, tal como vimos en clases (20 puntos).

   Listo.
   
4. El archivo `othello.py` es un archivo completamente en blanco. Desarrolla todo lo necesario para un juego de 
   [Othello](http://en.wikipedia.org/wiki/Reversi). Todas las decisiones son tuyas. No importa que juegue lento,
   pero que el ordenamiento y las funciones de utilidad hagan que jugar contra el motor de IA sea muy dificil de
   ganar (60 puntos).

   Aun no termino :/
   
   

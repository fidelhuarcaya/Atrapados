from math import inf as infinity
from random import choice
import platform
import time
from os import system


humano = -1
computador = +1
tablero = [
    [-1, 1, 2, 3, 4,5,-2],
    [-1, 1, 2, 3, 4,5,-2]
    
]


def evaluar(estado):
    """
   Función para la evaluación heurística del estado.
    : param estado: el estado del tablero actual
    : retorna: +1 si el computadoruter ganador; -1 si el ganador humano; 0 empate
    """
    if ganador(estado, computador):
        puntuacion = +1
    elif ganador(estado, humano):
        puntuacion = -1
    else:
        puntuacion = 0

    return puntuacion


def ganador(estado, jugador):
    """
    Esta función prueba si un jugador específico gana. Posibilidades:
    * Gana computador si las fichas están en los casilleros 6 y 13
    * Gana computador si las fichas están en los casilleros 2 y 9 """
    estado_ganador = [
        [estado[0][1], estado[1][1]],
    ]
    if [jugador, jugador] in estado_ganador:
        return True
    else:
        return False


def fin_juego(estado):
    """
     Esta función prueba si gana el humano o la computadora
    : param state: el estado de la placa actual
    : return: Verdadero si gana el humano o la computadora
    """
    return ganador(estado, humano) or ganador(estado, computador)


def casillas_vacias(estado):
    """
    Cada casillero vacía se agregará a la lista de celdas
    : estado: el estado de la placa actual
    : return: una lista de celdas vacías
    """
    cells = []

    for x, row in enumerar(estado):
        for y, cell in enumerar(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def movimiento_valido(x, y):
    """
     Un movimiento es válido si la celda elegida está vacía
    : param x: coordenada X
    : param y: coordenada Y
    : return: Verdadero si el tablero [x] [y] está vacío
    """
    if [x, y] in casillas_vacias(tablero):
        return True
    else:
        return False


def mover_ficha(x, y, jugador):
    """
    Establecer el movimiento a bordo, si las coordenadas son válidas
    : param x: coordenada X
    : param y: coordenada Y
    : param player: el jugador actual
    """
    if movimiento_valido(x, y):
        tablero[x][y] = jugador
        return True
    else:
        return False


"""def minimax(self, estado, jugador):
       if(self.ganador()):
            self.mostrarGanador()
        else:
            movimiento = -1
            puntuacion = -2
            pos = random.randint(1, 14)
            print("Aleatorio: ", pos)
            if(self.movimiento_valido(pos)):
                return pos
            else:
                return self.minimax(estado, jugador)"""
#Función de IA que elige el mejor movimiento

def minimax(estado, profundidad, jugador):   
    if jugador == computador:
        mejor = [-1, -1, -infinity]
    else:
        mejor = [-1, -1, +infinity]

    if profundidad == 0 or fin_juego(estado):
        puntuacion = evaluar(estado)
        return [-1, -1, puntuacion]

    for cell in casillas_vacias(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = jugador
        puntuacion = minimax(estado, profundidad - 1, -jugador)
        estado[x][y] = 0
        puntuacion[0], puntuacion[1] = x, y

        if jugador == computador:
            if puntuacion[2] > mejor[2]:
                mejor = puntuacion  # max value
        else:
            if puntuacion[2] < mejor[2]:
                mejor = puntuacion  # min value

    return mejor


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(estado, c_choice, h_choice):
    """
    Print the tablero on console
    :param estado: current estado of the tablero
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in estado:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    Llama a la función minimax si la profundidad <9,
    de lo contrario, elige una coordenada aleatoria.
    :regresar:
    """
    profundidad = len(casillas_vacias(tablero))
    if profundidad == 0 or fin_juego(tablero):
        return

    clean()
    print(f'computadoruter turn [{c_choice}]')
    render(tablero, c_choice, h_choice)

    if profundidad == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(tablero, profundidad, computador)
        x, y = move[0], move[1]

    mover_ficha(x, y, computador)
    time.sleep(1)


def turno_humano(c_choice, h_choice):
    """
     El humano juega eligiendo un movimiento válido.
    """
    profundidad = len(casillas_vacias(tablero))
    if profundidad == 0 or fin_juego(tablero):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'humano turn [{h_choice}]')
    render(tablero, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = mover_ficha(coord[0], coord[1], humano)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeytableroInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    """
    Main function that calls all functions
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if humano is the first

    # humano chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeytableroInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computadoruter's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # humano may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeytableroInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(casillas_vacias(tablero)) > 0 and not fin_juego(tablero):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        turno_humano(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if ganador(tablero, humano):
        clean()
        print(f'humano turn [{h_choice}]')
        render(tablero, c_choice, h_choice)
        print('YOU WIN!')
    elif ganador(tablero, computador):
        clean()
        print(f'computadoruter turn [{c_choice}]')
        render(tablero, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(tablero, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()

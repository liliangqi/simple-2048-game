import numpy as np
import numpy.random as npr
from readchar import readchar
import os


def create_chessboard(size=4):
    """create a new chessboard"""

    board = np.zeros((size, size), dtype=np.int32)
    board = initial_each_step(board)
    shown_board = draw_chessboard(board)
    os.system('clear')
    print(shown_board)

    return board


def initial_each_step(board):
    """select a random position with value 0 and set it to 2 or 4"""

    positions = np.argwhere(board == 0)
    position = positions[npr.choice(positions.shape[0])]
    # initialize with 2 or 4 (in lower probability)
    board[position[0], position[1]] = 2 if npr.choice(100) > 79 else 4

    return board


def next_step(board, direction='up'):
    """step to the next step in the game"""

    board_size = board.shape[0]
    if direction == 'left' or direction == 'right':
        board = board.T

    for i in range(board_size):
        column = board[:, i]
        addition_result = []
        if direction == 'down' or direction == 'right':
            column = column[::-1]

        # remove zeros in a column
        column = np.delete(column, np.where(column == 0))
        j = 0
        while j < len(column)-1:
            if column[j] == column[j+1]:
                addition_result.append(column[j] + column[j+1])
                j += 2
            else:
                addition_result.append(column[j])
                j += 1
        if j == len(column)-1:
            addition_result.append(column[j])

        while len(addition_result) < board_size:
            addition_result.append(0)
        addition_result = np.array(addition_result)
        if direction == 'down' or direction == 'right':
            addition_result = addition_result[::-1]

        board[:, i] = addition_result

    if direction == 'left' or direction == 'right':
        board = board.T

    return board


def able_to_step(board):
    """judge if it is able to go to next step in current chessboard"""

    board_size = board.shape[0]
    flag = False

    if 0 in board:  # if there is 0 in the board, it must be able to continue
        flag = True
    else:
        for i in range(board_size):
            column = board[:, i]
            # judge if there are two adjacent numbers with same value
            for prev, nex in zip(column[:-1], column[1:]):
                if prev == nex:
                    flag = True
                    break
            if flag:
                break

    return flag


def draw_chessboard(board):
    """draw the chessboard"""

    board_size = board.shape[0]
    output = ''

    # draw the emepty chessboard
    for i in range(board_size):
        output += ('+' + '-' * 6) * board_size
        output += '+\n'
        output += ('|' + ' ' * 6) * board_size
        output += '|\n'

    output += ('+' + '-' * 6) * board_size
    output += '+'

    output = list(output)
    x_list, y_list = np.where(board != 0)

    for x, y in zip(x_list, y_list):
        # find the position to fill the non-zero number
        rect_position = (7 * board_size + 2) * (2 * x + 1) + 7 * y + 5
        num = board[x, y]
        while True:
            last_ch = str(num % 10)
            num //= 10
            output[rect_position] = last_ch
            rect_position -= 1

            if num == 0:
                break

    output = ''.join(output)

    return output


chessboard_size = 5
chessboard = create_chessboard(chessboard_size)

# TODO: set scores for the game
keys = 'WASDRQwasdrq'
actions = ['up', 'left', 'down', 'right', 'restart', 'exit']
action_dict = dict(zip(keys, actions * 2))

while 2048 not in chessboard:
    if able_to_step(chessboard) or able_to_step(chessboard.T):
        reminder_message = 'Press a key: WASD to move, R to restart, Q to quit'
        print(reminder_message)
        control_key = readchar()

        if control_key in 'WASDwasd':
            temp = chessboard.copy()  # need a slice rather than reference
            chessboard = next_step(chessboard, action_dict[control_key])
            if not (chessboard == temp).all():  # if the chessboard is changed
                chessboard = initial_each_step(chessboard)
            shown_board = draw_chessboard(chessboard)
            os.system('clear')
            print(shown_board)

        elif control_key in 'Rr':
            chessboard = create_chessboard(chessboard_size)

        elif control_key in 'Qq':
            print('Bye~')
            break

        else:
            continue
    else:
        print('Gameover. Press R to restart, or Q to quit.')
        if readchar() in 'Rr':
            chessboard = create_chessboard(chessboard_size)
        elif readchar() in 'Qq':
            print('Bye~')
            break
        else:
            continue

if 2048 in chessboard:
    os.system('clear')
    shown_board = draw_chessboard(chessboard)
    print(shown_board)
    print('Congratulations! You win!')

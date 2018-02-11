import numpy as np
import numpy.random as npr
from readchar import readchar


def initial_each_step(board):
    """select a random position with value 0 and set it to 2"""

    board_size = board.shape[0]
    choice_range_list = []
    x_list, y_list = np.where(board == 0)
    for x, y in zip(x_list, y_list):
        choice_range_list.append(x * board_size + y)

    position = npr.choice(choice_range_list)
    position_x = position // board_size
    position_y = position % board_size
    # TODO: initialize with 4 in lower probability
    board[position_x, position_y] = 2

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


chessboard_size = 4
chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int32)
chessboard = initial_each_step(chessboard)

current_score = 0

print(chessboard)

# do not consider restarting now
while True:
    control_key = readchar()

    if control_key == 'w' or control_key == 'W': 
        temp = chessboard.copy()  # need a slice rather than reference
        chessboard = next_step(chessboard, 'up')
        if not (chessboard == temp).all():
            chessboard = initial_each_step(chessboard)
        print(chessboard)

    elif control_key == 's' or control_key == 'S': 
        temp = chessboard.copy()
        chessboard = next_step(chessboard, 'down')
        if not (chessboard == temp).all():
            chessboard = initial_each_step(chessboard)
        print(chessboard)

    elif control_key == 'a' or control_key == 'A': 
        temp = chessboard.copy()
        chessboard = next_step(chessboard, 'left')
        if not (chessboard == temp).all():
            chessboard = initial_each_step(chessboard)
        print(chessboard)

    elif control_key == 'd' or control_key == 'D': 
        temp = chessboard.copy()
        chessboard = next_step(chessboard, 'right')
        if not (chessboard == temp).all():
            chessboard = initial_each_step(chessboard)
        print(chessboard)

    else:
        break

print('Done')




















def momentum_heuristic(board, turn):
    """
    Uses the 'Momentum' method to work out the heuristic values.

    The 'Momentum' method works by identifying patterns that have not been blocked by an opponent and therefore
    that the opponent must respond to or risk losing the game. If a pattern is only blocked on one end, half
    points are awarded when calculating the heuristic.

    :param board: a Pente game board
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: current board, heuristic score
    """
    XXXX_points = 20 # In effect, this score is 30 since having an unblocked 4 also means you have an unblocked 3
    XXX_points = 10
    X0X_points = 3

    opp = 3 - turn
    tot = 0
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == turn:
                for dir in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    num_blocking = 0
                    try:
                        if board[row - (1 * dir[0])][column - (1 * dir[1])] == opp:
                            num_blocking += 1
                        elif row - (1 * dir[0]) < 0 or column - (1 * dir[1]) < 0:
                            num_blocking += 1
                    except IndexError:
                        num_blocking += 1
                    try:
                        if (board[row + (1 * dir[0])][column + (1 * dir[1])] == turn and
                                board[row + (2 * dir[0])][column + (2 * dir[1])] == turn and
                                board[row + (3 * dir[0])][column + (3 * dir[1])] == turn):
                            try:
                                if board[row + (4 * dir[0])][column + (4 * dir[1])] == opp:
                                    num_blocking += 1
                            except IndexError:
                                num_blocking += 1

                            if num_blocking == 0:
                                tot += XXXX_points
                            elif num_blocking == 1:
                                tot += XXXX_points / 2
                            continue
                    except IndexError:
                        pass
                    try:
                        if (board[row + (1 * dir[0])][column + (1 * dir[1])] == turn and
                              board[row + (2 * dir[0])][column + (2 * dir[1])] == turn):
                            try:
                                if board[row + (3 * dir[0])][column + (3 * dir[1])] == opp:
                                    num_blocking += 1
                            except IndexError:
                                num_blocking += 1

                            if num_blocking == 0:
                                tot += XXX_points
                            elif num_blocking == 1:
                                tot += XXX_points / 2
                            continue
                    except IndexError:
                        continue
                    try:
                        if board[row + (2 * dir[0])][column + (2 * dir[1])] == turn:
                            try:
                                if board[row + (3 * dir[0])][column + (3 * dir[1])] == opp:
                                    num_blocking += 1
                            except IndexError:
                                num_blocking += 1

                            if num_blocking == 0:
                                tot += X0X_points
                            elif num_blocking == 1:
                                tot += X0X_points / 2
                            continue
                    except IndexError:
                        continue

    return board, tot


if __name__ == '__main__':
    board = [[0, 0, 0, 0, 1, 0, 1],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0]]

    print(momentum_heuristic(board, 1)[1])

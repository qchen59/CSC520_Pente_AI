import copy
import numpy as np


def calculate_heuristic(board, turn):
    """
    Detects streaks (consecutive placements of stones) for the given turn. Then sets the heuristic values of the nodes
    that surrounds the streaks. Following are the possible heuristic values, their interpretations, and some examples in
    the x axis. Same examples are valid for any direction (4 axes in total) in the board. Star signs (*) in the examples
    represent streaks/already placed stones.

    # 6 - adjacent to a streak of four  (6 * * * * 6), (3 * 6 * * * 5)
    # 5 - adjacent to a streak of three (5 * * * 5), (4 * * 5 * 3)
    # 4 - adjacent to a streak of two   (4 * * 4), (3 * 4 * 3)
    # 3 - adjacent to a streak of one   (3 * 3)

    Notes: Uncomment the 'for' loop at line 73 if you want to take a look at an overview of the calculated heuristic
           values. Number '1' and '2' represents the stone placements of each player. Number from 3-6 represents
           heuristic values for the given turn.

    :param board: a Pente game board from an ongoing game (must not be a finished game)
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: the coordinates of the maximum heuristic value (best position to place the piece).
    """

    size = len(board)
    heuristics = copy.deepcopy(board)
    opponent = 2 if turn == 1 else 1                                       # Getting the opponent
    values = {6: 4, 5: 3, 4: 2, 3: 1, 0: 0}                                # Heuristics to streak mapping
    streaks = {4: 6, 3: 5, 2: 4, 1: 3, 0: 0}                               # Streaks to heuristics mapping

    for i in range(size):
        for j in range(size):
            if board[i][j] == turn:
                for axis in [(1, 0), (0, 1), (1, 1), (1, -1)]:             # Four axes that we consider
                    count = 3                                              # To count the streak
                    for k in range(1, 5):
                        row_change = k * axis[0]
                        col_change = k * axis[1]

                        if 0 <= i + row_change < size and 0 <= j + col_change < size:
                            node = board[i + row_change][j + col_change]
                            if node == turn:
                                count += 1
                                continue
                            break
                        break

                    # Setting the heuristic value of the node that is adjacent to the streak from the left side
                    if i - axis[0] >= 0 and j - axis[1] >= 0:
                        left_node = heuristics[i - axis[0]][j - axis[1]]
                        if left_node != turn and left_node != opponent and left_node == 0:
                            heuristics[i - axis[0]][j - axis[1]] = count
                        elif left_node != turn and left_node != opponent and i - 2 * axis[0] >= 0 and j - 2 * axis[1] >= 0:
                            if heuristics[i - 2 * axis[0]][j - 2 * axis[1]] == turn:
                                streak = values[heuristics[i - axis[0]][j - axis[1]]] + values[count]
                                try:
                                    heuristics[i - axis[0]][j - axis[1]] = streaks[streak]
                                except KeyError:
                                    print("The game has already finished")
                                    exit(-1)
                        elif left_node != turn and left_node != opponent and left_node < count:
                            heuristics[i - axis[0]][j - axis[1]] = count + (left_node % 2)

                    # Setting the heuristic value of the node that is adjacent to the streak from the right side
                    if i + row_change < size and j + col_change < size:
                        right_node = heuristics[i + row_change][j + col_change]
                        if right_node != turn and right_node != opponent and right_node == 0:
                            heuristics[i + row_change][j + col_change] = count
                        elif right_node != turn and right_node != opponent and right_node < count:
                            heuristics[i + row_change][j + col_change] = count + (right_node % 2)

    # print("Heuristic")
    # for i in heuristics:
    #     print(*i, sep=' ')

    max_index = np.where(heuristics == np.amax(heuristics))
    return list(zip(max_index[0], max_index[1]))[0]

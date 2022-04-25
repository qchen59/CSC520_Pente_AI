import copy
import math


def calculate_streaks(board, turn):
    """
    Detects streaks (consecutive placements of stones) for the given board and turn. Outputs a score based on how ideal
    a position is for the next placement, based on the current streaks.

    a node adjacent to a streak of 0 is given a score of 0.
    a node adjacent to a streak of 1 is given a score of 3.
    a node adjacent to a streak of 2 is given a score of 4.
    a node adjacent to a streak of 3 is given a score of 5.
    a node adjacent to a streak of 4 is given a score of 6.

    Final output is the total of all heuristic values.


    :param board: a Pente game board
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: current board, board with heuristic values, and a score that is calculated based on the heuristic
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
                    if 0 <= i - axis[0] < size and 0 <= j - axis[1] < size:
                        left_node = heuristics[i - axis[0]][j - axis[1]]
                        if left_node != turn and left_node != opponent and left_node == 0:
                            heuristics[i - axis[0]][j - axis[1]] = count
                        elif left_node != turn and left_node != opponent and 0 <= i - 2 * axis[0] < size and 0 <= j - 2 * axis[1] < size:
                            if heuristics[i - 2 * axis[0]][j - 2 * axis[1]] == turn:
                                streak = values[heuristics[i - axis[0]][j - axis[1]]] + values[count]
                                if streak > 4:
                                    streak = 4
                                heuristics[i - axis[0]][j - axis[1]] = streaks[streak]
                        elif left_node != turn and left_node != opponent and left_node < count:
                            if count + (left_node % 2) > 6:
                                heuristics[i - axis[0]][j - axis[1]] = count
                            else:
                                heuristics[i - axis[0]][j - axis[1]] = count + (left_node % 2)

                    # Setting the heuristic value of the node that is adjacent to the streak from the right side
                    if 0 <= i + row_change < size and 0 <= j + col_change < size:
                        right_node = heuristics[i + row_change][j + col_change]
                        if right_node != turn and right_node != opponent and right_node == 0:
                            heuristics[i + row_change][j + col_change] = count
                        elif right_node != turn and right_node != opponent and right_node < count:
                            if count + (right_node % 2) > 6:
                                heuristics[i + row_change][j + col_change] = count
                            else:
                                heuristics[i + row_change][j + col_change] = count + (right_node % 2)

    # print("Heuristics")
    # for i in heuristics:
    #     print(*i, sep=' ')

    score = 0
    for i in range(size):
        for j in range(size):
            if heuristics[i][j] > 2:
                score += heuristics[i][j]
    return board, heuristics, score


def mid_control_streaks(board, turn):
    """
    Uses the 'calculate_streaks' method to work out the heuristic values. Then if there are streaks around the middle
    of the board, the final score is bumped up.

    :param board: a Pente game board
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: current board, board with heuristic values, and a score that is calculated based on the heuristic
    """
    board, heuristics, score = calculate_streaks(board, turn)
    size = len(board)

    if size < 6:                                               # No point calculating this heuristic for smaller boards
        return board, heuristics, score

    mid = math.ceil(size / 2)                                  # Getting the middle point of the board

    for i in range(mid - 3, mid + 2):
        for j in range(mid - 3, mid + 2):
            if heuristics[i][j] > 2:                           # Doubling the score of the heuristic values that are in
                score += 2 * heuristics[i][j]                  # the middle of the board.

    return board, heuristics, score


def mid_control_pieces(board, turn):
    """
    Calculates a heuristic score based on the placements around the middle of the board. For every turn's piece the
    score is increased by one. For every opponents piece, the score is decreased by one.

    :param board: a Pente game board
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: current board and a score that is calculated based on the heuristic
    """
    size = len(board)
    opponent = 2 if turn == 1 else 1                           # Getting the opponent
    mid = math.ceil(size / 2)                                  # Getting the middle point of the board
    score = 0

    for i in range(mid - 3, mid + 2):
        for j in range(mid - 3, mid + 2):
            if board[i][j] == turn:
                score += 1
            elif board[i][j] == opponent:
                score -= 1
    return board, score

import ConsecutivePieces as Cp
import math
import copy


def mid_control_streaks(board, turn):
    """
    Uses the 'calculate_streaks' method to work out the heuristic values. Then the heuristic values of the pieces that
    are in the middle 5x5 area of the board is doubled. This will bumped up the final score as well.

    :param board: a Pente game board
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: current board, board with heuristic values, and a score that is calculated based on the heuristic
    """
    board, heuristics, score = Cp.calculate_streaks(board, turn)
    size = len(board)

    if size < 6:                                               # No point calculating this heuristic for smaller boards
        return board, heuristics, score

    mid = math.ceil(size / 2)                                  # Getting the middle point of the board

    for i in range(mid - 3, mid + 2):
        for j in range(mid - 3, mid + 2):
            if heuristics[i][j] > 2:                           # Doubling the score of the heuristic values that are in
                heuristics[i][j] = 2 * heuristics[i][j]        # the middle of the board.

    score = 0
    for i in range(size):
        for j in range(size):
            if heuristics[i][j] > 2:
                score += heuristics[i][j]
    return board, heuristics, score


def mid_control_pieces(board, turn):
    """
    Calculates a heuristic score based on the placements inside the middle 5x5 area of the board. For every turn's piece
    the score is increased by one. For every opponents piece, the score is decreased by one.

    Each node adjacent to a turn player's piece, will get a heuristic value of either 3 or 6. If the piece is inside the
    middle 5x5 area the value is 6. Otherwise 3.

    :param board: a Pente game board
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is wanting to place a piece

    :return: current board, board with heuristic values, and a score that is calculated based on the heuristic
    """
    size = len(board)
    heuristics = copy.deepcopy(board)
    opponent = 2 if turn == 1 else 1                           # Getting the opponent
    mid = math.ceil(size / 2)                                  # Getting the middle point of the board
    score = 0

    # Calculating heuristics of the middle 5x5 area
    for i in range(mid - 3, mid + 2):
        for j in range(mid - 3, mid + 2):
            if board[i][j] == turn:
                score += 1
                for axis in [(1, 0), (0, 1), (1, 1), (1, -1)]:                      # Four axes that we consider
                    if mid - 3 <= i - axis[0] < mid + 2 and mid - 3 <= j - axis[1] < mid + 2:
                        node = board[i - axis[0]][j - axis[1]]
                        if node != turn and node != opponent:
                            heuristics[i - axis[0]][j - axis[1]] = 6
                    if mid - 3 <= i + axis[0] < mid + 2 and mid - 3 <= j + axis[1] < mid + 2:
                        node = board[i + axis[0]][j + axis[1]]
                        if node != turn and node != opponent:
                            heuristics[i + axis[0]][j + axis[1]] = 6
            elif board[i][j] == opponent:
                score -= 1

    # Calculating heuristics of the rest of the board
    for i in range(size):
        for j in range(size):
            if mid - 3 <= i < mid + 2 or mid - 3 <= j < mid + 2:
                continue
            if board[i][j] == turn:
                for axis in [(1, 0), (0, 1), (1, 1), (1, -1)]:                      # Four axes that we consider
                    if 0 <= i - axis[0] < size and 0 <= j - axis[1] < size:
                        node = board[i - axis[0]][j - axis[1]]
                        if node != turn and node != opponent:
                            heuristics[i - axis[0]][j - axis[1]] = 3
                    if 0 <= i + axis[0] < size + 2 and 0 <= j + axis[1] < size:
                        node = board[i + axis[0]][j + axis[1]]
                        if node != turn and node != opponent:
                            heuristics[i + axis[0]][j + axis[1]] = 3

    return board, heuristics, score

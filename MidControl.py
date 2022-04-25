import ConsecutivePieces as Cp
import math


def mid_control_streaks(board, turn):
    """
    Uses the 'calculate_streaks' method to work out the heuristic values. Then if there are streaks around the middle
    of the board, the final score is bumped up.

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
    return score

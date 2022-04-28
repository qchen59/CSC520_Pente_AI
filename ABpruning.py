import math
import sys
import pente
import copy
import ConsecutivePieces
import timeit
import CapturedPieces
import MidControl
import Momentum

sys.setrecursionlimit(15000)
pinfi = sys.maxsize
ninfi = -sys.maxsize

# 1 -- ConsecutivePieces
# 2 -- CapturedPieces
# 3 -- mid_control_pieces
# 4 -- mid_control_streaks
# 5 -- Momentum
# 6 -- ConsecutivePieces + CapturedPieces
# 7 -- Momentum + CapturedPieces
# 8 -- ConsecutivePieces + mid_control_pieces
# 9 -- Momentum + mid_control_pieces
# 10 -- mid_control_streaks + mid_control_pieces
numberOfHeuristic = 5
bigDepth = 4
Combinations = {
    1: {1: 1, 2: 1, 3: "player 1 -- ConsecutivePieces, player 2 -- ConsecutivePieces"},
    2: {1: 1, 2: 2, 3: "player 1 -- ConsecutivePieces, player 2 -- CapturedPieces"},
    3: {1: 1, 2: 3, 3: "player 1 -- ConsecutivePieces, player 2 -- mid_control_pieces"},
    4: {1: 1, 2: 4, 3: "player 1 -- ConsecutivePieces, player 2 -- mid_control_streaks"},
    5: {1: 1, 2: 5, 3: "player 1 -- ConsecutivePieces, player 2 -- Momentum"},
    6: {1: 1, 2: 6, 3: "player 1 -- ConsecutivePieces, player 2 -- ConsecutivePieces + CapturedPieces"},
    7: {1: 1, 2: 7, 3: "player 1 -- ConsecutivePieces, player 2 -- Momentum + CapturedPieces"},
    8: {1: 1, 2: 8, 3: "player 1 -- ConsecutivePieces, player 2 -- ConsecutivePieces + mid_control_pieces"},
    9: {1: 1, 2: 9, 3: "player 1 -- ConsecutivePieces, player 2 -- Momentum + mid_control_pieces"},
    10: {1: 1, 2: 10, 3: "player 1 -- ConsecutivePieces, player 2 -- mid_control_streaks + mid_control_pieces"},
}
names = {
    1: "ConsecutivePieces",
    2: "CapturedPieces",
    3: "mid_control_pieces",
    4: "mid_control_streaks",
    5: "Momentum",
    6: "ConsecutivePieces + CapturedPieces",
    7: "Momentum + CapturedPieces",
    8: "ConsecutivePieces + mid_control_pieces",
    9: "Momentum + mid_control_pieces",
    10: "mid_control_streaks + mid_control_pieces",
}


# Board object to implement
class Board:
    """
    Construct a board object for implementation

    :param board: a Pente game board
    :param status: the status of win, 1 for player 1 wins and 2 for player 2 wins
    :param moves: a list of all previous moves [ [row, col] ... ]
    """
    board = []
    status = 0
    captures = [0, 0]
    moves = []

    # initialize the board
    def __init__(self, size, board=None):
        self.board = pente.make_board(size)
        if board != None:
            for i in range(len(board.board)):
                for j in range(len(board.board[0])):
                    self.board[i][j] = board.board[i][j]

    def getEmptyPositions(self):
        """
        Get all empty positons on the board
        :return: all empty positions with cols and rows
        """
        emptyPosition = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    emptyPosition.append([i, j])
        return emptyPosition

    def performMove(self, p, player):
        """
        Call the pente game to perform a move
        :param p: the position of move that we want to perform
        :param playerNo: the player that perform the move, either 1 or 2
        """
        captures = [0, 0]
        # (game, captures, 1, 0, 6)
        game, captures, win = pente.update_board(self.board, captures, player, p[0], p[1])
        self.board = game
        self.status = win
        self.captures = captures

    def printBoard(self):
        pente.print_board(self.board)


# 1 -- ConsecutivePieces
# 2 -- CapturedPieces
# 3 -- mid_control_pieces
# 4 -- mid_control_streaks
# 5 -- Momentum
# 6 -- ConsecutivePieces + CapturedPieces
# 7 -- Momentum + CapturedPieces
# 8 -- ConsecutivePieces + mid_control_pieces
# 9 -- Momentum + mid_control_pieces
# 10 -- mid_control_streaks + mid_control_pieces
def getHeu(board, player, capturess):
    """
    Helper method for selecting heuristic.

    :param board: a board object
    :param player: either 1 or 2, the current player
    :param capturess: a list of how many stones are captured

    :return: current board, board with heuristic values, and a score that is calculated based on the heuristic
    """

    global numberOfHeuristic
    if numberOfHeuristic == 1:  # 1 -- ConsecutivePieces
        return ConsecutivePieces.calculate_streaks(board, player)
    elif numberOfHeuristic == 2:  # 2 -- CapturedPieces
        return CapturedPieces.captured_pieces(board, capturess, player)
    elif numberOfHeuristic == 3:  # 3 -- mid_control_pieces
        return MidControl.mid_control_pieces(board, player)
    elif numberOfHeuristic == 4:  # 4 -- mid_control_streaks
        return MidControl.mid_control_streaks(board, player)
    elif numberOfHeuristic == 5:  # 5 -- Momentum
        tboard, score = Momentum.momentum_heuristic(board, player)
        heuristics = tboard
        return tboard, heuristics, score
    elif numberOfHeuristic == 6:  # 6 -- ConsecutivePieces + CapturedPieces
        tboard, heuristics, score = ConsecutivePieces.calculate_streaks(board, player)
        tboard, heuristics, score1 = CapturedPieces.captured_pieces(board, capturess, player)
        return tboard, heuristics, score1 + score
    elif numberOfHeuristic == 7:  # 7 -- Momentum + CapturedPieces
        tboard, score = Momentum.momentum_heuristic(board, player)
        tboard, heuristics, score1 = CapturedPieces.captured_pieces(board, capturess, player)
        return tboard, heuristics, score1 + score
    elif numberOfHeuristic == 8:  # 8 -- ConsecutivePieces + mid_control_pieces
        tboard, heuristics, score = ConsecutivePieces.calculate_streaks(board, player)
        tboard, heuristics, score1 = MidControl.mid_control_pieces(board, player)
        return tboard, heuristics, score1 + score
    elif numberOfHeuristic == 9:  # 9 -- Momentum + mid_control_pieces
        tboard, score = Momentum.momentum_heuristic(board, player)
        tboard, heuristics, score1 = MidControl.mid_control_pieces(board, player)
        return tboard, heuristics, score1 + score
    elif numberOfHeuristic == 10:  # 10 -- mid_control_streaks + mid_control_pieces
        tboard, heuristics, score = MidControl.mid_control_streaks(board, player)
        tboard, heuristics, score1 = MidControl.mid_control_pieces(board, player)
        return tboard, heuristics, score1 + score


def minmax(depth, board, maximizingPlayer, player, alpha, beta, size):
    """
    The implementation of the alpha beta pruning.

    :param depth: Current depth of the search
    :param board: a board object
    :param maximizingPlayer: a boolean to decide go max or go min. True for max and False for min.
    :param player: either 1 or 2, the current player for the algorithm.
    :param alpha: alpha variable for alpha beta pruning
    :param beta: beta variable for alpha beta pruning

    :return: heuristic score, board object
    """
    global bigDepth
    # Terminate conditions
    if depth == bigDepth:  # The depth of alpha beta
        tboard, heuristics, score = getHeu(board.board, player, board.captures)
        # print(score)
        return score, board

    # someone wins end and return
    if board.status != 0:
        if board.status == player:
            # player wins
            score = pinfi
        else:
            # opponent wins
            score = ninfi
        return score, board

    childArray = board.getEmptyPositions()
    if len(childArray) == 0:
        tboard, heuristics, score = getHeu(board.board, player, board.captures)
        return score, board

    # Max
    if maximizingPlayer:
        best = ninfi
        for a in childArray:
            temp = Board(size, board)
            temp.captures = copy.deepcopy(board.captures)
            temp.performMove(a, player)
            temp.moves = copy.deepcopy(board.moves)
            temp.moves.append({'player': player, 'move': a})
            val, board2 = minmax(depth + 1, temp, False, player, alpha, beta, size)
            if val > best:
                best = val
                result = board2
                alpha = max(alpha, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best, result
    # Min
    else:
        best = pinfi
        childArray = board.getEmptyPositions()
        for a in childArray:
            temp = Board(size, board)
            temp.captures = copy.deepcopy(board.captures)
            temp.performMove(a, 3 - player)
            temp.moves = copy.deepcopy(board.moves)
            temp.moves.append({'player': 3 - player, 'move': a})
            val, board2 = minmax(depth + 1, temp, True, player, alpha, beta, size)
            if val < best:
                best = val
                result = board2
                beta = min(beta, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best, result


def performGame(heur1, heur2, boardSize):
    """
    The implementation of the alpha beta pruning.

    :param heur1: the heuristic for the first player, can be 1 - 10(see the numberOfHeuristic variable)
    :param heur2: the heuristic for the second player, can be 1 - 10(see the numberOfHeuristic variable)
    :param boardSize: the size for the pente board(x by x)

    :return: 1 if player 1 wins or 2 if player 2 wins, board of the final round
    """

    # Assign the heuristics
    global numberOfHeuristic
    # performGame between two heuristics
    game = pente.make_board(boardSize)
    player = 1
    i = 0
    captures = [0, 0]

    # Place the first stone at the middle
    # print(i)
    i += 1
    # print('player ', player)
    middle = math.floor(boardSize / 2)
    move = [middle, middle]
    # print('move', move)
    numberOfHeuristic = heur1
    game, captures, win = pente.update_board(game, captures, player, move[0], move[1])
    # print('captures', captures)
    player = 3 - player
    # pente.print_board(game)

    board = Board(boardSize)
    board.board = game

    while True:
        # print(i)
        i += 1
        # print('player ', player)
        # Player 1
        if i % 2 != 0:
            numberOfHeuristic = heur1
            v, result = minmax(0, board, True, player, ninfi, pinfi, boardSize)
        # Player 2
        else:
            numberOfHeuristic = heur2
            v, result = minmax(0, board, True, player, ninfi, pinfi, boardSize)
        # board.printBoard()
        move = result.moves[0]['move']
        # print('move', move)
        game, captures, win = pente.update_board(game, captures, player, move[0], move[1])
        # print('captures', captures)
        # pente.print_board(game)
        # board, heuristics, score = AdjacentPieces.calculate_heuristic(game, 3 - player)
        # print('sc', heuristics)
        if win != 0:
            # print(win, "win!!!!!")
            # print(numberOfHeuristic)
            return win, game
        player = 3 - player
        board = Board(boardSize)
        board.board = game
        board.captures = copy.deepcopy(captures)


if __name__ == '__main__':
    for i in range(1, 11):
        print("======================================================================")
        win, game = performGame(1, i, 11)  # Player 1's Heuristic unchanged
        print(str(i) + ". " + Combinations[i][3] + "| Winner: Player " + str(win))
        pente.print_board(game)
        print()
        win, game = performGame(i, 1, 11)  # Player 2's Heuristic unchanged
        print("   Player 1 -- " + names[i] + ", player 2 -- ConsecutivePieces| Winner: Player " + str(win))
        pente.print_board(game)
        print()

    # performGame(1, 1, 7)

import sys
import pente
import copy
import ConsecutivePieces
import timeit

sys.setrecursionlimit(15000)
pinfi = sys.maxsize
ninfi = -sys.maxsize
# Change here to change the heuristic
# 1 -- ConsecutivePieces
numberOfHeuristic = 1

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
    moves = []

    # initialize a 7x7 board
    def __init__(self, board = None):
        self.board = pente.make_board(7)
        if board != None:
            for i in range(len(board.board)):
                for j in range(len(board.board[0])):
                    self.board[i][j] = board.board[i][j]

    def getEmptyPositions(self):
        emptyPosition = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    emptyPosition.append([i, j])
        return emptyPosition

    def performMove(self, p, player):
        captures = [0, 0]
        # (game, captures, 1, 0, 6)
        game, captures, win = pente.update_board(self.board, captures, player, p[0], p[1])
        self.board = game
        self.status = win

    def printBoard(self):
        pente.print_board(self.board)


# class State:
#     board = Board()
#     playerNo = 0
#
#     def __init__(self, state=None):
#         if state is not None:
#             self.board = Board(state.board)
#             self.playerNo = state.playerNo
#
#     def togglePlayer(self):
#         self.playerNo = 3 - self.playerNo
#
#     def getOpponent(self):
#         return 3 - self.playerNo
#
#     def getAllPossibleStates(self):
#         # constructs a list of all possible states from current state
#         possibleStates = []
#         availablePosition = self.board.getEmptyPositions()
#         for p in availablePosition:
#             newState = State()
#             newState.board = Board(self.board)
#             newState.playerNo = 3 - self.playerNo
#             newState.board.performMove(p, newState.playerNo)
#             possibleStates.append(newState)
#         return possibleStates


# class Node:
#     state = State()
#     parent = None
#     childArray = []
#
#     def __init__(self, node=None):
#         if node is not None:
#             self.state = copy.deepcopy(node.state)
#             self.parent = copy.deepcopy(node.parent)
#             self.childArray = copy.deepcopy(node.childArray)

def getHeu(board, tempplayer):
    global numberOfHeuristic
    if numberOfHeuristic == 1:
        return ConsecutivePieces.calculate_streaks(board, tempplayer)
    else:
        raise Exception("GG")


def minmax(depth, board, maximizingPlayer, player, alpha, beta, preboard, move):
    # print("-------------")
    # board.printBoard()
    # Terminating condition. One player win
    if maximizingPlayer:
        tempplayer = player
    else:
        tempplayer = 3 - player
    if depth == 3:
        tboard, heuristics, score = getHeu(board.board, tempplayer)
        # print('player', tempplayer, heuristics[move[0]][move[1]], board.board)
        return score, board

    if board.status != 0:
        # print('win')
        tboard, heuristics, score = getHeu(board.board, tempplayer)
        return score, board

    childArray = board.getEmptyPositions()
    if len(childArray) == 0:
        tboard, heuristics, score = getHeu(board.board, tempplayer)
        return score, board

    # Max
    if maximizingPlayer:
        numberOfHeuristic = 3
        best = ninfi
        for a in childArray:
            temp = Board(board)
            temp.performMove(a, player)
            temp.moves = copy.deepcopy(board.moves)
            temp.moves.append({'player': player, 'move': a})
            val, board2 = minmax(depth + 1, temp, False, player, alpha, beta, board, a)
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
            temp = Board(board)
            temp.performMove(a, 3 - player)
            temp.moves = copy.deepcopy(board.moves)
            temp.moves.append({'player': 3 - player, 'move': a})
            val, board2 = minmax(depth + 1, temp, True, player, alpha, beta, board, a)
            if val < best:
                best = val
                result = board2
                beta = min(beta, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best, result


if __name__ == '__main__':
    tik=timeit.default_timer()
    board = Board()
    player = 1
    move = [0,0]
    win = 0
    while win == 0:
        print('player ', player)
        v, result = minmax(0, board, True, player,ninfi, pinfi, board, move)
        # print('result', result.moves)
        result.printBoard()
        move = result.moves[0]['move']
        print('move', move)
        captures = [0, 0]
        # (game, captures, 1, 0, 6)
        board.board, captures, win = pente.update_board(board.board, captures, player, move[0], move[1])
        # print('captures', captures)
        pente.print_board(board.board)
        player = 3 - player
    tok=timeit.default_timer()
    print(win, "win!!!!!")
    print('end')
    print("Processing time: ", tok - tik)
    print(numberOfHeuristic)


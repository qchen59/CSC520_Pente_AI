import math
import copy
import ABpruning
import MCTS
import pente
import sys

pinfi = sys.maxsize
ninfi = -sys.maxsize

def performGame(heur1, heur2, boardSize):
    """
    The implementation of the alpha beta pruning.

    :param heur1: the heuristic for the first player, can be 1 - 10(see the numberOfHeuristic variable)
    :param heur2: the heuristic for the second player, can be 1 - 10(see the numberOfHeuristic variable)
    :param boardSize: the size for the pente board(x by x)

    :return: 1 if player 1 wins or 2 if player 2 wins, board of the final round
    """

    # performGame between two heuristics
    game = pente.make_board(boardSize)
    player = 1
    i = 0
    captures = [0, 0]

    mcts = MCTS.MCTS(boardSize)
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

    board = ABpruning.Board()
    board.board = game
    mtboard = MCTS.Board(boardSize)
    mtboard.board = game

    while True:
        # print(i)
        i += 1
        # print('player ', player)
        # Player 1
        if i % 2 != 0:
            ABpruning.numberOfHeuristic = heur1
            # print('he', ABpruning.numberOfHeuristic)
            v, result = ABpruning.minmax(0, board, True, player, ninfi, pinfi)
            move = result.moves[0]['move']
        # Player 2
        else:
            move, board = mcts.findNextMove(board, player, heur2)
        # board.printBoard()
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
        board = ABpruning.Board()
        board.board = game
        board.captures = copy.deepcopy(captures)

        mtboard = MCTS.Board(boardSize)
        mtboard.board = game
        mtboard.captures = copy.deepcopy(captures)


def performGameS(heur1, heur2, boardSize):
    """
    The implementation of the alpha beta pruning.

    :param heur1: the heuristic for the first player, can be 1 - 10(see the numberOfHeuristic variable)
    :param heur2: the heuristic for the second player, can be 1 - 10(see the numberOfHeuristic variable)
    :param boardSize: the size for the pente board(x by x)

    :return: 1 if player 1 wins or 2 if player 2 wins, board of the final round
    """

    # performGame between two heuristics
    game = pente.make_board(boardSize)
    player = 1
    i = 0
    captures = [0, 0]

    mcts = MCTS.MCTS(boardSize)
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

    board = ABpruning.Board()
    board.board = game
    mtboard = MCTS.Board(boardSize)
    mtboard.board = game

    while True:
        # print(i)
        i += 1
        # print('player ', player)
        # Player 1
        if i % 2 != 0:
            move, board = mcts.findNextMove(board, player, heur1)
        # Player 2
        else:
            ABpruning.numberOfHeuristic = heur2
            # print('he', ABpruning.numberOfHeuristic)
            v, result = ABpruning.minmax(0, board, True, player, ninfi, pinfi)
            move = result.moves[0]['move']
        # board.printBoard()
        # print('move', move)
        game, captures, win = pente.update_board(game, captures, player, move[0], move[1])
        # print('captures', captures)
        # pente.print_board(game)
        # print('sc', heuristics)
        if win != 0:
            # print(win, "win!!!!!")
            # print(numberOfHeuristic)
            return win, game
        player = 3 - player
        board = ABpruning.Board()
        board.board = game
        board.captures = copy.deepcopy(captures)

        mtboard = MCTS.Board(boardSize)
        mtboard.board = game
        mtboard.captures = copy.deepcopy(captures)

if __name__ == '__main__':

    abList = [2, 3]
    mctsList = ['conP',  'cpc', 'mc']
    for h in abList:
        print(h)
        tw = 0
        for hh in mctsList:
            print(hh)
            p1 = [0, 0]
            p2 = [0, 0]
            for i in range(5):
                # ab first
                win, game = performGame(h, hh, 11)
                if win == 1:
                    p1[0] = p1[0] + 1
                if win == 2:
                    p1[1] = p1[1] + 1
                # mcts first
                win, game = performGameS(hh, h, 11)
                if win == 1:
                    p2[0] = p2[0] + 1
                if win == 2:
                    p2[1] = p2[1] + 1
            print(p1, p2)
    # h is ab
    # for h in abList:
    #     print(h)
    #     tw = 0
    #     for hh in mctsList:
    #         hw = 0
    #         if hh != h:
    #             win = performGame(h, hh, 11)
    #             # AB player 1 and MCTS player 2
    #             print('win', win)
    #         print('      ', hh, hw)
    #         tw += hw
    #     print('win rate', tw)
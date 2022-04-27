# main function for the Monte Carlo Tree Search
# Refers to the MCTS tutorial: https://www.baeldung.com/java-monte-carlo-tree-search
import math
import random
import sys
import copy
import pente
import ConsecutivePieces
import CapturedPieces
import MidControl
import Momentum
import time

timeout = 0.05

class Board:
    """
    The Board class, hold the board status
    """

    # The 2d array for board
    board = []
    # current status, 0 : in progress, 1 : player 1 win, 2: player 2 win
    status = 0
    # previous move to reach this board
    move = []
    # captures
    captures = [0, 0]


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
        # print('empty', emptyPosition)
        return emptyPosition

    def performMove(self, p, playerNo):
        """
        Call the pente game to perform a move
        :param p: the position of move that we want to perform
        :param playerNo: the player that perform the move, either 1 or 2
        """
        captures = [0, 0]
        # (game, captures, 1, 0, 6)
        game, captures, win = pente.update_board(self.board, self.captures, playerNo, p[0], p[1])
        # print('c', captures)
        self.board = game
        self.status = win
        self.move = copy.deepcopy(p)
        self.captures = captures

    def printBoard(self):
        """
        Print the current board for display purpose
        """
        pente.print_board(self.board)


class State:
    """
    The state class for holding current board, and other score information
    """

    # current player
    playerNo = 0
    # visit count of this state
    visitCount = 0
    # win score of this state
    winScore = 0

    def __init__(self, size, state=None):
        self.board = Board(size)
        self.size = size
        if state is not None:
            self.board = Board(state.board)
            self.playerNo = state.playerNo
            self.visitCount = state.visitCount
            self.winScore = state.winScore
            self.captures = copy.deepcopy(state.captures)

    def addH(self, h1, h2):
        # print(h1)
        for i in range(len(h1)):
            for j in range(len(h2)):
                if h1[i][j] != 1 and h1[i][j] != 2:
                    h1[i][j] = h1[i][j] + h2[i][j]
        # print(h1)
        return h1

    def getAllPossibleStates(self):
        """
        Get all possible states based on the current board
        :return: a list of possible states
        """
        # constructs a list of all possible states from current state
        possibleStates = []
        availablePosition = self.board.getEmptyPositions()
        for p in availablePosition:
            newState = State(self.size)
            newState.board = Board(self.size, self.board)
            newState.board.captures = copy.deepcopy(self.board.captures)
            newState.playerNo = 3 - self.playerNo
            newState.board.performMove(p, newState.playerNo)
            possibleStates.append(newState)
        return possibleStates

    def simulatePlay(self, heur):
        """
        Simulate a play by referring to the heuristics
        :param heur: the heuristic function we want to use
        :return:
        """
        # print('------------', self.playerNo, 'captures: ', self.board.captures)
        # self.board.printBoard()
        if heur == 'conP':
            board, heuristics, score = ConsecutivePieces.calculate_streaks(self.board.board, self.playerNo)
        if heur == 'mcs':
            board, heuristics, score = MidControl.mid_control_streaks(self.board.board, self.playerNo)
        if heur == 'mcp':
            board, heuristics, score = MidControl.mid_control_pieces(self.board.board, self.playerNo)
        if heur == 'capP':
            board, heuristics, score = CapturedPieces.captured_pieces(self.board.board, self.board.captures, self.playerNo)
        if heur == 'mom':
            board, heuristics, score = Momentum.MCTS_momentum(self.board.board, self.playerNo)
        if heur == 'cpc':
            board, h1, score = ConsecutivePieces.calculate_streaks(self.board.board, self.playerNo)
            board, h2, score = CapturedPieces.captured_pieces(self.board.board, self.board.captures, self.playerNo)
            heuristics = self.addH(h1, h2)
        if heur == 'mc':
            board, h1, score = Momentum.MCTS_momentum(self.board.board, self.playerNo)
            board, h2, score = CapturedPieces.captured_pieces(self.board.board, self.board.captures, self.playerNo)
            heuristics = self.addH(h1, h2)
        if heur == 'cpp':
            board, h1, score = ConsecutivePieces.calculate_streaks(self.board.board, self.playerNo)
            board, h2, score = MidControl.mid_control_pieces(self.board.board, self.playerNo)
            heuristics = self.addH(h1, h2)
        if heur == 'mp':
            board, h1, score = Momentum.MCTS_momentum(self.board.board, self.playerNo)
            board, h2, score = MidControl.mid_control_pieces(self.board.board, self.playerNo)
            heuristics = self.addH(h1, h2)
        if heur == 'mcsp':
            board, h1, score = MidControl.mid_control_streaks(self.board.board, self.playerNo)
            board, h2, score = MidControl.mid_control_pieces(self.board.board, self.playerNo)
            heuristics = self.addH(h1, h2)

        maxnum = 0
        maxnode = []
        for i in range(len(heuristics)):
            for j in range(len(heuristics[0])):
                if heuristics[i][j] > maxnum and heuristics[i][j] != 1 and heuristics[i][j] != 2:
                    maxnum = heuristics[i][j]
                    maxnode = [i, j]
        if len(maxnode) > 0:
            self.board.performMove(maxnode, self.playerNo)
        else:
            availablePositions = self.board.getEmptyPositions()
            if len(availablePositions) != 0:
                selectRandom = random.randrange(len(availablePositions))
                self.board.performMove(availablePositions[selectRandom], self.playerNo)


    def togglePlayer(self):
        """
        Toggle the player
        """
        self.playerNo = 3 - self.playerNo

    def incrementVisit(self):
        """
        Increase the visit count
        """
        self.visitCount += 1

    def getOpponent(self):
        """
        Get the opponent of current player
        :return: the opponent player
        """
        return 3 - self.playerNo

    def addScore(self, add):
        """
        Add score to the win score
        :param add: the added score
        """
        self.winScore += add


class Node:
    """
    The node class to hold the state
    """

    # The parent of this node
    parent = None
    # Children of this node
    childArray = []

    def __init__(self, size, node=None):
        self.state = State(size)
        if node is not None:
            self.state = copy.deepcopy(node.state)
            self.parent = copy.deepcopy(node.parent)
            self.childArray = copy.deepcopy(node.childArray)

    def getRandomChildNode(self):
        """
        Get a random child node
        :return: a random child node of current node
        """
        selectRandom = random.randrange(len(self.childArray))
        return self.childArray[selectRandom]

    def printNode(self):
        """
        Pint a node, for debug purpose
        """
        self.state.board.printBoard()
        print('child', len(self.childArray))

    def getChildWithMaxScore(self):
        """
        Get the child of the max visit count of current node
        :return: child of the max visit count
        """
        children = []
        for c in self.childArray:
            # print('child', c.state.board.board)
            children.append({'count': c.state.visitCount, 'n': c})
        children = sorted(children, key=lambda d: d['count'], reverse=True)
        return children[0]['n']


class MCTS:
    """
    The MCTS class
    """
    # The opponent
    opponent = 0
    # board size
    size = 7

    def __init__(self, size):
        self.size = size
        self.root = Node(self.size)

    def selectPromisingNode(self, rootNode):
        """
        Get the best leaf with the best UCT score
        :param rootNode: the root node
        :return: the best leaf node
        """
        node = rootNode
        # print('rt - pr', node.state.board.board)
        # print('rt - pr', len(node.childArray))
        #
        while len(node.childArray) != 0:
            # print('count', len(node.childArray))
            node = bestUCT(node)
        return node

    def expandNode(self, node):
        '''
        Expand the current node with all possible states
        :param node: Given node
        '''
        possibleStates = node.state.getAllPossibleStates()
        for state in possibleStates:
            # print(state.board.board)
            newNode = Node(self.size)
            newNode.state = state
            newNode.parent = node
            newNode.state.playerNo = node.state.getOpponent()
            newNode.childArray = []
            node.childArray.append(newNode)

    def backPropagation(self, nodeToExplore, playerNo):
        """
        Perform back propagation to add the value back to the nodes
        :param nodeToExplore: the node we explored
        :param playerNo: current player
        """
        tempNode = nodeToExplore
        while tempNode is not None:
            tempNode.state.incrementVisit()
            if tempNode.state.playerNo == playerNo:
                tempNode.state.addScore(10)
            tempNode = tempNode.parent

    def simulatePlayout(self, node, heur):
        """
        Simulate the playout
        :param node: the current node
        :param heur: the heurstic function
        :return: the board status - which player win?
        """
        tempNode = Node(self.size, node)
        tempState = tempNode.state
        boardStatus = tempState.board.status
        if boardStatus == self.opponent:
            tempNode.parent.state.winScore = sys.maxsize
            return boardStatus

        while boardStatus == 0:
            tempState.togglePlayer()
            tempState.simulatePlay(heur)
            boardStatus = tempState.board.status
        return boardStatus

    def findNextMove(self, board, playerNo, heur):
        """
        The main MCTS function, find the next move by the MCTS using selection, expansion, simulation and backpropagation.
        :param board: the current board
        :param playerNo: the current player
        :param heur: the heuristic function we want to use
        :return: the next estimated best move
        """
        # print('input', board.board)
        self.opponent = 3 - playerNo
        # print(playerNo, 'select?', board.board)
        self.root = Node(self.size)
        self.root.childArray = []
        self.root.state.board = copy.deepcopy(board)
        self.root.state.playerNo = self.opponent


        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            # print('simulation ', i)
            # Selection
            promisingNode = self.selectPromisingNode(self.root)
            # print('promising', promisingNode.state.board.board)
            # Expansion
            if promisingNode.state.board.status == 0:
                self.expandNode(promisingNode)

            # print('node')
            # promisingNode.childArray[0].printNode()
            # Simulation
            nodeToExplore = promisingNode
            if len(promisingNode.childArray) > 0:
                nodeToExplore = promisingNode.getRandomChildNode()

            playoutResult = self.simulatePlayout(nodeToExplore, heur)
            # Update
            self.backPropagation(nodeToExplore, playoutResult)
            # print('end', nodeToExplore)
            # print('end', nodeToExplore.childArray[0].childArray)

        winnerNode = self.root.getChildWithMaxScore()
        # print('root', self.root.state.board.board)
        # print('cd', self.root.childArray[0].state.board.board)
        # print('win', winnerNode.state.board.board)
        # self.root = winnerNode
        return winnerNode.state.board.move, winnerNode.state.board


def bestUCT(node):
    '''
    Return the node with the best UCT value in given node's children
    UCT:
    :param node: Given Node
    :return: The node with the best UCT value in given node's children
    '''
    totalVisit = node.state.visitCount
    uctlist = []
    for n in node.childArray:
        nodeVisit = n.state.visitCount
        nodeWinScore = n.state.winScore
        if nodeVisit == 0:
            nodeVisit = 1
        if totalVisit == 0:
            totalVisit = 1
        # print('log', nodeVisit, totalVisit)
        uct = (nodeWinScore / nodeVisit) + 1.41 * math.sqrt(math.log(totalVisit) / nodeVisit)
        uctlist.append({'uct': uct, 'node': n})
    uctlist = sorted(uctlist, key=lambda d: d['uct'], reverse=True)
    return uctlist[0]['node']


def performGame(heur1, heur2, boardSize):
    # performGame between two heuristics

    game = pente.make_board(boardSize)
    player = 1
    mcts = MCTS(boardSize)
    i = 0
    captures = [0, 0]

    # Place the very first at the middle
    # print(i)
    i += 1
    # print('player ', player)
    middle = math.floor(boardSize/2)
    move = [middle, middle]
    # print('move', move)
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
        if i % 2 != 0:
            move, board = mcts.findNextMove(board, player, heur1)
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
            return win
        player = 3 - player
        board = Board(boardSize)
        board.board = game
        board.captures = copy.deepcopy(captures)

def performGametest(heur1, heur2, boardSize):
    # performGame between two heuristics

    game = pente.make_board(boardSize)
    player = 1
    mcts = MCTS(boardSize)
    i = 0
    captures = [0, 0]

    # Place the very first at the middle
    print(i)
    i += 1
    print('player ', player)
    middle = math.floor(boardSize/2)
    move = [middle, middle]
    print('move', move)
    game, captures, win = pente.update_board(game, captures, player, move[0], move[1])
    print('captures', captures)
    player = 3 - player
    pente.print_board(game)

    board = Board(boardSize)
    board.board = game

    while True:
        print(i)
        i += 1
        print('player ', player)
        if i % 2 != 0:
            move, board = mcts.findNextMove(board, player, heur1)
        else:
            move, board = mcts.findNextMove(board, player, heur2)
        print('move', move)
        game, captures, win = pente.update_board(game, captures, player, move[0], move[1])
        print('captures', captures)
        pente.print_board(game)
        if win != 0:
            print(win, "win!!!!!")
            return win
        player = 3 - player
        board = Board(boardSize)
        board.board = game
        board.captures = copy.deepcopy(captures)



if __name__ == '__main__':
    hList = ['conP', 'mcs', 'mcp', 'capP', 'mom', 'cpc', 'mc', 'cpp', 'mp', 'mcsp']
    for h in hList:
        print(h)
        tw = 0
        for hh in hList:
            hw = 0
            if hh != h:
                for i in range(2):
                    win = performGame(h, hh, 11)
                    if win == 1:
                        hw += 1
                for i in range(2):
                    win = performGame(hh, h, 11)
                    if win == 2:
                        hw += 1
            print('      ', hh, hw)
            tw += hw
        print('win rate', tw)

    # performGametest('cpc', 'cpc', 11)





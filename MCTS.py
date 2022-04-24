# main function for the Monte Carlo Tree Search
# Refers to the MCTS tutorial: https://www.baeldung.com/java-monte-carlo-tree-search
import math
import random
import sys
import copy
import pente


class Board:
    board = []
    status = 0

    def __init__(self):
        self.board = pente.make_board(7)

    def getEmptyPositions(self):
        emptyPosition = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    emptyPosition.append([i, j])
        return emptyPosition

    def performMove(self, p, playerNo):
        captures = [0, 0]
        # (game, captures, 1, 0, 6)
        game, captures, win = pente.update_board(self.board, captures, playerNo, p[0], p[1])
        self.board = game
        self.status = win

    def printBoard(self):
        pente.print_board(self.board)


class State:
    board = Board()
    playerNo = 0
    visitCount = 0
    winScore = 0

    def __init__(self, state=None):
        if state is not None:
            self.board = copy.deepcopy(state.board)
            self.playerNo = state.playerNo
            self.visitCount = state.visitCount
            self.winScore = state.winScore

    def getAllPossibleStates(self):
        # constructs a list of all possible states from current state
        possibleStates = []
        availablePosition = self.board.getEmptyPositions()
        for p in availablePosition:
            newState = State()
            newState.board = copy.deepcopy(self.board)
            newState.playerNo = 3 - self.playerNo
            newState.board.performMove(p, newState.playerNo)
            possibleStates.append(newState)
        return possibleStates

    def randomPlay(self):
        # get a list of all possible positions on the board and play a random move
        availablePositions = self.board.getEmptyPositions()
        selectRandom = random.randrange(0, len(availablePositions))
        self.board.performMove(availablePositions[selectRandom], self.playerNo)

    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo

    def incrementVisit(self):
        self.visitCount += 1

    def getOpponent(self):
        return 3 - self.playerNo

    def addScore(self, add):
        self.winScore += add


class Node:
    state = State()
    parent = None
    childArray = []

    def __init__(self, node=None):
        if node is not None:
            self.state = copy.deepcopy(node.state)
            self.parent = copy.deepcopy(node.parent)
            self.childArray = copy.deepcopy(node.childArray)

    def getRandomChildNode(self):
        selectRandom = random.randrange(0, len(self.childArray))
        return self.childArray[selectRandom]

    def printNode(self):
        self.state.board.printBoard()
        print('child', len(self.childArray))

    def getChildWithMaxScore(self):
        children = []
        for c in self.childArray:
            children.append({'count': c.state.visitCount, 'n': c})
        children = sorted(children, key=lambda d: d['count'], reverse=True)
        return children[0]['n']


class MCTS:
    level = 3
    opponent = 0
    root = Node()

    def selectPromisingNode(self, rootNode):
        node = rootNode
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
            newNode = Node()
            newNode.state = state
            newNode.parent = node
            newNode.state.playerNo = node.state.getOpponent()
            newNode.childArray = []
            node.childArray.append(newNode)

    def backPropogation(self, nodeToExplore, playerNo):
        tempNode = nodeToExplore
        while tempNode is not None:
            tempNode.state.incrementVisit()
            if tempNode.state.playerNo == playerNo:
                tempNode.state.addScore(1)
            tempNode = tempNode.parent

    # TODO: update with the heuristic implementation
    def simulateRandomPlayout(self, node):
        tempNode = Node(node)
        tempState = tempNode.state
        boardStatus = tempState.board.status
        if boardStatus == self.opponent:
            tempNode.parent.state.winScore = sys.maxsize
            return boardStatus

        while boardStatus == 0:
            tempState.togglePlayer()
            tempState.randomPlay()
            boardStatus = tempState.board.status
        return boardStatus

    def findNextMove(self, board, playerNo):
        self.opponent = 3 - playerNo
        self.root.state.board = board
        self.root.state.playerNo = self.opponent
        # TODO: define number of loop times or based on given time limitation
        for i in range(3):
            # Slection
            promisingNode = self.selectPromisingNode(self.root)
            print('promising', promisingNode.state.board.printBoard())
            # Expansion
            if promisingNode.state.board.status == 0:
                self.expandNode(promisingNode)
            # print('node')
            # promisingNode.childArray[0].printNode()
            # Simulation
            nodeToExplore = promisingNode
            if len(promisingNode.childArray) > 0:
                nodeToExplore = promisingNode.getRandomChildNode()

            playoutResult = self.simulateRandomPlayout(nodeToExplore)
            # Update
            self.backPropogation(nodeToExplore, playoutResult)
            # print('end', nodeToExplore)
            # print('end', nodeToExplore.childArray[0].childArray)

        winnerNode = self.root.getChildWithMaxScore()
        self.root = winnerNode
        return winnerNode.state.board



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
        if n.state.visitCount == 0:
            uct = sys.maxsize
        else:
            # print('log', nodeVisit, totalVisit)
            uct = (nodeWinScore / nodeVisit) + 1.41 * math.sqrt(math.log(totalVisit) / nodeVisit)
        uctlist.append({'uct': uct, 'node': n})
    uctlist = sorted(uctlist, key=lambda d: d['uct'], reverse=True)
    return uctlist[0]['node']


if __name__ == '__main__':
    board = Board()
    player = 1
    totalMove = 7 * 7
    mcts = MCTS()
    for i in range(totalMove):
        print(i)
        board = mcts.findNextMove(board, player)
        board.printBoard()
        if board.status != 0:
            print(board.status, "win!!!!!")
            break
        player = 3 - player

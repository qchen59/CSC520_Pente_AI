import sys
import pente
import MCTS
import ABpruning
import copy
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QPushButton, QWidget, QSizePolicy, QMessageBox,
    QLineEdit, QFormLayout, QVBoxLayout, QStackedLayout, QComboBox, QHBoxLayout
)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pente")
        # self.setFixedSize(800, 800)
        self.turn = 1
        self.boardSize = 7
        self.game = None
        self.captures = [0, 0]
        self.win = None

        # Layout definitions
        self.mainLayout = QVBoxLayout()
        self.topHorizontal = QHBoxLayout()
        self.grid = QGridLayout()
        self.sizeForm = QFormLayout()
        self.algorithmsDropDown = QStackedLayout()
        self.heuristicsDropDown = QStackedLayout()

        # A form to enter the size
        self.sizeWidget = QLineEdit()
        self.sizeWidget.setText(str(self.boardSize))
        self.sizeForm.addRow("Size:", self.sizeWidget)

        # button to set the size
        self.setSizeButton = QPushButton()
        self.setSizeButton.setFixedSize(QtCore.QSize(56, 28))
        self.setSizeButton.setText("OK")
        self.setSizeButton.clicked.connect(self.set_size)

        # Dropdown definitions for algorithms and heuristics
        self.algorithms = QComboBox()
        self.heuristics = QComboBox()
        self.algorithms.addItems(["Alpha-Beta", "Monte Carlo"])
        self.heuristics.addItems(["Consecutive Pieces", "Mid Control Streaks", "Mid Control Pieces",
                             "Captured Pieces", "Momentum", "Consecutive Pieces + Captured Pieces",
                             "Momentum + Captured Pieces", "Consecutive Pieces + Mid Control Pieces",
                             "Momentum + Mid Control Pieces", "Mid Control Streaks + Mid Control Pieces"])
        self.algorithmsDropDown.addWidget(self.algorithms)
        self.heuristicsDropDown.addWidget(self.heuristics)

        # A popup message to show after a win occur
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Winner Winner Chicken Dinner!")
        self.popup.setStandardButtons(QMessageBox.Retry)
        self.popup.buttonClicked.connect(self.win_popup)

        # Adding widgets to layouts
        self.topHorizontal.addLayout(self.sizeForm)
        self.topHorizontal.addWidget(self.setSizeButton)
        self.topHorizontal.addLayout(self.algorithmsDropDown)
        self.topHorizontal.addLayout(self.heuristicsDropDown)
        self.mainLayout.addLayout(self.topHorizontal)
        self.mainLayout.addLayout(self.grid)

        # Creating the grid and drawing the GUI
        self.create_grid(self.boardSize)
        self.setLayout(self.mainLayout)

        # Creating a pente board, MCTS objects, and AB objects
        self.game = pente.make_board(self.boardSize)
        self.monteCarlo = MCTS.MCTS(self.boardSize)
        self.board = MCTS.Board(self.boardSize)
        self.abBoard = ABpruning.Board(self.boardSize)
        self.heuristicsNames = ["conP", "mcs", "mcp", "capP", "mom", "cpc", "mc", "cpp", "mp", "mcsp"]
        self.pos_inf = sys.maxsize
        self.neg_inf = -sys.maxsize

    def create_grid(self, size):
        """
        Creates the Pente game board with the given size.

        :param size: size of the game board
        """
        for i in range(size):
            for j in range(size):
                button = QPushButton()
                button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                button.setFixedSize(QtCore.QSize(62, 62))
                button.clicked.connect(self.place_stone)
                self.grid.addWidget(button, i, j)

    def set_size(self):
        """
        Deletes the current game board and recreates it with the user entered size.
        """
        size = self.sizeWidget.text()
        self.boardSize = int(size)
        self.win_popup()                       # Calling this as this method does what we want for this scenario as well

    def place_stone(self):
        """
        Placing a stone on the clicked cell.
        """
        print("pressed")
        button = self.sender()
        index = self.grid.indexOf(button)
        position = self.grid.getItemPosition(index)
        row = position[0]
        column = position[1]

        button.setEnabled(False)
        button.setText('1')
        button.setStyleSheet("background-color:#ccd4f2;font-weight: bold;color: #000000;")

        self.game, self.captures, win = pente.update_board(self.game, self.captures, 1, row, column)
        self.check_win(win)
        self.updateBoard(self.game)

        if not self.popup.isVisible():
            algorithm = self.algorithms.currentText()
            heuristic = self.heuristics.currentIndex()

            if algorithm == "Monte Carlo":
                self.board = MCTS.Board(self.boardSize)
                self.board.board = self.game
                self.board.captures = copy.deepcopy(self.captures)
                move, board = self.monteCarlo.findNextMove(self.board, 2, self.heuristicsNames[heuristic])

                ai_row = move[0]
                ai_column = move[1]
                self.game, self.captures, win = pente.update_board(self.game, self.captures, 2, ai_row, ai_column)
                self.check_win(win)

                self.board = MCTS.Board(self.boardSize)
                self.board.board = self.game
                self.board.captures = copy.deepcopy(self.captures)
            elif algorithm == "Alpha-Beta":
                self.abBoard = ABpruning.Board(self.boardSize)
                self.abBoard.board = self.game
                self.abBoard.captures = copy.deepcopy(self.captures)
                ABpruning.numberOfHeuristic = heuristic + 1
                # ABpruning.bigDepth = 4
                value, result = ABpruning.minmax(0, self.abBoard, True, 2, self.neg_inf, self.pos_inf, self.boardSize)
                move = result.moves[0]['move']
                ai_row = move[0]
                ai_column = move[1]
                self.game, self.captures, win = pente.update_board(self.game, self.captures, 2, ai_row, ai_column)
                self.check_win(win)
            else:
                raise Exception("Invalid Algorithm")
            self.updateBoard(self.game)


            ai_button_index = self.boardSize * ai_row + ai_column
            button = self.grid.itemAt(ai_button_index).widget()
            button.setText('2')
            button.setStyleSheet("background-color:#ff8e97;font-weight: bold;color: #000000;")

    def updateBoard(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                ai_button_index = self.boardSize * i + j
                button = self.grid.itemAt(ai_button_index).widget()
                if board[i][j] == 0:
                    button.setEnabled(True)
                    button.setText('')
                    button.setStyleSheet("")
                elif board[i][j] == 1:
                    button.setEnabled(False)
                    button.setText('1')
                    button.setStyleSheet("background-color:#ccd4f2;font-weight: bold;color: #000000;")
                elif board[i][j] == 2:
                    button.setEnabled(False)
                    button.setText('2')
                    button.setStyleSheet("background-color:#ff8e97;font-weight: bold;color: #000000;")



    def check_win(self, win):
        """
        Checks whether a win condition is met. If yes, shows the winner in a pop-up window along with a
        button to play again.

        :param win: an integer indicating either player 1 won,  player 2 won or game still not over.
        """
        if win == 0:
            return
        self.popup.setText("Player " + str(win) + " has won!!!")
        self.popup.show()

    def win_popup(self):
        """
        Runs when a user clicks on 'Retry' after game completion.
        """
        self.clear_layout(self.grid)
        self.game = pente.make_board(self.boardSize)
        self.monteCarlo = MCTS.MCTS(self.boardSize)
        self.board = MCTS.Board(self.boardSize)
        self.abBoard = ABpruning.Board(self.boardSize)
        self.create_grid(self.boardSize)

    def clear_layout(self, layout):
        """
        Clears all elements from an already drawn layout.

        :param layout: the layout that needs elements removed
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

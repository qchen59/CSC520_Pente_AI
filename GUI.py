import sys
import pente
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QPushButton, QWidget, QSizePolicy,
    QLineEdit, QFormLayout, QVBoxLayout, QStackedLayout, QComboBox, QHBoxLayout
)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pente")
        self.setFixedSize(800, 800)
        self.turn = 1
        self.boardSize = 11
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
        algorithms = QComboBox()
        heuristics = QComboBox()
        algorithms.addItems(["Alpha-Beta", "Monte Carlo"])
        heuristics.addItems(["Consecutive Pieces", "Mid Control Streaks", "Mid Control Pieces",
                             "Captured Pieces", "Momentum", "Consecutive Pieces + Captured Pieces",
                             "Momentum + Captured Pieces", "Consecutive Pieces + Mid Control Pieces",
                             "Momentum + Mid Control Pieces", "Mid Control Streaks + Mid Control Pieces"])
        self.algorithmsDropDown.addWidget(algorithms)
        self.heuristicsDropDown.addWidget(heuristics)

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

        self.game = pente.make_board(self.boardSize)

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
        # TODO : Implement this
        print("Not implemented Yet")
        # size = self.sizeWidget.text()
        # self.clearLayout(self.grid)

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
        # button.setText('1')
        #
        # game, captures, win = pente.update_board(self.game, self.captures, 1, row, column)
        # game, captures, win = pente.update_board(self.game, self.captures, 2, 3, 5)

        if self.turn == 1:
            button.setText('1')
            button.setStyleSheet("background-color:#ccd4f2;font-weight: bold;color: #000000;")
            self.turn = 2
        else:
            button.setText('2')
            button.setStyleSheet("background-color:#ff8e97;font-weight: bold;color: #000000;")
            self.turn = 1

    def clear_layout(self, layout):
        """
        Clears all elements from an already drawn layout. This method would come in handy when
        implementing set_size method.

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

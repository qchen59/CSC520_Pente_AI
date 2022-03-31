import copy


def make_board(size):
    # Makes a size by size 2d array filled with 0s
    new_board = []

    for i in range(size):
        new_board.append([])
        for j in range(size):
            new_board[-1].append(0)
    return new_board

def print_board(board):
    # Just prints the board. It expects a 2d array as a board
    for i in board:
        print(*i, sep=' ')

def update_board(curr_board, captures, turn, row, col):
    """
    This function takes a board state and returns the new board state. It accounts for captures.
    :param curr_board: a Board class object (defined above) for the current board
    :param captures: a 2-element list for keeping track of captured pieces. 1st element is player 1, 2nd is player 2
    :param turn: either 1 or 2, depending on if the 1st or 2nd player is placing a piece
    :param row: the row number for the piece being placed
    :param col: the column number for the piece being placed
    :return: The updated board, updated captures, and an integer. The integer is 0 if the game is not over, 1 if
    player 1 won, and 2 if player 2 won.
    """

    board = copy.deepcopy(curr_board)
    captures = captures.copy()

    if board[row][col] == 0:
        # Change piece to players number
        board[row][col] = turn
        size = len(board)

        # Check if the player has made 5 in a row
        for dir in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            count = 0
            for i in range(1, 5):
                row_change = i * dir[0]
                col_change = i * dir[1]
                if 0 <= row + row_change < size and 0 <= col + col_change < size:
                    if board[row + row_change][col + col_change] == turn:
                        count += 1
                    else:
                        break

            for i in range(1, 5):
                row_change = i * dir[0]
                col_change = i * dir[1]
                if 0 <= row + row_change < size and 0 <= col + col_change < size:
                    if board[row - row_change][col - col_change] == turn:
                        count += 1
                    else:
                        break
            if count >= 4:
                return board, captures, turn

        if turn == 1:
            opp = 2
        else:
            opp = 1

        # Check if any pieces were captured, and update the board
        # It also ends the game if 10 pieces have been captured
        # Each tuple in the list is a direction that should be checked
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            try:
                rm = dir[0]  # row multiplier. Always 1, -1, or 0
                cm = dir[1]  # column multiplier. Always 1, -1, or 0
                if board[row + (1 * rm)][col + (1 * cm)] == opp and \
                        board[row + (2 * rm)][col + (2 * cm)] == opp and \
                        board[row + (3 * rm)][col + (3 * cm)] == turn:
                    board[row + (1 * rm)][col + (1 * cm)] = 0
                    board[row + (2 * rm)][col + (2 * cm)] = 0
                    captures[turn - 1] += 2
                    if captures[turn - 1] >= 10:
                        return board, captures, turn
            except IndexError:
                pass

    else:
        raise Exception("Invalid Move")

    return board, captures, 0


# Main function for testing. Current code is just to check if captures work.
if __name__ == '__main__':
    game = make_board(7)
    captures = [0, 0]

    game, captures, win = update_board(game, captures, 1, 0, 0)
    game, captures, win = update_board(game, captures, 2, 1, 1)
    game, captures, win = update_board(game, captures, 2, 2, 2)
    print_board(game)
    print("Captures:", captures)
    print('--------------')
    game, captures, win = update_board(game, captures, 1, 3, 3)
    print_board(game)
    print("Captures:", captures)


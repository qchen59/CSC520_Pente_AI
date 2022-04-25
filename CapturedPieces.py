import copy


def captured_pieces(board, captures, turn):
    size = len(board)
    heuristics = copy.deepcopy(board)
    opponent = 2 if turn == 1 else 1                           # Getting the opponent
    score = 0
    possible_captures_turn = 0
    possible_captures_opponent = 0

    for i in range(size):
        for j in range(size):
            if board[i][j] == turn:
                for axis in [(1, 0), (0, 1), (1, 1), (1, -1)]:                      # Four axes that we consider
                    count = 0
                    for k in range(1, 4):
                        row_change = k * axis[0]
                        col_change = k * axis[1]

                        if 0 <= i + row_change < size and 0 <= j + col_change < size:
                            node = board[i + row_change][j + col_change]
                            if node == opponent and count < 2:
                                count += 1
                                continue
                            elif node != turn and node != opponent and count == 2:
                                possible_captures_turn += 1
                                heuristics[i + row_change][j + col_change] = 3
                            break
                        break
                    for k in range(1, 4):
                        row_change = k * axis[0]
                        col_change = k * axis[1]

                        if 0 <= i - row_change < size and 0 <= j - col_change < size:
                            node = board[i - row_change][j - col_change]
                            if node == opponent and count < 2:
                                count += 1
                                continue
                            elif node != turn and node != opponent and count == 2:
                                possible_captures_turn += 1
                            break
                        break

            if board[i][j] == opponent:
                for axis in [(1, 0), (0, 1), (1, 1), (1, -1)]:                      # Four axes that we consider
                    count = 0
                    for k in range(1, 4):
                        row_change = k * axis[0]
                        col_change = k * axis[1]

                        if 0 <= i + row_change < size and 0 <= j + col_change < size:
                            node = board[i + row_change][j + col_change]
                            if node == turn and count < 2:
                                count += 1
                                continue
                            elif node != turn and node != opponent and count == 2:
                                possible_captures_opponent += 1
                            break
                        break
                    for k in range(1, 4):
                        row_change = k * axis[0]
                        col_change = k * axis[1]

                        if 0 <= i - row_change < size and 0 <= j - col_change < size:
                            node = board[i - row_change][j - col_change]
                            if node == turn and count < 2:
                                count += 1
                                continue
                            elif node != turn and node != opponent and count == 2:
                                possible_captures_turn += 1
                            break
                        break

    score = captures[0] + possible_captures_turn - captures[1] - possible_captures_opponent
    return board, heuristics, score

def generate_chessboard(rows, columns):
    board = ""
    for i in range(rows, 0, -1):
        board += str(i) + " |"
        for j in range(1, columns+1):
            if (i+j) % 2 == 0:
                board += "_|"
            else:
                board += "#|"
        board = board[:-1] + "|"  + "\n"
    board += "  "
    for j in range(1, columns+1):
        board += chr(j+96) + " "
    board = board[:-1]
    return board

print(generate_chessboard(8, 8))

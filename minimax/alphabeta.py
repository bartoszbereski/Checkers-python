from copy import deepcopy

RED = (178, 34, 34)
WHITE = (220, 220, 220)
alpha = float('-inf')
beta = float('inf')


def minimax(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, alpha, beta, False, game)[0]
            max_eval = max(max_eval, evaluation)
            best_move = move if max_eval == evaluation else best_move
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]
            min_eval = min(min_eval, evaluation)
            best_move = move if min_eval == evaluation else best_move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

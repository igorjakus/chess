import chess


def get_king_surroundings(board: chess.Board, color: chess.Color):
    """Zwraca pola wokół króla, w tym pole z królem"""
    king_square = board.pieces(chess.KING, color).pop()
    
    king_file = chess.square_file(king_square)
    king_rank = chess.square_rank(king_square) 
    
    surrounding_squares = []
    
    for rank_offset in [-1, 0, 1]:
        for file_offset in [-1, 0, 1]:
            new_rank = king_rank + rank_offset
            new_file = king_file + file_offset
            
            if 0 <= new_rank <= 7 and 0 <= new_file <= 7:  # pole jest na planszy
                square = chess.square(new_file, new_rank)
                surrounding_squares.append(square)

    return surrounding_squares

def is_attacked_by_pawn(board: chess.Board, square):
    if board.turn == chess.WHITE:
        up_left = 7
        up_right = 9
    else:
        up_left = -9
        up_right = -7

    piece1 = None
    piece2 = None

    if square % 8 != 0:
        if 0 <= square + up_right <= 63:
            piece1 = board.piece_at(square + up_right)
        
    elif square % 8 != 7:
        if 0 <= square + up_right <= 63:
            piece2 = board.piece_at(square + up_left)

    if piece1 is not None and piece1.piece_type == chess.PAWN and piece1.color != board.turn:
        return True
    if piece2 is not None and piece2.piece_type == chess.PAWN and piece2.color != board.turn:
        return True
    return False

def pieces_count(board: chess.Board):
    return chess.popcount(board.occupied)
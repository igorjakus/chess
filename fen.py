import pieces


def fen_to_board(board, fen):
    """Modify list to specific position from FEN notation

    Args:
        board ([ChessBoard list]): basically list with few new methods

        fen ([str]): FEN is the standard chess notation.
        It is used to describe position of chess game
        FEN can be stored in single line string

    Raises:
        Exception: [Print 'ass' in polish on unwanted case]
    """

    if not board:
        board += 64 * [None]

    # True for white color, False for black color
    WHITE = True
    BLACK = False

    i, j = 0, 0
    for char in fen:
        index = 8*j + i
        if char.isalpha():
            if char == 'p':
                board[index] = pieces.Pawn(color=BLACK)
            elif char == 'P':
                board[index] = pieces.Pawn(color=WHITE)

            elif char == 'n':
                board[index] = pieces.Knight(color=BLACK)
            elif char == 'N':
                board[index] = pieces.Knight(color=WHITE)

            elif char == 'b':
                board[index] = pieces.Bishop(color=BLACK)
            elif char == 'B':
                board[index] = pieces.Bishop(color=WHITE)

            elif char == 'r':
                board[index] = pieces.Rook(color=BLACK)
            elif char == 'R':
                board[index] = pieces.Rook(color=WHITE)

            elif char == 'q':
                board[index] = pieces.Queen(color=BLACK)
            elif char == 'Q':
                board[index] = pieces.Queen(color=WHITE)

            elif char == 'k':
                board[index] = pieces.King(color=BLACK)
            elif char == 'K':
                board[index] = pieces.King(color=WHITE)
            i += 1

        elif char == '/':
            j += 1
            i = 0
        elif 1 <= int(char) <= 8:
            for x in range(int(char)):
                board[index] = None
                i += 1
                index = 8*j + i
        else:
            raise Exception("dupa")


def board_to_fen(board):
    i = 0
    fen = ''
    for piece in board:

        if isinstance(piece, pieces.Knight):
            if piece.color:
                fen += 'N'
            else:
                fen += 'n'

        elif isinstance(piece, pieces.Bishop):
            if piece.color:
                fen += 'B'
            else:
                fen += 'b'

        elif isinstance(piece, pieces.Rook):
            if piece.color:
                fen += 'R'
            else:
                fen += 'r'

        elif isinstance(piece, pieces.Queen):
            if piece.color:
                fen += 'Q'
            else:
                fen += 'q'

        elif isinstance(piece, pieces.King):
            if piece.color:
                fen += 'K'
            else:
                fen += 'k'

        elif isinstance(piece, pieces.Pawn):
            if piece.color:
                fen += 'P'
            else:
                fen += 'p'
        else:
            fen += ''
        i += 1
        if i % 8 == 0:
            fen += '/'
    return fen


"""
   A FEN string defines a particular position using only the ASCII characters.
   A FEN string contains six fields separated by a space. The fields are:
   1) Piece placement (from white's perspective). Each rank is described, starting
      with rank 8 and ending with rank 1; within each rank, the contents of each
      square are described from file A through file H. Following the Standard
      Algebraic Notation (SAN), each piece is identified by a single letter taken
      from the standard English names. White pieces are designated using upper-case
      letters ("PNBRQK") while Black take lowercase ("pnbrqk"). Blank squares are
      noted using digits 1 through 8 (the number of blank squares), and "/"
      separates ranks.
   2) Active color. "w" means white moves next, "b" means black.
   3) Castling availability. If neither side can castle, this is "-". Otherwise,
      this has one or more letters: "K" (White can castle kingside), "Q" (White
      can castle queenside), "k" (Black can castle kingside), and/or "q" (Black
      can castle queenside).
   4) En passant target square (in algebraic notation). If there's no en passant
      target square, this is "-". If a pawn has just made a 2-square move, this
      is the position "behind" the pawn. This is recorded regardless of whether
      there is a pawn in position to make an en passant capture.
   5) Halfmove clock. This is the number of halfmoves since the last pawn advance
      or capture. This is used to determine if a draw can be claimed under the
      fifty-move rule.
   6) Fullmove number. The number of the full move. It starts at 1, and is
      incremented after Black's move.
"""

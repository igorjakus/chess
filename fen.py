import pieces


def fen_to_board(fen):
    """Returns list of pieces from FEN position

    Args:
        fen ([str]): [description]

    Raises:
        Exception: [Print 'ass' in polish on unwanted case]

    Returns:
        [list]: FEN is the standard chess notation.
        It is used to describe position of chess game
        FEN can be stored in single line string"""

    board = []
    i, j = 0, 0
    for char in fen:
        if char.isalpha():
            if char == 'p':
                board.append(pieces.Pawn(i, j, is_black=True))
            elif char == 'P':
                board.append(pieces.Pawn(i, j, is_black=False))

            elif char == 'n':
                board.append(pieces.Knight(i, j, is_black=True))
            elif char == 'N':
                board.append(pieces.Knight(i, j, is_black=False))

            elif char == 'b':
                board.append(pieces.Bishop(i, j, is_black=True))
            elif char == 'B':
                board.append(pieces.Bishop(i, j, is_black=False))

            elif char == 'r':
                board.append(pieces.Rook(i, j, is_black=True))
            elif char == 'R':
                board.append(pieces.Rook(i, j, is_black=False))

            elif char == 'q':
                board.append(pieces.Queen(i, j, is_black=True))
            elif char == 'Q':
                board.append(pieces.Queen(i, j, is_black=False))

            elif char == 'k':
                board.append(pieces.King(i, j, is_black=True))
            elif char == 'K':
                board.append(pieces.King(i, j, is_black=False))
            i += 1

        elif char == '/':
            j += 1
            i = 0
        elif 1 <= int(char) <= 8:
            i += int(char)
        else:
            raise Exception("dupa")

    return board

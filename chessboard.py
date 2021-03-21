from fen import fen_to_board


class ChessBoard:
    """ Manage chessboard """
    def __init__(self):
        self._setup_chess_board()
        self._setup_chess_pieces()

    def _setup_chess_board(self):
        self.chess_board = []
        for i in range(8):
            for j in range(8):
                self.chess_board.append(Square(i, j))

    def _setup_chess_pieces(self):
        starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.chess_pieces = fen_to_board(starting_fen)

    def load_fen(self, fen_notation):
        """ Adds pieces objects to pieces list

        Arg: notation ([str]): FEN stored in single line string """

        self.chess_pieces = fen_to_board(fen_notation)

    def flip_board(self):
        for piece in self.chess_pieces:
            piece.rect.x = abs(piece.rect.x - 7*100)
            piece.rect.y = abs(piece.rect.y - 7*100)


class Square():
    """ Represents single square on chessboard """
    def __init__(self, x, y):
        self.is_black = (x + y) % 2 == 1
        self.x = x
        self.y = y

    def position(self):
        return (self.x * 100, self.y * 100)

    def color(self):
        return (125, 135, 150) if self.is_black else (232, 235, 239)

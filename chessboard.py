from fen import fen_to_board


class ChessBoard:
    """ Manage chessboard """
    def __init__(self):
        self._setup_pieces()

    def _setup_pieces(self):
        starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.pieces = fen_to_board(starting_fen)

    def reset_pieces(self):
        starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.pieces = fen_to_board(starting_fen)

    def load_fen(self, fen_notation):
        """ Adds pieces objects to pieces list

        Arg: notation ([str]): FEN stored in single line string """

        self.pieces = fen_to_board(fen_notation)

    def flip_board(self):
        for piece in self.pieces:
            piece.rect.x = abs(piece.rect.x - 7*100)
            piece.rect.y = abs(piece.rect.y - 7*100)

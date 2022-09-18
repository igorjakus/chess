from fen import fen_to_board


class ChessBoard(list):
    """This class is an extended type of list that is initialized
    with starting chess position

    You also can reset it to starting position or load another position
    using a FEN notation"""

    def __init__(self):
        super().__init__()
        self._place_pieces()

    def _place_pieces(self):
        starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        fen_to_board(self, starting_fen)

    def reset(self):
        starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        fen_to_board(self, starting_fen)

    def load_fen(self, fen_notation):
        fen_to_board(self, fen_notation)

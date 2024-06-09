from evaluators.evaluator import Evaluator
import chess


class MaterialEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
   
    def evaluate(self, board : chess.Board):
        """Material-balance based evaluation"""
        cached_value = super().evaluate(board)
        if cached_value is not None:
            return cached_value

        fen = board.fen()
        value = self.material(board)
        self.cache[fen] = value
        return value
    
    @staticmethod
    def material(board : chess.Board):
        """Returns material balance in centipawns
        I found it at chessprogramming.com"""
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return (
            100 * (chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns)) +
            300 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            300 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            500 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            900 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )

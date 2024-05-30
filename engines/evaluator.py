from abc import ABC, abstractmethod
import chess


class Evaluator(ABC):
    WIN_EVALUATION = 10_000  # maximum value for evaluation

    def __init__(self):
        self.cache = dict()
    
    @abstractmethod
    def evaluate(self, board: chess.Board):
        fen = board.fen()
        if fen in self.cache:
            return self.cache[fen]
        
        if board.is_game_over():
            result = board.result()
            if result == '1-0':
                return self.WIN_EVALUATION  # White wins
            elif result == '0-1':
                return -self.WIN_EVALUATION  # Black wins
            else:
                return 0  # Draw
        return None


class MaterialEvaluator(Evaluator):
    def __init__(self):
        super().__init__()

    def material(self, board : chess.Board):
        """Returns material balance
        I found it at chessprogramming.com"""
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return (
            chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
            3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )
   
    def evaluate(self, board : chess.Board):
        """Material-balance based evaluation"""
        cached_value = super().evaluate(board)
        if cached_value is not None:
            return cached_value

        fen = board.fen()
        value = self.material(board)
        self.cache[fen] = value
        return value
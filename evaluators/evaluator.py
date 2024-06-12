from abc import ABC, abstractmethod
import chess


class Evaluator(ABC):
    WIN_EVALUATION = 10_000  # maximum value for evaluation

    def __init__(self):
        self.cache = dict()
    
    @abstractmethod
    def evaluate(self, board: chess.Board):
        """Returns board evaluation in centipawns"""
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

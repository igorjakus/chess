import chess
import chess.engine
from config import Config
from evaluators.material import Evaluator


class StockfishEvaluator(Evaluator):
    STOCKFISH_PATH = Config.STOCKFISH_PATH
 
    def __init__(self, time_limit):
        self.engine = chess.engine.SimpleEngine.popen_uci(self.STOCKFISH_PATH)
        self.time_limit = time_limit
    
    def evaluate(self, board: chess.Board):
        info = self.engine.analyse(board, chess.engine.Limit(time=self.time_limit))
        score = info["score"].white().score(mate_score=self.WIN_EVALUATION)
        return score

    def __del__(self):
        self.engine.quit()

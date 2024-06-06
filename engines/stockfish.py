import chess
import chess.engine
from engines.engine import Engine
from config import Config


class StockfishEngine(Engine):
    TIME_PER_MOVE = Config.STOCKFISH_TIME_PER_MOVE
    PATH = Config.STOCKFISH_PATH

    def __init__(self, board : chess.Board):
        self.engine = chess.engine.SimpleEngine.popen_uci(self.PATH)
        self.board = board

    def play_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(self.TIME_PER_MOVE))
        self.board.push(result.move)

    def __del__(self):
        self.engine.quit()

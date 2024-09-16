import chess
import chess.engine
from config import Config
from engines.engine import Engine


class StockfishEngine(Engine):
    TIME_PER_MOVE = Config.STOCKFISH_TIME_PER_MOVE
    PATH = Config.STOCKFISH_PATH

    def __init__(self, board: chess.Board):
        self.engine = chess.engine.SimpleEngine.popen_uci(self.PATH)
        self.board = board

    def play_move(self):
        if not self.board.is_game_over():
            result = self.engine.play(
                self.board, chess.engine.Limit(self.TIME_PER_MOVE)
            )
            self.board.push(result.move)

    def quit(self):
        self.engine.quit()

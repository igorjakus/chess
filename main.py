import chess
import interface
from engines.random_engine import RandomEngine


class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        self.engine = RandomEngine(self.board)
        self.against_engine = True

    def mode_0(self):
        while not self.board.is_game_over():
            self.ui.player_move()
            self.ui.player_move()

    def mode_1(self):
        while not self.board.is_game_over():
            self.ui.player_move()
            self.engine.play_move()

    def run(self):
        while not self.board.is_game_over():
            self.ui.player_move()
            self.engine.play_move()

if __name__ == "__main__":
    app = App()
    app.run()

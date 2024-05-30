import chess
import interface
from engines.random_engine import RandomEngine


class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        self.engine = RandomEngine(self.board)

    def reset(self):
        self.ui.reset()

    def mode_0(self):
        self.ui.player_move()
        self.ui.player_move()

    def mode_1(self):
        self.ui.player_move()
        self.engine.play_move()
    
    def mode_2(self):
        raise NotImplementedError
        self.engine.play_move()
        self.engine.play_move()
        # need to add displaying moves

    def run(self, mode):
        if mode == 0:
            turn = self.mode_0
        elif mode == 1:
            turn = self.mode_1
        elif mode == 2:
            turn = self.mode_2
        else:
            raise NotImplementedError


        while True:
            while not self.board.is_game_over():
                turn()
            
            while self.board.is_game_over():
                if mode == 2:
                    self.reset()
                else:
                    self.ui.handle_events()

if __name__ == "__main__":
    app = App()
    app.run(mode=1)

import chess
import interface
from random import randint

from engines.random_engine import RandomEngine
from engines.mcts import MCTS


class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        self.engine = RandomEngine(self.board)
        self.engine = MCTS(self.board)

    def reset(self):
        self.ui.reset()

    def mode_0(self):
        # Player vs Player
        self.ui.player_move()
        self.ui.flip()
        self.ui.update_screen()

        self.ui.player_move()
        self.ui.flip()
        self.ui.update_screen()

    def mode_1(self):
        # Player vs AI
        if self.player_starts: 
            self.ui.player_move()
            self.ui.update_screen()

            self.engine.play_move()
            self.ui.update_screen()
        else:
            self.engine.play_move()
            self.ui.update_screen()

            self.ui.player_move()
            self.ui.update_screen()    

    def mode_2(self):
        # AI vs AI
        self.engine.play_move()
        self.ui.update_screen()

        self.engine.play_move()
        self.ui.update_screen()

    def who_first(self):
        self.player_starts = bool(randint(0, 1))
        if not self.player_starts:
            self.ui.flip() 
    
    def run(self, mode):
        if mode == 0:
            turn = self.mode_0
        elif mode == 1:
            turn = self.mode_1
        elif mode == 2:
            turn = self.mode_2
        else:
            raise ValueError("Invalid mode. Please choose 0 (Player vs Player), 1 (Player vs AI), or 2 (AI vs AI).")

        while True:
            if mode == 1:
                self.who_first()
    
            while not self.board.is_game_over():
                turn()
            
            if mode == 2:
                self.reset()
            else:
                self.ui.handle_events()


if __name__ == "__main__":
    app = App()
    app.run(mode=1)

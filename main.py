import chess
import interface
from engines.random import RandomEngine
# from engines.mcts import MCTS

class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        self.engine = RandomEngine(self.board)
        # self.engine = MCTS(self.board)
        self.player_starts = True

    def reset(self):
        self.ui.reset()

    def player_vs_player(self):
        for _ in range(2):
            self.ui.player_move()
            self.ui.flip()
            self.ui.update_screen()

    def player_vs_ai(self):
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

    def ai_vs_ai(self):
        for _ in range(2):
            self.engine.play_move()
            self.ui.update_screen()

    def switch_player(self):
        self.player_starts = not self.player_starts
        self.ui.flip()

    def run(self, mode):
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid mode. Please choose 0 (Player vs Player), 1 (Player vs AI), or 2 (AI vs AI).")
        
        mode_actions = {
            0: self.player_vs_player,
            1: self.player_vs_ai,
            2: self.ai_vs_ai
        }

        while True:
            while not self.board.is_game_over():
                mode_actions[mode]()
            
            if mode == 1:
                self.switch_player()

            elif mode == 2:
                self.reset()
            
            # bug: trzeba osobna funkcje ktora handluje eventy jak sie skonczy gra
            self.ui.handle_events()

if __name__ == "__main__":
    app = App()
    app.run(mode=1)

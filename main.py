import sys
import chess
import interface
from engines.random import RandomEngine
from engines.mcts import MCTS_Engine
from engines.stockfish import StockfishEngine


class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        # self.engine = RandomEngine(self.board)
        # self.engine = MCTS_Engine(self.board)
        self.engine = StockfishEngine(self.board)
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

    def quit(self):
        self.engine.quit()
        sys.exit()

    def run(self):
        try:
            mode = self.ui.handle_gameover()
        
            if mode not in [1, 2, 3]:
                raise ValueError("Invalid mode. Please choose 0 (Player vs Player), 1 (Player vs AI), or 2 (AI vs AI).")
            
            mode_actions = {
                1: self.player_vs_player,
                2: self.player_vs_ai,
                3: self.ai_vs_ai
            }

            while True:
                while not self.board.is_game_over():
                    mode_actions[mode]()
                
                if mode == 2:
                    self.switch_player()
                
                mode = self.ui.handle_gameover()
    
        except SystemExit:
            self.quit()
        

if __name__ == "__main__":
    app = App()
    app.run()

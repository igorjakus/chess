import sys

import chess
import ui.interface as interface
from config import Config
from engines.mcts import MCTSEngine
from engines.negamax import NegamaxEngine
from engines.random import RandomEngine
from engines.stockfish import StockfishEngine


class App:
    """ Main class of the App"""
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        self.__init_engine()
        self.player_starts = True

    def __init_engine(self):
        """Init main and secondary engine (for engines battle)"""
        main_engine = Config.ENGINE
        if main_engine == "stockfish":
            self.engine = StockfishEngine(self.board)
        elif main_engine == "mcts":
            self.engine = MCTSEngine(self.board)
        elif main_engine == "random":
            self.engine = RandomEngine(self.board)
        elif main_engine == "negamax":
            self.engine = NegamaxEngine(self.board)
        else:
            raise IndexError("Wrong engine in config.py!")

        secondary_engine = Config.SECONDARY_ENGINE
        if secondary_engine == "stockfish":
            self.second_engine = StockfishEngine(self.board)
        elif secondary_engine == "mcts":
            self.second_engine = MCTSEngine(self.board)
        elif secondary_engine == "random":
            self.second_engine = RandomEngine(self.board)
        elif secondary_engine == "negamax":
            self.second_engine = NegamaxEngine(self.board)
        else:
            raise IndexError("Wrong engine in config.py!")

    def reset(self):
        """Reset app"""
        self.ui.reset()

    def player_vs_player(self):
        """One turn in PvP"""
        for _ in range(2):
            self.ui.player_move()
            self.ui.flip()
            self.ui.update_screen()

    def player_vs_ai(self):
        """One turn in PvE"""
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
        """One turn in EvE"""
        self.engine.play_move()
        self.ui.update_screen()

        self.second_engine.play_move()
        self.ui.update_screen()

    def switch_player(self):
        """Switch player that starts, flip board"""
        self.player_starts = not self.player_starts
        self.ui.flip()

    def quit(self):
        """Safely quit the application"""
        self.engine.quit()
        sys.exit()

    def run(self):
        """Run main loop"""
        mode_actions = {
            1: self.player_vs_player,
            2: self.player_vs_ai,
            3: self.ai_vs_ai
        }

        try:
            mode = self.ui.handle_init()
            
            while True:
                while not self.board.is_game_over():
                    mode_actions[mode]()
                
                mode = self.ui.handle_game_over()
                if mode == 2:
                    self.switch_player()
    
        except SystemExit:
            self.quit()
        

if __name__ == "__main__":
    app = App()
    app.run()

import chess
import interface
import subprocess
import json
import os

from engines.random_engine import RandomEngine
from random import randint

class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)
        self.engine = RandomEngine(self.board)
        self.iterations = 1000
        self.depth = 20

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

            self.play_ai_move()
            self.ui.update_screen()
        else:
            self.play_ai_move()
            self.ui.update_screen()

            self.ui.player_move()
            self.ui.update_screen()

    def mode_2(self):
        # AI vs AI
        self.play_ai_move()
        self.ui.update_screen()

        self.play_ai_move()
        self.ui.update_screen()

    def who_first(self):
        self.player_starts = bool(randint(0, 1))
        if not self.player_starts:
            self.ui.flip()

    def play_ai_move(self):
        # Get the correct path to mcts_engine.py
        engine_path = os.path.join(os.path.dirname(__file__), 'engines', 'mcts.py')
        
        process = subprocess.Popen(['pypy3', engine_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        input_data = json.dumps({
            "board_fen": self.board.fen(),
            "iterations": self.iterations,
            "depth": self.depth
        })
        stdout, stderr = process.communicate(input=input_data.encode('utf-8'))
        if stderr:
            print(stderr.decode('utf-8'))
        move = json.loads(stdout.decode('utf-8'))["move"]
        self.board.push(chess.Move.from_uci(move))

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
    print("Current Working Directory:", os.getcwd())  # Print working directory
    app.run(mode=1)

from engines.engine import Engine
from random import choice


class RandomEngine(Engine):
    def play_move(self):
        moves = list(self.board.legal_moves)
        if moves:
            self.board.push(choice(moves))

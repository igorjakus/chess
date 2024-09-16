from random import choice

from engines.engine import Engine


class RandomEngine(Engine):
    def play_move(self):
        moves = list(self.board.legal_moves)
        if moves:
            self.board.push(choice(moves))

    def quit(self):
        self.__del__()

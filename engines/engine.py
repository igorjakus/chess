from abc import ABC, abstractmethod
import chess


class Engine(ABC):
    def __init__(self, board : chess.Board):
        self.board = board

    @abstractmethod
    def play_move(self):
        pass

    @abstractmethod
    def quit(self):
        pass

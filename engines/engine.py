from abc import ABC, abstractmethod
import chess


class Engine(ABC):
    def __init__(self, board : chess.Board):
        self.board = board

    @abstractmethod
    def play_move(self) -> None:
        """Engine plays move and change board"""
        pass

    @abstractmethod
    def quit(self) -> None:
        """Safely turns off the engine"""
        pass

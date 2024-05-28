from abc import ABC, abstractmethod
import chess


class Engine(ABC):
    def __init__(self, board : chess.Board):
        self.board = board
        # self.pgn

    @abstractmethod
    def play_move(self):
        """Plays best move, returns that move"""
        pass

    # @abstractmethod
    # def opponent_play(self, move):
    #     """Plays move made by opponent

    #     Args:
    #         move (str): The move made by the opponent in standard chess notation.
    #     """
    #     pass

    # @abstractmethod
    # def print_pgn(self):
    #     """Method to print the game in PGN (Portable Game Notation) format."""
    #     pass

    # @abstractmethod
    # def load_fen(self, fen):
    #     """Method to load a game state from a FEN (Forsyth-Edwards Notation) string.

    #     Args:
    #         fen (str): The FEN string representing the game state.
    #     """
    #     self.board.set_fen(fen)

    # @abstractmethod
    # def get_fen(self):
    #     """Method to print the current game state in FEN format."""
    #     return self.board.fen()

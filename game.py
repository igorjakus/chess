import chessboard
import interface


class ChessGame():
    """This class manages all of the chess game

    Attributes:
        board (ChessBoard): blah blah
        ui (UserInterface): blah blah
    """

    def __init__(self):
        # Setting up chessboard
        self.board = chessboard.ChessBoard()

        # Setting up display
        self.ui = interface.UserInterface(self.board)

    def run_game(self):
        while True:
            self.ui._check_events()
            self.ui._update_screen()


if __name__ == '__main__':
    game = ChessGame()
    game.run_game()


import chess
import interface as interface


class App:
    def __init__(self):
        """Initialize the chess application."""
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)

    def run(self):
        """Run the main application loop."""
        self.ui.update_screen()
        while True:
            self.ui.handle_events()


if __name__ == "__main__":
    app = App()
    app.run()
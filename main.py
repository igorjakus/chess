import chess
import interface as interface


class App:
    def __init__(self):
        self.board = chess.Board()
        self.ui = interface.UserInterface(self.board)

    def run(self):    
        while True:
            self.ui.handle_events()


if __name__ == "__main__":
    app = App()
    app.run()

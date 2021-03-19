import pygame
from sys import exit


class ChessGame():
    """ Managing all game of chess"""
    def __init__(self):

        # Setting up display
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Python Chess - Igor Jakus")

        self.setup_board()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()

    def setup_board(self):
        self.board = []
        for i in range(8):
            for j in range(8):
                self.board.append(Square(i, j))

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit()

    def _update_screen(self):
        self.blit_board()
        pygame.display.flip()

    @staticmethod
    def handle_quit():
        exit()

    def blit_board(self):
        for square in self.board:
            pygame.draw.rect(self.screen, square.color(),
                             ((*square.position()), 100, 100))


class Square():
    """ Class for chess game square represence """
    def __init__(self, posX, posY):
        self.is_black = (posX + posY) % 2 == 0
        self.posX = posX
        self.posY = posY

    def position(self):
        return (self.posX * 100, self.posY * 100)

    def color(self):
        return (125, 135, 150) if self.is_black else (232, 235, 239)


if __name__ == '__main__':
    game = ChessGame()
    game.run_game()

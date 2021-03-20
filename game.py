from sys import exit
import pygame
import chessboard


class ChessGame():
    """ Managing all game of chess"""
    def __init__(self):

        # Setting up display
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Python Chess - Igor Jakus")

        # Setting up chessboard
        self.board = chessboard.ChessBoard()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.board.change_sides()

    @staticmethod
    def handle_quit():
        exit()

    def _blit_board(self):
        for square in self.board.chess_board:
            pygame.draw.rect(self.screen, square.color(),
                             ((*square.position()), 100, 100))

    def _blit_pieces(self):
        for piece in self.board.chess_pieces:
            self.screen.blit(piece.img, piece.rect)

    def _update_screen(self):
        self._blit_board()
        self._blit_pieces()
        pygame.display.flip()


if __name__ == '__main__':
    game = ChessGame()
    game.run_game()

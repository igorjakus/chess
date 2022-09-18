from sys import exit
from random import choice

from pieces import Pawn, Queen
import pygame


WHITE = True
BLACK = False


class UserInterface():
    """Class that helps user to use app and visualize all the stuff"""
    def __init__(self, board):

        # Setting up display
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Python Chess - Igor Jakus")
        window_logo = pygame.image.load("assets/king_white.png")
        pygame.display.set_icon(window_logo)

        self.moves = []
        self.board = board
        self.playersturn = WHITE
        self.selected_piece = None
        self.flipped_view = False

    def _reset(self):
        self.moves = []
        self.board.reset()
        self.playersturn = WHITE
        self.selected_piece = None
        self.flipped_view = False

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # handle mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse()

            # handle keyboard
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.flipped_view = not self.flipped_view
        elif event.key == pygame.K_r:
            self._reset()
        elif event.key == pygame.K_p:
            self.random_move()

    def _handle_mouse(self):
        # get mouse position
        mouseX, mouseY = pygame.mouse.get_pos()

        # get index of pieces list for selected_square square
        selected_square = (mouseX // 100) + (mouseY // 100) * 8
        if self.flipped_view:
            selected_square = abs(selected_square-63)  # 8*8 - 1

        # we have to check if its integer because
        # if it's 0 it would return None
        if isinstance(self.selected_piece, int):
            # if selected square has no piece, color = None
            color = getattr(self.board[selected_square], 'color', None)
            if color != self.board[self.selected_piece].color:
                if selected_square in self.moves:
                    self._move_piece(selected_square)
            else:
                self.moves = self.board[selected_square].moves(self.board)
                self.selected_piece = selected_square

        else:
            if self.board[selected_square] is not None:
                # you can only select your pieces
                if self.board[selected_square].color == self.playersturn:
                    self.moves = self.board[selected_square].moves(self.board)
                    self.selected_piece = selected_square

    def _move_piece(self, selected_square):
        # promotion
        if isinstance(self.board[self.selected_piece], Pawn):
            if 0 <= selected_square <= 7:
                # promotion for white pawn
                self.board[selected_square] = Queen(color=WHITE)
            elif 56 <= selected_square <= 63:
                # promotion for black pawn
                self.board[selected_square] = Queen(color=BLACK)

            else:
                # if no promotion
                self.board[selected_square] = self.board[self.selected_piece]

        else:
            # if no promotion
            self.board[selected_square] = self.board[self.selected_piece]

        # clearing board
        self.board[self.selected_piece] = None

        # cancel select
        self.selected_piece = None
        self.moves = []

        # switch turn
        # self.flipped_view = not self.flipped_view
        self.playersturn = not self.playersturn

    def random_move(self):
        # get list with all legal moves
        moves = []
        for piece in self.board:
            if piece is not None:
                if piece.color == self.playersturn:
                    for pm in piece.moves(self.board):
                        moves.append([piece, pm])

        # pick random one of all legal moves
        move = choice(moves)
        print("Random move:", move)

        # move piece with that picked move
        self.selected_piece = self.board.index(move[0])
        self._move_piece(move[1])

    def _update_screen(self):
        self._blit_board()
        self._blit_moves()
        self._blit_pieces()
        pygame.display.flip()

    def _blit_board(self):
        for i in range(8):
            for j in range(8):
                #            black                             white
                color = (125, 135, 150) if (i+j) % 2 else (232, 235, 239)
                pygame.draw.rect(self.screen, color, (i*100, j*100, 100, 100))

    def _blit_pieces(self):
        for square, piece in enumerate(self.board):
            if piece is None:
                continue
            rect_x, rect_y = ((square % 8) * 100, (square // 8) * 100)
            if self.flipped_view:
                rect_x, rect_y = abs(rect_x - 7 * 100), abs(rect_y - 7 * 100)
            self.screen.blit(piece.img, (rect_x, rect_y, 100, 100))

    def _blit_moves(self):
        for possible_move in self.moves:

            posX, posY = (possible_move % 8)*100, (possible_move // 8)*100
            if self.flipped_view:
                posX, posY = self.flipped_view_position(posX, posY)

            if self.board[possible_move]:
                rect = posX, posY, 100, 100
                pygame.draw.rect(self.screen, (255, 102, 102), rect)
            else:
                center = posX + 50, posY + 50
                pygame.draw.circle(self.screen, (111, 159, 191), center, 15)

    @staticmethod
    def flipped_view_position(x, y):
        return abs(x - 7*100), abs(y - 7*100)

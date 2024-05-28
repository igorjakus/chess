from sys import exit
import pygame
import chess
import random
from resource_manager import ResourceManager


class UserInterface:
    SQUARE_SIZE = 80
    SCREEN_SIZE = (8 * SQUARE_SIZE, 8 * SQUARE_SIZE)

    def __init__(self, board: chess.Board):
        self.resources = ResourceManager(UserInterface.SQUARE_SIZE)

        pygame.init()
        self.screen = pygame.display.set_mode(UserInterface.SCREEN_SIZE)
        pygame.display.set_caption("Python Chess - Igor Jakus")
        pygame.display.set_icon(self.resources.logo)
        
        self.board = board
        self.selected_piece = None
        self.flipped_view = False
        self.legal_moves = []

    def reset(self):
        self.board.reset()
        self.selected_piece = None
        self.flipped_view = False
        self.legal_moves = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click()
                self.update_screen()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
                self.update_screen()

    def _quit_game(self):
        pygame.quit()
        exit()

    def _handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.flipped_view = not self.flipped_view
        elif event.key == pygame.K_r:
            self.reset()
        elif event.key == pygame.K_p:
            self.random_move()

    def _handle_mouse_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_square = self._get_square_under_mouse(mouse_x, mouse_y)
        if self.selected_piece is None:
            self._select_piece(selected_square)
        else:
            self._move_or_deselect_piece(selected_square)

    def _select_piece(self, square):
        if self.board.color_at(square) is self.board.turn:
            self.selected_piece = square
            self.legal_moves = [move for move in self.board.legal_moves if move.from_square == square]

    def _move_or_deselect_piece(self, square):
        if square == self.selected_piece:  # deselect
            self.selected_piece = None
            self.legal_moves = []
        else:  # move piece
            move = chess.Move(self.selected_piece, square)

            if self.is_promotion(move):
                    move.promotion = self._handle_promotion()

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_piece = None
                self.legal_moves = []
    
    def _handle_promotion(self):
        """ trzeba to rozwinąć! """
        return chess.QUEEN
    
    def random_move(self):
        moves = list(self.board.legal_moves)
        if moves:
            self.board.push(random.choice(moves))

    def update_screen(self):
        """Update the screen with the current state of the board."""
        self._draw_board()
        self._highlight_moves()
        self._draw_pieces()
        pygame.display.flip()

    def _draw_board(self):
        SQUARE = self.SQUARE_SIZE
        WHITE = (232, 235, 239)
        BLACK = (125, 135, 150)

        for i in range(8):
            for j in range(8):
                color = BLACK if (i + j) % 2 else WHITE
                pygame.draw.rect(
                    self.screen,
                    color,
                    (i * SQUARE, j * SQUARE, SQUARE, SQUARE),
                )

    def _draw_pieces(self):
        SQUARE = UserInterface.SQUARE_SIZE
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = self.resources.piece_images[piece.symbol()]
                pos_x, pos_y = self._square_to_position(square)
                rect = pygame.Rect(pos_x, pos_y, SQUARE, SQUARE)
                self.screen.blit(piece_image, rect)

    def _get_square_under_mouse(self, mouse_x, mouse_y):
        # ekran zaczyna sie od lewego gornego rogu
        selected_row = 7 - mouse_y // UserInterface.SQUARE_SIZE
        selected_col = mouse_x // UserInterface.SQUARE_SIZE

        if self.flipped_view:
            selected_row = 7 - selected_row
            selected_col = 7 - selected_col

        print(selected_row, selected_col)
        return chess.square(selected_col, selected_row)

    def _square_to_position(self, square):
        """Square to pos_x, pos_y"""
        row, col = divmod(square, 8)
        if self.flipped_view:
            col, row = 7 - col, 7 - row

        x = col * self.SQUARE_SIZE
        y = (7-  row) * self.SQUARE_SIZE
        return x, y

    def _highlight_moves(self):
        SQUARE = self.SQUARE_SIZE
        LIGHT_BLUE = (111, 159, 191)
        RED = (255, 102, 102)

        if self.selected_piece is not None:
            x, y = self._square_to_position(self.selected_piece)
            rect = (x, y, SQUARE, SQUARE)
            pygame.draw.rect(self.screen, LIGHT_BLUE, rect)

        for move in self.legal_moves:
            square = move.to_square
            x, y = self._square_to_position(square)

            if self.board.is_capture(move): 
                rect = (x, y, SQUARE, SQUARE)
                pygame.draw.rect(self.screen, RED, rect)
            else:
                center = (x + SQUARE // 2, y + SQUARE // 2)
                pygame.draw.circle(self.screen, LIGHT_BLUE, center, SQUARE // 7)

    def _highlight_check(self):
        pass

    @staticmethod
    def is_promotion(move):
        return chess.Move.from_uci(str(move)).promotion is not None
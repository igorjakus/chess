from sys import exit
import pygame
import chess
import random
from resource_manager import ResourceManager


class UserInterface:
    SQUARE = 80
    SCREEN_SIZE = (8 * SQUARE, 8 * SQUARE)

    WHITE = (232, 235, 239)
    BLACK = (125, 135, 150)
    LIGHT_BLUE = (111, 159, 191)
    RED = (255, 102, 102)
    DARK_RED = (136, 8, 8)

    def __init__(self, board: chess.Board):
        self.resources = ResourceManager(self.SQUARE)

        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
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
        self._draw_effects()
        self._draw_pieces()
        pygame.display.flip()

    def _draw_board(self):
        for i in range(8):
            for j in range(8):
                color = self.BLACK if (i + j) % 2 else self.WHITE
                rect = (i * self.SQUARE, j * self.SQUARE, self.SQUARE, self.SQUARE)
                pygame.draw.rect(self.screen, color, rect)

    def _draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = self.resources.piece_images[piece.symbol()]
                pos_x, pos_y = self._square_to_position(square)
                rect = pygame.Rect(pos_x, pos_y, self.SQUARE, self.SQUARE)
                self.screen.blit(piece_image, rect)

    def _draw_effects(self):
        self._highlight_moves()
        self._highlight_selected()
        self._highlight_check()

    def _highlight_moves(self):
        for move in self.legal_moves:
            square = move.to_square
            x, y = self._square_to_position(square)

            if self.board.is_capture(move): 
                rect = (x, y, self.SQUARE, self.SQUARE)
                pygame.draw.rect(self.screen, self.RED, rect)
            else:
                center = (x + self.SQUARE // 2, y + self.SQUARE // 2)
                pygame.draw.circle(self.screen, self.LIGHT_BLUE, center, self.SQUARE // 7)

    def _highlight_selected(self):
         if self.selected_piece is not None:
            x, y = self._square_to_position(self.selected_piece)
            rect = (x, y, self.SQUARE, self.SQUARE)
            pygame.draw.rect(self.screen, self.LIGHT_BLUE, rect)

    def _highlight_check(self):
        if self.board.is_check():
            king_square = self.board.king(self.board.turn)
            x, y = self._square_to_position(king_square)
            rect = (x, y, self.SQUARE, self.SQUARE)
            pygame.draw.rect(self.screen, self.DARK_RED, rect)

    def _get_square_under_mouse(self, mouse_x, mouse_y):
        # ekran zaczyna sie od lewego gornego rogu
        selected_row = 7 - mouse_y // self.SQUARE
        selected_col = mouse_x // self.SQUARE

        if self.flipped_view:
            selected_row = 7 - selected_row
            selected_col = 7 - selected_col

        return chess.square(selected_col, selected_row)

    def _square_to_position(self, square):
        """Square to pos_x, pos_y"""
        row, col = divmod(square, 8)
        if self.flipped_view:
            col, row = 7 - col, 7 - row

        x = col * self.SQUARE
        y = (7 - row) * self.SQUARE
        return x, y

    def is_promotion(self, move):
        # Check if the move is a pawn move to the back rank
        if self.board.piece_at(move.from_square).piece_type == chess.PAWN:
            if chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7:
                return True
        return False
    
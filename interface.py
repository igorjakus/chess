from sys import exit
import pygame
import chess
import random

from config import Config
from resource_manager import ResourceManager


class UserInterface:
    def __init__(self, board: chess.Board):
        self.resources = ResourceManager(Config.SQUARE)

        pygame.init()
        self.screen = pygame.display.set_mode(Config.SCREEN_SIZE)
        pygame.display.set_caption("Python Chess - Igor Jakus")
        pygame.display.set_icon(self.resources.logo)

        self.font = pygame.font.SysFont(None, Config.FONT)
        self.small_font = pygame.font.SysFont(None, Config.SMALL_FONT)

        self.board = board
        self.selected_piece = None
        self.flipped_view = False
        self.legal_moves = []
        self.game_over = False
        self.update_screen()

    def reset(self):
        self.board.reset()
        self.selected_piece = None
        self.flipped_view = False
        self.legal_moves = []
        self.game_over = False

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

    def _select_piece(self, square):
        if self.board.color_at(square) is self.board.turn:
            self.selected_piece = square
            self.legal_moves = [move for move in self.board.legal_moves if move.from_square == square]
    
    def player_move(self):
        move_made = False
        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    move_made = self._handle_mouse_click()
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event)
                self.update_screen()

    def _handle_mouse_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_square = self._get_square_under_mouse(mouse_x, mouse_y)
        if self.selected_piece is None:
            self._select_piece(selected_square)
        elif selected_square == self.selected_piece:
            self._deselect_piece()
        else:
            if self._move_piece(selected_square):
                return True  # Zwróć True, jeśli ruch został wykonany
        return False  # Zwróć False, jeśli ruch nie został wykonany

    def _move_piece(self, square):
        move = chess.Move(self.selected_piece, square)
        if self._is_promotion(move):
            move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_piece = None
            self.legal_moves = []

            if self.board.is_game_over():
                self.game_over = True
            return True  # Ruch został wykonany
        return False  # Ruch nie został wykonany

    def _deselect_piece(self):
        self.selected_piece = None
        self.legal_moves = []

    def _is_promotion(self, move):
        piece = self.board.piece_at(move.from_square)
        return piece and piece.piece_type == chess.PAWN and chess.square_rank(move.to_square) in {0, 7}

    def random_move(self):
        self._deselect_piece()
        moves = list(self.board.legal_moves)
        if moves:
            self.board.push(random.choice(moves))

    def update_screen(self):
        self._draw_board()
        self._draw_effects()
        self._draw_pieces()
        if self.game_over:
            self._draw_game_over()
        pygame.display.flip()

    def _draw_board(self):
        for i in range(8):
            for j in range(8):
                color = Config.BLACK if (i + j) % 2 else Config.WHITE
                rect = (i * Config.SQUARE, j * Config.SQUARE, Config.SQUARE, Config.SQUARE)
                pygame.draw.rect(self.screen, color, rect)

    def _draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = self.resources.piece_images[piece.symbol()]
                pos_x, pos_y = self._square_to_position(square)
                rect = pygame.Rect(pos_x, pos_y, Config.SQUARE, Config.SQUARE)
                self.screen.blit(piece_image, rect)

    def _draw_effects(self):
        self._highlight_moves()
        self._highlight_selected()
        self._highlight_check()

    def _highlight_moves(self):
        for move in self.legal_moves:
            x, y = self._square_to_position(move.to_square)
            if self.board.is_capture(move):
                rect = (x, y, Config.SQUARE, Config.SQUARE)
                pygame.draw.rect(self.screen, Config.RED, rect)
            else:
                center = (x + Config.SQUARE // 2, y + Config.SQUARE // 2)
                pygame.draw.circle(self.screen, Config.LIGHT_BLUE, center, Config.SQUARE // 7)

    def _highlight_selected(self):
        if self.selected_piece is not None:
            x, y = self._square_to_position(self.selected_piece)
            rect = (x, y, Config.SQUARE, Config.SQUARE)
            pygame.draw.rect(self.screen, Config.LIGHT_BLUE, rect)

    def _highlight_check(self):
        if self.board.is_check():
            king_square = self.board.king(self.board.turn)
            x, y = self._square_to_position(king_square)
            rect = (x, y, Config.SQUARE, Config.SQUARE)
            pygame.draw.rect(self.screen, Config.DARK_RED, rect)

    def _draw_game_over(self):
        text = self.font.render(f"GAME OVER {self.board.result()}", True, Config.DARK_RED)
        text_rect = text.get_rect(center=(Config.SCREEN_SIZE[0] // 2, Config.SCREEN_SIZE[1] // 2))
        self.screen.blit(text, text_rect)

        small_text = self.small_font.render("Press r to start new game", True, Config.DARK_RED)
        small_text_rect = small_text.get_rect(center=(Config.SCREEN_SIZE[0] // 2, Config.SCREEN_SIZE[1] // 2 + Config.SCREEN_SIZE[1] // 15))
        self.screen.blit(small_text, small_text_rect)

    def _get_square_under_mouse(self, mouse_x, mouse_y):
        selected_row = 7 - mouse_y // Config.SQUARE
        selected_col = mouse_x // Config.SQUARE

        if self.flipped_view:
            selected_row = 7 - selected_row
            selected_col = 7 - selected_col

        return chess.square(selected_col, selected_row)

    def _square_to_position(self, square):
        row, col = divmod(square, 8)
        if self.flipped_view:
            col, row = 7 - col, 7 - row

        x = col * Config.SQUARE
        y = (7 - row) * Config.SQUARE
        return x, y

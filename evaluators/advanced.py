import chess
from evaluators.piece_tables import PAWN_TABLE, KNIGHTS_TABLE
from evaluators.helper_functions import get_king_surroundings
from evaluators.evaluator import Evaluator


class AdvancedEvaluator(Evaluator):
    MAX_SCORE = 10_000

    def __init__(self):
        self.cache = dict()

    def evaluate(self, board: chess.Board):
        """ Podaje ewaluacje planszy podaną w centypionach"""
        fen = board.board_fen()
        if fen in self.cache:
            return self.cache[fen]

        if board.is_game_over():
            return self.gameover_evaluation(board)

        value = (
            self.material(board) + 
            self.attacking_squares(board) * 5 +
            self.tempo(board) * 10 +
            self.aggressiveness(board) * 10 +
            self.pawn_advancement(board) * 10 +  # tu tez moze byc blad
            self.knight_position(board) # tu moze byc blad
        )

        value *= 1 if board.turn == chess.WHITE else -1
        self.cache[fen] = value
        return value

    def gameover_evaluation(self, board):
        winner = board.outcome().winner
        if winner is None:
            return 0  # draw
        if winner == chess.WHITE: 
            return self.MAX_SCORE - len(board.move_stack) # prioritise faster checkmates
        return -self.MAX_SCORE + len(board.move_stack)    # prioritise faster checkmates
    
    def material(self, board : chess.Board):
        """I found it at chessprogramming.com"""
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return (
            100 * chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
            300 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            300 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            500 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            900 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )

    def tempo(self, board: chess.Board):
        return 1 if board.turn == chess.WHITE else -1

    def aggressiveness(self, board: chess.Board):
        """Ile figur atakuje pola wokół króla"""
        value = 0

        # ile białych figur atakuje czarnego króla i jego otoczenie
        for square in get_king_surroundings(board, chess.BLACK):
            value += chess.popcount(board.attackers_mask(chess.WHITE, square))
        
        # ile czarnych figur atakuje białego króla i jego otoczenie
        for square in get_king_surroundings(board, chess.WHITE):
            value -= chess.popcount(board.attackers_mask(chess.BLACK, square))
        
        return value

    def attacking_squares(self, board: chess.Board):
        """Count how many squares (including it's own) is white or black attacking"""
        white_moves = 0
        black_moves = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                attacks_mask = board.attacks_mask(square)
                if piece.color == chess.WHITE:
                    white_moves += chess.popcount(attacks_mask)
                else:
                    black_moves += chess.popcount(attacks_mask)

        return white_moves - black_moves


    def pawn_advancement(self, board: chess.Board):
        """Oblicza sumę wartości pionków na podstawie tabeli PAWN_TABLE."""
        total_value = 0
        
        # Dodaj wartości białych pionków
        for square in board.pieces(chess.PAWN, chess.WHITE):
            row = square // 8
            col = square % 8
            total_value += PAWN_TABLE[7-row][col]
        
        for square in board.pieces(chess.PAWN, chess.BLACK):
            row = square // 8
            col = square % 8
            total_value -= PAWN_TABLE[row][col]
        
        return total_value

    def knight_position(self, board: chess.Board):
        """Oblicza sumę wartości pionków na podstawie tabeli PAWN_TABLE."""
        total_value = 0
        
        # Dodaj wartości białych pionków
        for square in board.pieces(chess.KNIGHT, chess.WHITE):
            row = square // 8
            col = square % 8
            total_value += KNIGHTS_TABLE[7-row][col]
        
        for square in board.pieces(chess.KNIGHT, chess.BLACK):
            row = square // 8
            col = square % 8
            total_value -= KNIGHTS_TABLE[row][col]
        
        return total_value

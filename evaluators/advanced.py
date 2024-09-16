import chess
from evaluators.evaluator import Evaluator
from evaluators.pesto import (EG_BISHOP, EG_KING, EG_KNIGHT, EG_PAWN, EG_QUEEN,
                              EG_ROOK, MG_BISHOP, MG_KING, MG_KNIGHT, MG_PAWN,
                              MG_QUEEN, MG_ROOK)
from evaluators.piece_tables import (BISHOP_TABLE, KING_ENDGAME_TABLE,
                                     KING_MIDGAME_TABLE, KNIGHT_TABLE,
                                     PAWN_TABLE, QUEEN_TABLE, ROOK_TABLE)


class AdvancedEvaluator(Evaluator):
    MAX_SCORE = 10_000

    def __init__(self):
        self.cache = dict()

    def evaluate(self, board: chess.Board):
        """Returns evaluation for given board in centipawns"""
        fen = board.board_fen()
        if fen in self.cache:
            return self.cache[fen]

        if board.is_game_over():
            return self.gameover_evaluation(board)

        value = (
            self.material(board) + 
            # self.piece_tables(board) +
            self.pesto_tables(board)
            # self.tempo(board) * 10
            # self.attacking_squares(board) * 5 +
            # self.aggressiveness(board) * 10
        )

        value *= 1 if board.turn == chess.WHITE else -1
        self.cache[fen] = value
        return value

    def gameover_evaluation(self, board : chess.Board):
        """Evaluate when game is over"""
        winner = board.outcome().winner
        if winner is None:
            return 0  # draw
        score = self.MAX_SCORE - len(board.move_stack) # prioritise faster checkmates
        return score if winner == board.turn else -score

    @staticmethod
    def material(board : chess.Board):
        """Returns material balance in centipawns"""
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return (
            100 * chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
            300 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            300 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            500 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            900 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )

    def piece_tables(self, board: chess.Board) -> int:
        evaluation = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            
            if piece is not None:
                piece_type = piece.piece_type
                color = piece.color
                
                if piece_type == chess.PAWN:
                    table = PAWN_TABLE
                elif piece_type == chess.KNIGHT:
                    table = KNIGHT_TABLE
                elif piece_type == chess.BISHOP:
                    table = BISHOP_TABLE
                elif piece_type == chess.ROOK:
                    table = ROOK_TABLE
                elif piece_type == chess.QUEEN:
                    table = QUEEN_TABLE
                elif piece_type == chess.KING:
                    if self.is_endgame(board):
                        table = KING_ENDGAME_TABLE
                    else:
                        table = KING_MIDGAME_TABLE 
    
                if color == chess.WHITE:
                    evaluation += table[chess.square_mirror(square)]
                else:
                    evaluation -= table[square]
        
        return evaluation

    def pesto_tables(self, board: chess.Board) -> int:
        """Use PeSTO as piece-table to estimate pieces strategic placement"""
        evaluation = 0
        endgame = self.is_endgame(board)
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            
            if piece is not None:
                piece_type = piece.piece_type
                color = piece.color
                
                if piece_type == chess.PAWN:
                    table = EG_PAWN if endgame else MG_PAWN
                elif piece_type == chess.KNIGHT:
                    table = EG_KNIGHT if endgame else MG_KNIGHT
                elif piece_type == chess.BISHOP:
                    table = EG_BISHOP if endgame else MG_BISHOP
                elif piece_type == chess.ROOK:
                    table = EG_ROOK if endgame else MG_ROOK
                elif piece_type == chess.QUEEN:
                    table = EG_QUEEN if endgame else MG_QUEEN
                elif piece_type == chess.KING:
                    table = EG_KING if endgame else MG_KING
                else:
                    continue
                
                if color == chess.WHITE:
                    evaluation += table[chess.square_mirror(square)]
                else:
                    evaluation -= table[square]
        
        return evaluation

    @staticmethod
    def tempo(board: chess.Board):
        """Reward if white has tempo, punish if black has tempo"""
        return 1 if board.turn == chess.WHITE else -1

    @staticmethod
    def attacking_squares(board: chess.Board):
        """Count how many squares each side attacks"""
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
      
    def aggressiveness(self, board: chess.Board):
        """Returns sum of attackers for each square near king"""
        value = 0

        # ile białych figur atakuje czarnego króla i jego otoczenie
        for square in self.get_king_surroundings(board, chess.BLACK):
            value += chess.popcount(board.attackers_mask(chess.WHITE, square))
        
        # ile czarnych figur atakuje białego króla i jego otoczenie
        for square in self.get_king_surroundings(board, chess.WHITE):
            value -= chess.popcount(board.attackers_mask(chess.BLACK, square))
        
        return value

    @staticmethod
    def get_king_surroundings(board: chess.Board, color: chess.Color):
        """Returns list of squares around king"""
        king_square = board.pieces(chess.KING, color).pop()
        
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square) 
        
        surrounding_squares = []
        
        for rank_offset in [-1, 0, 1]:
            for file_offset in [-1, 0, 1]:
                new_rank = king_rank + rank_offset
                new_file = king_file + file_offset
                
                if 0 <= new_rank <= 7 and 0 <= new_file <= 7:  # pole jest na planszy
                    square = chess.square(new_file, new_rank)
                    surrounding_squares.append(square)

        return surrounding_squares
    
    @staticmethod
    def is_endgame(board: chess.Board) -> bool:
        return chess.popcount(board.queens) == 0
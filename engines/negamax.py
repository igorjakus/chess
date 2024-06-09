import chess
from engines.engine import Engine
from evaluators.advanced import AdvancedEvaluator
from config import Config


evaluator = AdvancedEvaluator()

def ordered_moves(board: chess.Board, order=False):
    """Sort moves by evaluation"""
    def eval_prio(move):
        board.push(move)
        prio = evaluator.evaluate(board)
        board.pop()
        return prio
    
    moves = board.legal_moves
    return moves if not order else sorted(moves, key=eval_prio, reverse=True)

def negamax(state: chess.Board, depth, alpha, beta):
    if depth <= 0 or state.is_game_over():
        return evaluator.evaluate(state)

    # Sort moves only if depth is 6 or more
    moves = ordered_moves(state, order=depth>=6)
    
    max_score = float("-inf")
    for move in moves:
        state.push(move)
        score = -negamax(state, depth - 1, -beta, -alpha)
        state.pop()

        max_score = max(max_score, score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return max_score

def best_move(state: chess.Board, depth):
    best_move = None
    best_value = float("-inf")

    for move in state.legal_moves:
        state.push(move)
        value = -negamax(state, depth - 1, float("-inf"), float("inf"))
        state.pop()

        if value > best_value:
            best_value = value
            best_move = move
    
    return best_move


class NegamaxEngine(Engine):
    def __init__(self, board):
        self.board = board
        self.depth = Config.NEGAMAX_DEPTH

    def play_move(self):
        if self.board.is_game_over():
            return 
        move = best_move(self.board, self.depth)
        self.board.push(move)

    def quit(self):
        pass  # no need to delete anything manually
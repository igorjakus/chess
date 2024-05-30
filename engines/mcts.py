# mcts_engine.py

from math import sqrt, log
import random
import chess
import sys
import json

from evaluator import MaterialEvaluator
from engine import Engine

class Node:
    def __init__(self, board: chess.Board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(list(self.board.legal_moves))

    def uct(self, exploration_weight=1.4142):
        return (self.wins / self.visits) + exploration_weight * sqrt(log(self.parent.visits) / self.visits)

    def best_child(self, exploration_weight=1.4142):
        best_score = float("-inf")
        best_child = None
        for child in self.children:
            uct_score = child.uct(exploration_weight)
            if uct_score > best_score:
                best_child = child
                best_score = uct_score
        return best_child

    def add_child(self, child_state, move):
        child_node = Node(child_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

class MCTS(Engine):
    def __init__(self, board: chess.Board, iterations=1000, depth=20):
        self.board = board
        self.evaluator = MaterialEvaluator()
        self.iterations = iterations
        self.depth = depth

    def play_move(self):
        self.node = Node(self.board)
        move = self.mcts()
        self.board.push(move)
        return move

    def mcts(self):
        for __ in range(self.iterations):
            node = self.node

            # selection
            while not node.board.is_game_over() and node.is_fully_expanded():
                node = node.best_child()

            # expansion
            if not node.is_fully_expanded() and not node.board.is_game_over():
                # select move that's not child yet
                move = random.choice([m for m in node.board.legal_moves if not any(child.move == m for child in node.children)])
                new_board = node.board.copy()
                new_board.push(move)
                node = node.add_child(new_board, move)

            # simulation
            simulated_board = node.board.copy()
            reward = self.simulate_game(simulated_board)

            # backpropagation
            while node is not None:
                node.visits += 1
                node.wins += reward if node.board.turn == chess.WHITE else 1 - reward
                node = node.parent

        # best child is that with most visits (recommended by authors of MCTS)
        return max(self.node.children, key=lambda n: n.visits).move

    def simulate_game(self, board: chess.Board):
        for __ in range(self.depth):
            if board.is_game_over():
                result = board.result()
                if result == '1-0':
                    return 1
                elif result == '0-1':
                    return 0
                else:
                    return 0.5

            move = random.choice(list(board.legal_moves))
            board.push(move)

        evaluation = self.evaluator.evaluate(board)

        if abs(evaluation) < 3:
            return 0.5  # too small difference to determine win
        elif evaluation < 0:
            return 0
        else:
            return 1

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    board_fen = input_data["board_fen"]
    iterations = input_data["iterations"]
    depth = input_data["depth"]

    board = chess.Board(board_fen)
    engine = MCTS(board, iterations, depth)
    move = engine.play_move()

    sys.stdout.write(json.dumps({"move": move.uci()}))

from math import sqrt, log
import random
import chess

from evaluators.material import MaterialEvaluator
from engines.engine import Engine


class Node:
    def __init__(self, board: chess.Board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.uct_value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(list(self.board.legal_moves))

    def update_uct_value(self, exploration_weight=1.4142):
        if self.visits > 0:
            self.uct_value = (self.wins / self.visits) + exploration_weight * sqrt(log(self.parent.visits) / self.visits)

    def best_child(self, exploration_weight=1.4142):
        for child in self.children:
            child.update_uct_value(exploration_weight)
        return max(self.children, key=lambda child: child.uct_value)

    def add_child(self, child_state, move):
        child_node = Node(child_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node


class MCTS_Engine(Engine):
    def __init__(self, board: chess.Board, iterations=1000, depth=20):
        self.board = board
        self.evaluator = MaterialEvaluator()
        self.iterations = iterations
        self.depth = depth

    def play_move(self):
        self.node = Node(self.board)
        move = self.mcts()
        self.board.push(move)

    def mcts(self):
        for _ in range(self.iterations):
            node = self.node

            # Selection
            while not node.board.is_game_over() and node.is_fully_expanded():
                node = node.best_child()

            # Expansion
            if not node.is_fully_expanded() and not node.board.is_game_over():
                move = random.choice([m for m in node.board.legal_moves if not any(child.move == m for child in node.children)])
                new_board = node.board.copy()
                new_board.push(move)
                node = node.add_child(new_board, move)

            # Simulation
            simulated_board = node.board.copy()
            reward = self.simulate_game(simulated_board)

            # Backpropagation
            while node is not None:
                node.visits += 1
                if node.board.turn == chess.BLACK:
                    node.wins += reward  # reward is from White's perspective
                else:
                    node.wins += 1 - reward  # reward is from Black's perspective
                node = node.parent

        return max(self.node.children, key=lambda n: n.visits).move

    def simulate_game(self, board: chess.Board):
        """Simulate game into some depth and then evaluate"""
        for _ in range(self.depth):
            if board.is_game_over():
                result = board.result()
                if result == '1-0':
                    return 1  # White wins
                elif result == '0-1':
                    return 0  # Black wins
                else:
                    return 0.5  # Draw

            move = random.choice(list(board.legal_moves))
            board.push(move)

        evaluation = self.evaluator.evaluate(board)

        if abs(evaluation) <= 100:
            return 0.5  # too small difference to determine win
        elif evaluation < 0:
            return 0  # Black is winning
        else:
            return 1  # White is winning

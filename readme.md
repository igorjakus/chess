# Chess Engines in Python!

### Project Overview

This project is part of the Object-Oriented Programming course at the University of Wrocław. The main goal is to develop several chess engines in Python using the `python-chess` library, along with a playable interface. The project includes implementations of different algorithms such as MCTS (Monte Carlo Tree Search), Negamax, and a Random Player. Advanced optimization techniques, bitmask utilization, intelligent heuristics, and a user interface created with `pygame` are also integrated into the project.

### Features

1. **Chess Engines**
   - **MCTS (Monte Carlo Tree Search)**: A decision-making algorithm that uses randomness to explore the most promising moves and simulates game outcomes to choose the best move.
   - **Negamax**: A variant of the Minimax algorithm, optimized for zero-sum games like chess, with alpha-beta pruning.
   - **Random Player**: A simple algorithm that makes random moves.
   - **Stockfish**: You can play against Stockfish. Warning! Remember to specify your stockfish path in config!

2. **Optimization Techniques**
   - Advanced optimization tricks to enhance the performance of the chess engines.
   - Use of bitmasks for efficient board representation and move generation.
   - Implementation of intelligent heuristics to evaluate board positions and guide the search algorithms.

3. **User Interface**
   - A playable interface using `pygame` to interact with the chess engines.
   - Visualization of the chessboard, moves, and game status.
   - Support for player vs. engine and engine vs. engine modes.

### Technologies and Libraries

- **Python**: The main programming language used for the project.
- **python-chess**: A chess library for move generation, validation, and board representation.
- **pygame**: A library for creating the graphical user interface and handling user interactions.


### Configuration
Feel free to modify config.py to fine-tune your experience
If you want to use stockfish, remember to specify your stockfish path in config!
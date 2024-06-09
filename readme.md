# Chess Engines in Python!

### Project Overview

This project is part of the Object-Oriented Programming course at the University of Wrocław. The main goal is to develop several chess engines in Python using the `python-chess` library, along with a playable interface created with `pygame`. The project includes implementations of different algorithms such as MCTS (Monte Carlo Tree Search), Negamax, and a Random Player.

### Features

1. **Chess Engines**
   - **MCTS (Monte Carlo Tree Search)**: A decision-making algorithm that uses randomness to explore the most promising moves and simulates game outcomes to choose the best move.
   - **Negamax**: A variant of the Minimax algorithm, optimized for zero-sum games like chess, with alpha-beta pruning.
   - **Random Player**: A simple algorithm that makes random moves.
   - **Stockfish**: You can play against Stockfish. Warning! Remember to specify your stockfish path in config!

2. **User Interface**
   - A playable interface using `pygame` to interact with the chess engines.
   - Visualization of the chessboard, moves, and game status.
   - Support for player vs player, player vs engine and engine vs engine modes.

### Requirements
- Python 3.9.6 or later
- chess 1.10.0 or later
- pygame 2.5.2 or later

You can install the necessary dependencies using:
```bash
pip install -r requirements.txt
```

### Installation
```bash
git clone https://github.com/igorjakus/chess.git
cd chess
pip install -r requirements.txt
```

(Optional) If you want to use the Stockfish engine, download it and compile it from [Stockfish website](https://stockfishchess.org/download/). In the config.py file, specify the path to the compiled binary of Stockfish.

### Configuration
Feel free to modify `config.py` to fine-tune your experience. I've made the editing process as easy as possible.
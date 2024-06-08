class Config:
    # MOST IMPORTANT
    ENGINE = "stockfish"  # ["stockfish", "mcts", "random"]
    WINDOW_SIZE = 640

    # paths
    STOCKFISH_PATH = "/Users/igorjakus/Downloads/stockfish/src/stockfish"

    # engines variables
    STOCKFISH_TIME_PER_MOVE = 0.1
    MCTS_ITERATIONS = 1000
    MCTS_DEPTH = 20

    # sizes
    SQUARE_SIZE = WINDOW_SIZE // 8
    SCREEN_SIZE = (WINDOW_SIZE, WINDOW_SIZE)
    FONT = SCREEN_SIZE[0] // 10
    SMALL_FONT = SCREEN_SIZE[0] // 20

    # colors
    WHITE = (232, 235, 239)
    BLACK = (125, 135, 150)
    LIGHT_BLUE = (111, 159, 191)
    RED = (255, 102, 102)
    DARK_RED = (136, 8, 8)
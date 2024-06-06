class Config:
    # sizes
    SQUARE_SIZE = 80
    SCREEN_SIZE = (8 * SQUARE_SIZE, 8 * SQUARE_SIZE)
    FONT = SCREEN_SIZE[0] // 10
    SMALL_FONT = SCREEN_SIZE[0] // 20

    # colors
    WHITE = (232, 235, 239)
    BLACK = (125, 135, 150)
    LIGHT_BLUE = (111, 159, 191)
    RED = (255, 102, 102)
    DARK_RED = (136, 8, 8)

    # paths
    STOCKFISH_PATH = "/Users/igorjakus/Downloads/stockfish/src/stockfish"

    # engines variables
    STOCKFISH_TIME_PER_MOVE = 0.5
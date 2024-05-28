class Config:
    # sizes
    SQUARE = 80
    # EVALBAR_HEIGHT = SQUARE // 3
    EVALBAR_HEIGHT = 0
    SCREEN_SIZE = (8 * SQUARE, 8 * SQUARE + EVALBAR_HEIGHT)
    FONT = SCREEN_SIZE[0] // 10
    SMALL_FONT = SCREEN_SIZE[0] // 20

    # colors
    WHITE = (232, 235, 239)
    BLACK = (125, 135, 150)
    LIGHT_BLUE = (111, 159, 191)
    RED = (255, 102, 102)
    DARK_RED = (136, 8, 8)
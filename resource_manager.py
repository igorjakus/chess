import pygame


class ResourceManager:
    def __init__(self, SQUARE_SIZE):
        pygame.init()
        self.logo = self._load_logo()
        self.piece_images = self._load_piece_images(SQUARE_SIZE)

    def _load_logo(self):
        return pygame.image.load("assets/logo.png")

    def _load_piece_images(self, SQUARE_SIZE):
        PIECE_TYPES = {
            "P": "pawn",
            "R": "rook",
            "N": "knight",
            "B": "bishop",
            "Q": "queen",
            "K": "king",
        }

        pieces = {}

        for piece in ["P", "R", "N", "B", "Q", "K", "p", "r", "n", "b", "q", "k"]:
            color = "white" if piece.isupper() else "black"
            piece_type = PIECE_TYPES[piece.upper()]
            file = f"assets/pieces/{piece_type}_{color}.png"
            image = pygame.image.load(file)
            pieces[piece] = pygame.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
        return pieces

import pygame


class Piece:
    """ Parental class for all pieces """
    def __init__(self, x, y, is_black):
        self.is_black = is_black


class Pawn(Piece):
    points = 1

    def __init__(self, x, y, is_black):
        super().__init__(x, y, is_black)
        if is_black:
            self.img = pygame.image.load('assets/pawn_black.png')
        else:
            self.img = pygame.image.load('assets/pawn_white.png')
        self.rect = self.img.get_rect(topleft=(x*100, y*100))


class Knight(Piece):
    points = 3

    def __init__(self, x, y, is_black):
        super().__init__(x, y, is_black)
        if is_black:
            self.img = pygame.image.load('assets/knight_black.png')
        else:
            self.img = pygame.image.load('assets/knight_white.png')
        self.rect = self.img.get_rect(topleft=(x*100, y*100))


class Bishop(Piece):
    points = 3

    def __init__(self, x, y, is_black):
        super().__init__(x, y, is_black)
        if is_black:
            self.img = pygame.image.load('assets/bishop_black.png')
        else:
            self.img = pygame.image.load('assets/bishop_white.png')
        self.rect = self.img.get_rect(topleft=(x*100, y*100))


class Rook(Piece):
    points = 5

    def __init__(self, x, y, is_black):
        super().__init__(x, y, is_black)
        if is_black:
            self.img = pygame.image.load('assets/rook_black.png')
        else:
            self.img = pygame.image.load('assets/rook_white.png')
        self.rect = self.img.get_rect(topleft=(x*100, y*100))


class Queen(Piece):
    points = 8

    def __init__(self, x, y, is_black):
        super().__init__(x, y, is_black)
        if is_black:
            self.img = pygame.image.load('assets/queen_black.png')
        else:
            self.img = pygame.image.load('assets/queen_white.png')
        self.rect = self.img.get_rect(topleft=(x*100, y*100))


class King(Piece):

    def __init__(self, x, y, is_black):
        super().__init__(x, y, is_black)
        if is_black:
            self.img = pygame.image.load('assets/king_black.png')
        else:
            self.img = pygame.image.load('assets/king_white.png')
        self.rect = self.img.get_rect(topleft=(x*100, y*100))

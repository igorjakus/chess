import pygame


class Piece:
    hash_num = 0

    """ Parental class for all pieces """
    def __init__(self, color):
        self.color = color

    def moves(self, board):
        moves_list = []
        return moves_list


class Pawn(Piece):
    points = 1

    def __init__(self, color):
        super().__init__(color)
        if color:
            self.img = pygame.image.load('assets/pawn_white.png')
        else:
            self.img = pygame.image.load('assets/pawn_black.png')

    def moves(self, board):
        moves_list = []
        index = board.index(self)

        if self.color:
            # one square forward
            if board[index-8] is None:
                moves_list.append(index-8)

                # two squares forward
                if index // 8 == 6 and board[index-16] is None:
                    moves_list.append(index - 16)

            # taking enemy pieces
            for offset in [-7, -9]:
                square = index + offset
                if board[square] is not None:
                    if board[square].color != self.color:
                        if square % 8 - index % 8 in [-1, 1]:
                            moves_list.append(square)

        else:
            # one square forward
            if board[index+8] is None:
                moves_list.append(index+8)

                # two squares forward
                if index // 8 == 1 and board[index+16] is None:
                    moves_list.append(index + 16)

            # taking enemy pieces
            for offset in [7, 9]:
                square = index + offset
                if board[square] is not None:
                    if board[square].color != self.color:
                        if square % 8 - index % 8 in [-1, 1]:
                            moves_list.append(square)

        return moves_list


class Knight(Piece):
    points = 3

    def __init__(self, color):
        super().__init__(color)
        if color:
            self.img = pygame.image.load('assets/knight_white.png')
        else:
            self.img = pygame.image.load('assets/knight_black.png')

    def moves(self, board):
        moves_list = []
        index = board.index(self)

        offsets = [-17, -15, 15, 17, 10, 6, -10, -6]
        for move in offsets:
            square = index + move
            # skip out of board values
            if not 0 <= square <= 63:
                continue

            # if square is not the same color you can move here
            # when there is no piece, statement gives True
            if getattr(board[square], 'color', None) != self.color:
                if square % 8 - index % 8 in [-2, -1, 1, 2]:
                    moves_list.append(square)

        return moves_list


class Bishop(Piece):
    points = 3

    def __init__(self, color):
        super().__init__(color)
        if color:
            self.img = pygame.image.load('assets/bishop_white.png')
        else:
            self.img = pygame.image.load('assets/bishop_black.png')

    def moves(self, board):
        moves_list = []
        index = board.index(self)

        offsets = [-9, -7, 7, 9]
        for offset in offsets:
            square = index + offset
            while True:
                if 0 <= square <= 63:
                    if square % 8 - (square-offset) % 8 in [-1, 1]:
                        try:
                            if board[square].color != self.color:
                                moves_list.append(square)
                            break
                        except AttributeError:
                            moves_list.append(square)

                    else:
                        break

                else:
                    break
                square += offset

        return moves_list


class Rook(Piece):
    points = 5

    def __init__(self, color):
        super().__init__(color)
        if color:
            self.img = pygame.image.load('assets/rook_white.png')
        else:
            self.img = pygame.image.load('assets/rook_black.png')

    def moves(self, board):
        moves_list = []
        index = board.index(self)

        offsets = [-1, 1, -8, 8]
        for offset in offsets:
            square = index + offset
            while True:
                if 0 <= square <= 63:
                    if square % 8 - (square-offset) % 8 in [0, -1, 1]:
                        try:
                            if board[square].color != self.color:
                                moves_list.append(square)
                            break
                        except AttributeError:
                            moves_list.append(square)
                    else:
                        break

                else:
                    break
                square += offset

        return moves_list


class Queen(Piece):
    points = 8

    def __init__(self, color):
        super().__init__(color)
        if color:
            self.img = pygame.image.load('assets/queen_white.png')
        else:
            self.img = pygame.image.load('assets/queen_black.png')

    def moves(self, board):
        moves_list = []
        moves_list.extend(Bishop.moves(self, board))
        moves_list.extend(Rook.moves(self, board))
        return moves_list


class King(Piece):

    def __init__(self, color):
        super().__init__(color)
        if color:
            self.img = pygame.image.load('assets/king_white.png')
        else:
            self.img = pygame.image.load('assets/king_black.png')

    def moves(self, board):
        moves_list = []
        index = board.index(self)

        offsets = [-1, 1, -7, -8, -9, 7, 8, 9]
        for offset in offsets:
            square = index + offset
            if not 0 <= square <= 63:
                continue

            if getattr(board[square], 'color', None) != self.color:
                if square % 8 - index % 8 in [-1, 1]:
                    moves_list.append(square)

        return moves_list

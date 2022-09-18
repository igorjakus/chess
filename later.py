def square_to_index(square):
    """Returns index of board list for the given square

    Args:
        square (str):
            [first character is square file (letter from a to h)
            second character is square rank (number from 1 to 8)]

    Returns:
        [int]: [index (from 0 to 63) for given square]
    """
    # The files – going up to board – are labeled from a to h.
    square_file = square[0]

    # The ranks – going across the board – are from 1 to 8
    square_rank = square[1]

    return 8*(8-int(square_rank)) + ord(square_file)-97


def index_to_square(index):
    """Returns square name for the given index

    Args:
        index ([int]): [board list index from 0 to 63
                        0 is standing for a8 square
                        63 is standing for h1 square]

    Returns:
        [str]: [name of the square for the given index e.g. 'e4']
    """
    square_file = chr((index % 8) + 97)
    square_rank = index // 8
    return square_file + square_rank
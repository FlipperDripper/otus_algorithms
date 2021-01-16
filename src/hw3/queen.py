from ..test import test
from .rook import rook_movement
from .bishop import bishop_movement


def queen_movement(k):
    b_mask, b_count = bishop_movement(k)
    r_mask, r_count = rook_movement(k)
    mask = b_mask | r_mask
    count = b_count + r_count
    return mask, count


def format_output(output: str):
    count_of_steps, mask = output.split('\n')
    return int(mask), int(count_of_steps)


if __name__ == '__main__':
    t = test.Test(queen_movement, 'problems/3/5.Bitboard - Ферзь', int, format_output)
    t.start()

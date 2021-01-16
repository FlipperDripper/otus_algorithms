from ..test import test


def king_movement(k):
    position = 1 << k
    no_a = (1 << 0 | 1 << 8 | 1 << 16 | 1 << 24 | 1 << 32 | 1 << 40 | 1 << 48 | 1 << 56) ^ ((1 << 65) - 1)
    no_h = (1 << 7 | 1 << 15 | 1 << 16 | 1 << 23 | 1 << 31 | 1 << 39 | 1 << 48 | 1 << 55 | 1 << 63) ^ ((1 << 65) - 1)
    # В Python не происходит переполнения, поэтому добавил проверку
    no_top = (1 << 56 | 1 << 57 | 1 << 58 | 1 << 59 | 1 << 60 | 1 << 61 | 1 << 62 | 1 << 63) ^ ((1 << 65) - 1)
    mask = (
            ((no_a & no_top & position) << 7) | ((no_top & position) << 8) | ((no_top & no_h & position) << 9) |
            ((no_a & position) >> 1) | ((no_h & position) << 1) |
            ((no_a & position) >> 9) | (position >> 8) | ((no_h & position) >> 7)
    )
    n = mask
    count_of_steps = 0
    while n:
        a = n - 1
        n = n & a
        count_of_steps += 1
    return mask, count_of_steps


def format_output(output: str):
    count_of_steps, mask = output.split('\n')
    return int(mask), int(count_of_steps)


if __name__ == '__main__':
    t = test.Test(king_movement, 'problems/3/1.Bitboard - Король', int, format_output)
    t.start()

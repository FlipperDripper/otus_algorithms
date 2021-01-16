from ..test import test


def knight_movement(k):
    position = 1 << k

    no_a = 0xFeFeFeFeFeFeFeFe
    no_ab = 0xFcFcFcFcFcFcFcFc
    no_h = 0x7f7f7f7f7f7f7f7f
    no_gh = 0x3f3f3f3f3f3f3f3f

    mask = (no_gh & ((position << 6) | (position >> 10))
            | no_h & ((position << 15) | (position >> 17))
            | no_a & ((position << 17) | (position >> 15))
            | no_ab & ((position << 10) | (position >> 6))
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
    t = test.Test(knight_movement, 'problems/3/2.Bitboard - Конь', int, format_output)
    t.start()

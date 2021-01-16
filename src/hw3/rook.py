from ..test import test


def rook_movement(k):
    position = 1 << k
    x, y = k % 8, k // 8
    mask = 0

    for i in range(x, 0, -1):
        mask = mask | (position >> i)
    for i in range(1, 8 - x):
        mask = mask | (position << i)
    for i in range(y, 0, -1):
        mask = mask | (position >> (8 * i))
    for i in range (1, 8 - y):
        mask = mask | (position << (8 * i))

    return mask, 14


def format_output(output: str):
    count_of_steps, mask = output.split('\n')
    return int(mask), int(count_of_steps)


if __name__ == '__main__':
    t = test.Test(rook_movement, 'problems/3/3.Bitboard - Ладья', int, format_output)
    t.start()

from ..test import test


def bishop_movement(k):
    position = 1 << k
    x, y = k % 8, k // 8
    mask = 0

    # x -> 0; y -> 8; +7
    temp_x = x
    temp_y = y
    i = 1
    while temp_x > 0 and temp_y < 7:
        mask = mask | (position << (7 * i))
        temp_x -= 1
        temp_y += 1
        i += 1

    # x -> 8; y -> 8; +9
    temp_x = x
    temp_y = y
    i = 1
    while temp_x < 7 and temp_y < 7:
        mask = mask | (position << (9 * i))
        temp_x += 1
        temp_y += 1
        i += 1

    # x -> 0; y -> 0; -9
    temp_x = x
    temp_y = y
    i = 1
    while temp_x > 0 and temp_y > 0:
        mask = mask | (position >> (9 * i))
        temp_x -= 1
        temp_y -= 1
        i += 1

    # x -> 8; y -> 0; -7
    temp_x = x
    temp_y = y
    i = 1
    while temp_x < 7 and temp_y > 0:
        mask = mask | (position >> (7 * i))
        temp_x += 1
        temp_y -= 1
        i += 1

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
    t = test.Test(bishop_movement, 'problems/3/4.Bitboard - Слон', int, format_output)
    t.start()

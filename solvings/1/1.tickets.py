from test import test


# O(10^N)
def tickets(n: int) -> int:
    d = {}
    count = 0
    digit_sum = lambda num: sum(map(int, list(str(num))))
    for i in range(10 ** n):
        s = digit_sum(i)
        if s in d:
            d[s] += 1
        else:
            d[s] = 1
    for key in d:
        count += d[key] * d[key]
    print(d)
    return count


def tickets_fast(n: int) -> int:
    pass


if __name__ == '__main__':
    print(tickets(6))

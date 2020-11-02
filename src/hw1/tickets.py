from ..test import test

# O(10^N)
def tickets(n: int) -> int:
    d = {}
    count = 0
    def digit_sum(num): return sum(map(int, list(str(num))))
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
    arr = [1] * 10
    for _ in range(n - 1):
        arr = gen_array(arr)
    return sum([x * x for x in arr])

#O(n) ?
def gen_array(prev_array):
    delta_length = 9
    new_arr_len = len(prev_array) + delta_length
    new_arr = [None] * (new_arr_len)
    for i in range(new_arr_len, 0, -1):
        s = sum(prev_array[max(0, i - 10): i])
        new_arr[i - 1] = s
    return new_arr


if __name__ == '__main__':
    t = test.Test(tickets_fast, 'problems/1/1.Tickets', int, int)
    t.start()

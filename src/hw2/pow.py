from ..test import test
import math


def iter_pow(param):
    basis, exp = param
    r = 1
    for _ in range(exp):
        r *= basis
    return round(r, 11)


def two_exp(param):
    basis, exp = param
    if exp == 0:
        return 1
    two_exp_val = int(math.log(exp, 2))
    r = basis
    for i in range(two_exp_val):
        r *= r
    for i in range(exp - 2 ** two_exp_val):
        r = r * basis
    return round(r, 11)


def split_input(inp):
    basis, exp = str(inp).split('\n')
    return float(basis), int(exp)


def binary_decomposition(params):
    basis, exp = params
    res = 1
    bin_exp = 0

    while exp != 0:
        i = exp % 2
        if i == 1:
            part_res = basis
            for k in range(bin_exp):
                part_res *= part_res
            res *= part_res
        exp = exp // 2
        bin_exp += 1

    return round(res, 11)


if __name__ == '__main__':
    t = test.ComparableTest(
        {
            'iter_pow': iter_pow,
            'two_exp': two_exp,
            'binary_decomposition': binary_decomposition
        }, 'problems/2/3.Power', split_input, float)
    t.start()

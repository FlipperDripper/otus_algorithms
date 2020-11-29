from ..test import test
import math


def rec_fib(n):
    if n == 0:
        return 0
    if n < 3:
        return 1
    return rec_fib(n - 1) + rec_fib(n - 2)


def iterative_fib(n):
    if n == 0:
        return 0
    buffer = [0, 1]
    for i in range(n - 1):
        buffer = buffer[1:] + [buffer[0] + buffer[1]]
    return buffer[1]


def golden_section(n):
    fi = (1 + math.sqrt(5)) / 2
    return int((fi ** n) / math.sqrt(5) + 0.5)


def matrix_fib(n):
    if n == 0:
        return 0
    if n < 3:
        return 1
    matrix = [[1, 1], [1, 0]]
    result = [[1, 1], [1, 0]]
    for i in range(2, n):
        result = matrix_multiplication(result, matrix)
    return result[0][0]


def matrix_multiplication(first_matrix, second_matrix):
    result_matrix = []
    for (x, row) in enumerate(first_matrix):
        result_matrix.append([0] * len(row))
        for (y, col) in enumerate(second_matrix):
            result_matrix[x][y] = 0
            for i in range(len(row)):
                result_matrix[x][y] += row[i] * col[i]
    return result_matrix


if __name__ == '__main__':
    t = test.ComparableTest(
        {
            'Рекурсия': rec_fib,
            'Итерация': iterative_fib,
            'Золотое сечение': golden_section,
            'Матричное умножение': matrix_fib
        }, 'problems/2/4.Fibo', int, int)
    t.start()

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


def matrix_multiplication(M1, M2):
    a11 = M1[0][0] * M2[0][0] + M1[0][1] * M2[1][0]
    a12 = M1[0][0] * M2[0][1] + M1[0][1] * M2[1][1]
    a21 = M1[1][0] * M2[0][0] + M1[1][1] * M2[1][0]
    a22 = M1[1][0] * M2[0][1] + M1[1][1] * M2[1][1]
    r = [[a11, a12], [a21, a22]]
    return r


class MatrixFibonacci:
    Q = [[1, 1],
         [1, 0]]

    def __init__(self):
        self.__memo = {}

    def __get_matrix_power(self, M, p):
        """Возведение матрицы в степень (ожидается p равная степени двойки)."""

        if p == 1:
            return M
        if p in self.__memo:
            return self.__memo[p]
        K = self.__get_matrix_power(M, int(p / 2))
        R = matrix_multiplication(K, K)
        self.__memo[p] = R
        return R

    def get_number(self, n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        # Разложение переданной степени на степени, равные степени двойки,
        # т.е. 62 = 2^5 + 2^4 + 2^3 + 2^2 + 2^0 = 32 + 16 + 8 + 4 + 1.
        powers = [int(pow(2, b))
                  for (b, d) in enumerate(reversed(bin(n - 1)[2:])) if d == '1']

        matrices = [self.__get_matrix_power(MatrixFibonacci.Q, p)
                    for p in powers]
        while len(matrices) > 1:
            M1 = matrices.pop()
            M2 = matrices.pop()
            R = matrix_multiplication(M1, M2)
            matrices.append(R)
        return matrices[0][0][0]


if __name__ == '__main__':
    # решение с мемоизацией
    # работает быстрее на больших значениях
    m = MatrixFibonacci()
    t = test.ComparableTest(
        {
            'Рекурсия': rec_fib,
            'Итерация': iterative_fib,
            'Золотое сечение': golden_section,
            'Матричное умножение': matrix_fib,
            'Матричное умножение memo': m.get_number
        }, 'problems/2/4.Fibo', int, int)
    t.start()

from ..test import test
import math


def primes_iter(n: int) -> int:
    count = 0
    for i in range(2, n + 1):
        if is_prime(i):
            count += 1
    return count


def is_prime(n: int) -> bool:
    prime = True
    for i in range(2, n):
        if n % i == 0:
            prime = False
    return prime


def primes_iter_opt(n: int) -> int:
    count = 0
    prime_nums = []
    for i in range(2, n + 1):
        if is_prime_opt(i, prime_nums):
            prime_nums.append(i)
            count += 1
    return count


def is_prime_opt(n: int, prime_nums) -> bool:
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in prime_nums:
        if n % i == 0:
            return False
    return True


def sieve_erato_1(n: int):
    if n < 2:
        return 0
    arr = [True] * (n + 1)
    for i, val in enumerate(arr):
        if i < 2:
            continue
        if val:
            for j in range(i ** 2, n + 1, i):
                arr[j] = False
    return len(list(filter(bool, arr[2:])))


def sieve_erato_2(n: int):
    pr = []
    lp = [0] * (n + 1)
    count = 0
    for i in range(2, n +1):
        if lp[i] == 0:
            lp[i] = i
            count += 1
            pr.append(i)
        for p in pr:
            if p <= lp[i] and p * i <= n:
                lp[p * i] = p
            else:
                break
    return count


if __name__ == '__main__':
    t = test.ComparableTest(
        {
            'Итерация': primes_iter,
            'Оптимизированая итерация': primes_iter_opt,
            'Решето Эратосфена O(n log log n)': sieve_erato_1,
            'Решето Эратосфена O(n)': sieve_erato_2
        }, 'problems/2/5.Primes', int, int)
    t.start()

from ..test import test


def my_len(string: str) -> int:
    return len(string)


if __name__ == '__main__':
    t = test.Test(my_len, 'problems/1/0.String', None, int)
    t.start()

from typing import MutableSequence
from random import *


def bubble_sort(a: MutableSequence) -> None:
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1, i, -1):
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 10
    x = [None] * num

    print('버블 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')
    bubble_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

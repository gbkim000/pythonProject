from typing import MutableSequence
from random import *


def selection_sort(a: MutableSequence) -> None:
    n = len(a)
    for i in range(n - 1):
        min = i
        for j in range(i + 1, n):
            if a[j] < a[min]:
                min = j
            a[i], a[min] = a[min], a[i]


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 10
    x = [None] * num

    print('버블 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    selection_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

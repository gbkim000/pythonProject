from typing import MutableSequence
from random import *


def saker_sort(a: MutableSequence) -> None:
    left = 0
    right = len(a) - 1
    last = right
    while left < right:
        for j in range(right, left, -1):
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                last = j
        left = last

        for j in range(left, right):
            if a[j] < a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                last = j
        right = last


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 10
    x = [None] * num

    print('버블 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    saker_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

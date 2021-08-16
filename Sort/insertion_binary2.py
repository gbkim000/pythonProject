from typing import MutableSequence
from random import *
import bisect

def binary_insertion_sort2(a: MutableSequence) -> None:
    n = len(a)
    for i in range(1, n):
        bisect.insort(a, a.pop(i), 0, i)

if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('버블 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    binary_insertion_sort2(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

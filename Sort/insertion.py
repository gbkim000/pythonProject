from typing import MutableSequence
from random import *


def insertion_sort(a: MutableSequence) -> None:
    n = len(a)
    for i in range(1, n):
        j = i; tmp = a[i]
        while j > 0 and a[j - 1] > tmp:
            a[j] = a[j - 1]
            j = j - 1
        a[j] = tmp

if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 10
    x = [None] * num

    print('삽입 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    insertion_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

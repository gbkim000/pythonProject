from typing import MutableSequence
from random import *


def fsort(a: MutableSequence, max: int) -> None:
    n = len(a)
    f = [0] * (max + 1)
    b = [0] * n

    for i in range(n):              f[a[i]] += 1
    for i in range(1, max + 1):       f[i] += f[i - 1]
    for i in range(n - 1, -1, -1):    f[a[i]] -= 1; b[f[a[i]]] = a[i]
    for i in range(n):  a[i] = b[i]


def counting_sort(a: MutableSequence) -> None:
    fsort(a, max(a))


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('도수분포 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    print('\n오름차순으로 정렬합니다.')

    counting_sort(x)
    print('-' * 20)
    for i in range(num):
        print(f'x[{i}] = {x[i]}')

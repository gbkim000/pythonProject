from typing import MutableSequence
from random import *


def binary_insertion_sort(a: MutableSequence) -> None:
    n = len(a)
    for i in range(1, n):
        key = a[i]
        pl = 0
        pr = i - 1

        while True:
            mid = (pl + pr) // 2
            if a[mid] == key:
                break
            elif a[mid] < key:
                pl = mid + 1
            else:
                pr = mid - 1
            if pl > pr:
                break

        index = mid + 1 if pl <= pr else pr + 1

        for j in range(i, index, -1):
            a[j] = a[j - 1]
        a[index] = key


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('이진 삽입 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    binary_insertion_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

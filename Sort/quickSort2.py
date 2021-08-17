# import sys
# sys.path.append("C:\Users\FAMILY\PycharmProjects\pythonProject\chap04")
from random import *
from stack import Stack
from typing import MutableSequence


def qsort(a: MutableSequence, left: int, right: int) -> None:
    range = Stack(right - left + 1)
    range.push((left, right))

    while not range.is_empty():
        pl, pr = left, right = range.pop()
        x = a[(left + right) // 2]
        while pl <= pr:
            while a[pl] < x: pl += 1
            while a[pr] > x: pr -= 1
            if pl <= pr:
                a[pl], a[pr] = a[pr], a[pl]
                pl += 1
                pr -= 1
        if left < pr: range.push((left, pr))
        if pl < right: range.push((pl, right))


def quick_sort(a: MutableSequence) -> None:
    qsort(a, 0, len(a) - 1)


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('비재귀적 퀵 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    quick_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

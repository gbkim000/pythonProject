from typing import MutableSequence
from random import *


def sort3(arr: MutableSequence, a: int, b: int, c: int):
    if arr[b] < arr[a]: arr[b], arr[a] = arr[a], arr[b]
    if arr[c] < arr[b]: arr[c], arr[b] = arr[b], arr[c]
    if arr[b] < arr[a]: arr[b], arr[a] = arr[a], arr[b]
    return b


def insertion_sort(a: MutableSequence, left: int, right: int) -> None:
    for i in range(left + 1, right + 1):
        j = i
        temp = a[i]
        while j > 0 and a[j - 1] > temp:
            a[j] = a[j - 1]
            j -= 1
        a[j] = temp


def qsort(a: MutableSequence, left: int, right: int) -> None:
    if right - left < 9:
        insertion_sort(a, left, right)
    else:
        pl = left
        pr = right
        m = sort3(a, pl, (pl + pr) // 2, pr)
        x = a[m]
        a[m], a[pr - 1] = a[pr - 1], a[m]
        pl += 1
        pr -= 2

        while pl <= pr:
            while a[pl] < x: pl += 1
            while a[pr] > x: pr -= 1
            if pl <= pr:
                a[pl], a[pr] = a[pr], a[pl]
                pl += 1
                pr -= 1
        if left < pr: qsort(a, left, pr)
        if pl < right: qsort(a, pl, right)


def quick_sort(a: MutableSequence) -> None:
    qsort(a, 0, len(a) - 1)


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('재귀적 퀵 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    quick_sort(x)
    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

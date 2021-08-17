import sys
from random import *
from typing import MutableSequence

from stack import Stack


# sys.path.append("C:\\Users\\FAMILY\\PycharmProjects\\pythonProject\\") # 절대경로 지정
# from chap04.stack import Stack

def qsort(a: MutableSequence, left: int, right: int) -> None:
    sRange = Stack(right - left + 1)
    sRange.push((left, right))  # 스택에 튜플 '(left, right)' 값을 저장

    while not sRange.is_empty():
        pl, pr = left, right = sRange.pop()
        x = a[(left + right) // 2]
        while pl <= pr:
            while a[pl] < x: pl += 1
            while a[pr] > x: pr -= 1
            if pl <= pr:
                a[pl], a[pr] = a[pr], a[pl]
                pl += 1
                pr -= 1
        if left < pr: sRange.push((left, pr))
        if pl < right: sRange.push((pl, right))


# def quick_sort(a: MutableSequence) -> None:
#     qsort(a, 0, len(a) - 1)


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('비재귀적 퀵 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    # quick_sort(x)
    qsort(x, 0, len(x)-1)

    print()
    print('-' * 4 * num)

    for i in range(num):
        print(f'x[{i}] = {x[i]}')

from typing import MutableSequence
from random import *


def heap_sort(a: MutableSequence) -> None:
    def down_heap(a: MutableSequence, start: int, last: int) -> None:

        temp = a[start]
        parent = start

        while parent < (last + 1) // 2:
            left = parent * 2 + 1
            right = left + 1
            child = right if right <= last and a[right] > a[left] else left
            if temp >= a[child]:
                break
            a[parent] = a[child]
            parent = child
        a[parent] = temp

    # end def _down_heap

    n = len(a)

    for i in range((n - 1) // 2, -1, -1):
        down_heap(a, i, n - 1)

    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        down_heap(a, 0, i - 1)

if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('힙(heap) 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    print('\n오름차순으로 정렬합니다.')

    heap_sort(x)
    print('-' * 20)
    for i in range(num):
        print(f'x[{i}] = {x[i]}')


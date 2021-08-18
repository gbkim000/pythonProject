from typing import MutableSequence
from random import *


def merge_sort(a: MutableSequence) -> None:

    def _mSort(a: MutableSequence, left: int, right: int) -> None:
        if left < right:
            center = (left + right) // 2
            _mSort(a, left, center)
            _mSort(a, center + 1, right)

            p = j = 0
            i = k = left

            while i <= center:
                buff[p] = a[i]
                p += 1
                i += 1

            while i <= right and j < p:
                if buff[j] <= a[i]:
                    a[k] = buff[j]
                    j += 1
                else:
                    a[k] = a[i]
                    i += 1
                k += 1

            while j < p:
                a[k] = buff[j]
                k += 1
                j += 1
    # end def _mQsort

    n = len(a)
    buff = [None] * n
    _mSort(a, 0, n - 1)
    del buff


if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('병합 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    print('\n오름차순으로 정렬합니다.')

    merge_sort(x)
    print('-' * 20)
    for i in range(num):
        print(f'x[{i}] = {x[i]}')

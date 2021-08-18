from typing import MutableSequence
from random import *

if __name__ == '__main__':

    # num = int(input(('정렬할 자료 갯수: ')))
    num = 100
    x = [None] * num

    print('파이썬 내장함수로 정렬을 수행합니다.')
    for i in range(num):
        # x[i] = int(input(f'x[{i}:] '))
        x[i] = randint(1, 100)
        print(f'{x[i]:4}', end='')

    print('\n오름차순으로 정렬합니다.')
    x=sorted(x)
    print('-' * 20)
    for i in range(num):
        print(f'x[{i}] = {x[i]}')

    print('\n내림차순으로 정렬합니다.')
    x=sorted(x, reverse=True)
    print('-' * 20)
    for i in range(num):
        print(f'x[{i}] = {x[i]}')

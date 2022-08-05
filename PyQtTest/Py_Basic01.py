# %% 파인썬 변수의 유효 범위 예제

print('----------------------------------------------')
lang = 'jython'
def func():
    lang = 'python'
    print(lang)     # python
 
func()
print(lang)         # jython

print('----------------------------------------------')
lang = 'jython'
def func():
    global lang 
    lang = 'python'
    print(lang)     # python

func()
print(lang)         # python

print('----------------------------------------------')
def func():
    var = 1
    def func2():
        nonlocal var
        var = 3
    func2()
    print(var)      # 3
func()

print('----------------------------------------------')
def outer_func():
    a = 20
    def inner_func():
        a = 30
        print("a = %d" % a)     # a = 30
    inner_func()
    print("a = %d" % a)         # a = 20
a = 10
outer_func()
print("a = %d" % a)             # a = 10

# %% 파이썬 변수 선언과 네임스페이스

# 파이썬 변수는 로컬변수, 정적변수, 인스턴스변수, 클래스변수 등이 있다.
# 그런데 파이썬은 변수 선언문을 직접 명시하지 않기 때문에, 
# 변수의 네임스페이스는 대입이 한 번이라도 일어난 최초의 네임스페이스에 공간을 정한다.
# self.을 생략하게되면 로컬 네임스페이스와 인스턴스 네임스페이스가 섞이게 된다.
# 즉 클래스에서 x = 1하면 이게 로컬로 갈 지, 인스턴스로 갈지 모호해 진다.

a = 3
c = 'Hello'
def func():
    a = 100
    b = 'python'
    print('func 함수 locals', locals())       # {'a': 100, 'b': 'python'}
    def inner_func():
        a1 = 200
        b1 = 'Python Advanced'
        print('inner_func locals', locals())  # {'a1': 200, 'b1': 'Python Advanced'}
    inner_func()

func()
print('함수 외부 globals', globals()) # {'__name__': '__main__', '__builtin__': <module 'builtins ...
print('-' * 10)

# %% tuple / list

print(tuple((i for i in range(10) if i%2 == 0)))

a = (1.2, 2.5, 3.7, 4.6)
a = list(map(int, a))
print(a)
print('-'*30)

a = [[10,20],
     [500,600,700],
     [9],
     [30,40],
     [8],
     [800,900,1000]]

from pprint import pprint
pprint(a, indent = 4, width = 30)

for i in a:
    print(i)
    
# %% deepcopy()

a = [[10,20],[30,40]]
b = a
b[0][0] = 500
print(a)
print(b)
print()

import copy
b = copy.deepcopy(a)
b[0][0] = 300
print(a)
print(b)

# %% strip 함수

s = ', python. '
print(s)
s = s.strip(',. ')
print(s)

import string
s = ', python. '
s = s.strip(string.punctuation+' ')
print(s)

# %% collections 모듈 사용하기

import math
import collections

Point2D = collections.namedtuple('Point2D', ['x','y'])

p1 = Point2D(x = 30, y = 20)
p2 = Point2D(x = 60, y = 50)

a = p1.x - p2.x
b = p1.y - p2.y

c = math.sqrt(a*a + pow(b, 2))
print(c)

# %% 언더스코어('_')의 사용 

for _ in range(5): # 단순히 5번 반복할 목적으로 
    print('hello world') 

for _ in range(3): # _를 i로 바꿔서 보면 우리에게 익숙한 표현식일 것이다. 
    print(_) 
    
def values(): 
    return (1,2,3,4) # 튜플을 반환
a, b, _, _ = values() # 반환된 튜플중에서 앞의 2개의 값만 사용
print(a,b)

# %% 다른 모듈에서 임포트하기를 원하지 않을 때 ------------

# func.py ------------------------
def publicFunc(): 
    print('this is public function') 
    
def _privateFunc(): 
    print('this is private function')

# test1.py ------------------------
from func import * 

publicFunc()        # 이 함수는 잘 실행됨
# _privateFunc()    # 여기서 오류 발생, '_'로 시작하는 메소드는 import에서 가져올 수 없음.


# %% private 변수를 사용하고자 할 때 -----------------------

# order.py 
class Order: 
    
    def __init__(self): 
        self.coffee = 'Americano' 
        self.__price = 3000 
        
    def printInfo(self): 
        print(f"coffee : {self.coffee}") 
        print(f"price : {self.__price}")

# test2.py 
import order 
order1 = order.Order() 

print(order1.coffee)    # 이 문장은 잘 실행됨
#print(order1.__price)  # 여기서 오류 발생, '__'로 시작하는 private 변수는 외부접근 불가.

# %%

g = (i for i in range(50) if i %2 == 0)
print(g)
print(list(g))

g = (i for i in range(50) if i %2 == 0)
print(*g)

# %% is 연산자(객체가 같은지를 비교)
a = []
b = []
c = a

result = (a is b)
print("a is b ?", result)

result = (a is c)
print("a is c ?", result)

result = (b is c)
print("b is c ?", result)

# %% == 연산자(값이 같은지를 비교)
a = []
b = []
c = a

result = (a == b)
print("a == b ?", result)

result = (a == c)
print("a == c ?", result)

result = (b == c)
print("b == c ?", result)

# %% 리스트에 filter()를 사용하는 예제

# 일반함수로 구현
def myFunc(num):
    return num > 25

numbers = [20, 10, 44, 12, 34, 40]
filtered_iter = filter(myFunc, numbers)
filtered_list = list(filtered_iter)
print(filtered_list)

# lamda 함수로 구현
numbers = [20, 10, 44, 12, 34, 40]
filtered_iter = filter(lambda num: num > 25, numbers)
filtered_list = list(filtered_iter)
print(filtered_list)

# %% reduce()로 리스트의 모든 요소의 합 계산

from functools import reduce

def sum(a, b):
    print(f"[a = {a}, b = {b}], sum = {a} + {b} = {a+b}")
    return a + b

numbers = [1, 2, 3, 4, 5]
total = reduce(sum, numbers)
print(f"total = {total}")
    
# %% reduce()와 lambda
from functools import reduce

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, numbers)
print(f"total = {total}")

# %% reduce()로 최대 값 계산

from functools import reduce

def max(a, b):
    if a > b:
        return a
    else:
        return b

numbers = [10, 21, 421, 223, 52]
max_value = reduce(max, numbers)
print(f"max_value = {max_value}")

numbers = [10, 21, 421, 223, 52]
max_value = reduce(lambda a, b: a if a > b else b, numbers)
print(f"max_value = {max_value}")

# %% dict 정렬 (Key, Value로 sorting)

my_dict = {'c': 3, 'a': 1, 'b': 2, 'e': 1, 'd': 2}

sorted_dict = sorted(my_dict.items())
print(sorted_dict)

# key를 기준으로 내림차순 정렬
sorted_dict = sorted(my_dict.items(), key = lambda item: item[0], reverse = True)
print(sorted_dict)

# Value를 기준으로 정렬 (오름차순)
sorted_dict = sorted(my_dict.items(), key = lambda item: item[1])
print(sorted_dict)

# Value를 기준으로 정렬 (내림차순)
sorted_dict = sorted(my_dict.items(), key = lambda item: item[1], reverse = True)
print(sorted_dict)

# %% 문자열 검색 및 치환

## 방법 1.
title = '라이프사이즈900*6001팩 - 구입'
special_char = '\/:*?"<>|'
for c in special_char:
    if c in title:
        print(title.find(c), c)
        title = title.replace(c, 'x')
print(title)
# 라이프사이즈900x6001팩 - 구입


## 방법 2.
specialChar = '!@#$%^&*()_{}[]\|;:''"<>?/'
title2 = '[라이프사이즈]900*6001팩 - 구입?'
for i in range(len(specialChar)):
    title2 = title2.replace(specialChar[i], '')
print(title2)
# 라이프사이즈9006001팩 - 구입


## 방법 3.
title2 = ''.join(c for c in title2 if c not in specialChar)
print(title2)
# 라이프사이즈9006001팩 - 구입


## 방법 4.
# isalnum() 함수(문자열의 모든 요소가 문자 또는 숫자인 경우 True) - 단, 공백도 없어짐
title3 = '[라이프사이즈] <900 * 6001> 팩 - 구입?'
ntitle = ''
for c in title3:
    if c.isalnum():
        ntitle += c
print(ntitle)
# 라이프사이즈9006001팩구입

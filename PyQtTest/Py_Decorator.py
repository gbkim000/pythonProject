# %% 데코레이터 - "함수를 인수로 얻고 대가로 새로운 함수로 돌려주는 cllable(*)"
# 출처: https://engineer-mole.tistory.com/181 [매일 꾸준히, 더 깊이:티스토리]

def outer(x):
    def inner():
        print(x)
    return inner

print1 = outer(10)
print2 = outer(20)
print1()
print2()

# %% 데코레이터

def outer(some_func):
    def inner():
        print("before some_func")
        ret = some_func() #1
        return ret + 1
    return inner

def foo():
    return 1

decorated = outer(foo) #2
retVal = decorated()
print(retVal)

# %% 데코레이터 사용
# 출처: https://ybworld.tistory.com/108 [투손플레이스]

import time

#데코레이터 함수 정의 
def decoFunction(inputFunc): #원래 함수를 매개변수로 입력 받음 
    def clock(number, distance): # wrapper() 함수 정의
        start_time = time.time() 
        inputFunc(number, distance) #원래 함수 
        end_time = time.time() 
        print("걸린시간 : ", end_time - start_time)
    return clock #wrapper라는 함수를 리턴 

#데코레이터 사용 
@decoFunction 
def race(number : int, distance : int): 
    print(str(number)+"번 경주마가 출발했습니다.") 
    for n in range(0, distance): 
        print(str(n)+"km 달리는 중입니다.") 
        time.sleep(0.5) 
    print("경주마가 결승선에 도착했습니다.") 

if __name__ == "__main__": 
    race(1, 7)
        
# %% 데코레이터
# 출처: https://engineer-mole.tistory.com/181 [매일 꾸준히, 더 깊이:티스토리]

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        # self.__dict__ 메서드는 객체의 속성들을 담고 있는 딕셔너리 자료임.
        return "Coord: " + str(self.__dict__) # __dict__
    
def add(a, b):
    return Coordinate(a.x + b.x, a.y + b.y)

def sub(a, b):
    return Coordinate(a.x - b.x, a.y - b.y)

one = Coordinate(100, 200)
two = Coordinate(300, 200)
three = Coordinate(-100, 300)

# r1, r2, r3의 id값은 모두 다름.
r1 = add(one, two)
r2 = sub(one, two)
r3 = sub(one, three)

# 위 클래스에서 __repr__(self) 메서드를 삭제하면 아래 문장은 id값을 출력함.
print(r1)
print(r2)
print(r3)
print('------------------------------------------------')
print(add(one, two))
print(sub(one, two))
print(sub(one, three))
print('------------------------------------------------')

def Wrapper(func):
    def checker(a, b):
        
        # 전달받은 인수의 x, y값이 음수이면 0으로 치환
        if a.x < 0 or a.y < 0:
            a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
        if b.x < 0 or b.y < 0:
            b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
        
        # 원래 함수 호출
        ret = func(a, b)

        # 결과 값이 음수이면 0으로 치환
        if ret.x < 0 or ret.y < 0:
            ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
        
        # 최종 결과 반환
        return ret
    return checker

add = Wrapper(add)
sub = Wrapper(sub)

print(add(one, two))
print(sub(one, two))
print(sub(one, three))

# %%

def outer_function(msg):
    def inner_function():
        print(msg)
    return inner_function

hi_func = outer_function('Hi')
bye_func = outer_function('Bye')

hi_func()
bye_func()

# %% 데코레이터 - "함수를 인수로 얻고 대가로 새로운 함수로 돌려주는 cllable(*)"

def decorator_function(original_function):  # 1
    def wrapper_function():  # 5
        return original_function()  # 7
    return wrapper_function  # 6

def display():  # 2
    print('display 함수가 실행됐습니다.')  # 8

decorated_display = decorator_function(display)  # 3
decorated_display()  # 4

# %% 일반 함수 데코레이터 사용하기(인수 없음)
def decorator_function(original_function):
    def wrapper_function():
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return original_function()
    return wrapper_function

@decorator_function  # 1
def display_1():
    print('display_1 함수가 실행됐습니다.')

@decorator_function  # 2
def display_2():
    print('display_2 함수가 실행됐습니다.')

# display_1 = decorator_function(display_1)  # 3
# display_2 = decorator_function(display_2)  # 4

display_1()
print()
display_2()

# %% 일반 함수 데코레이터 사용하기(인수 있음)

def Decorator_function(original_function):
    def wrapper_function(*args, **kwargs):  #1
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return original_function(*args, **kwargs)  #2
    return wrapper_function

@Decorator_function
def display():
    print('display 함수가 실행됐습니다.')

@Decorator_function
def display_info(name, age):
    print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

display()
print()
display_info('John', 25)

# %% 클래스 형식의 데코레이터 사용하기

class DecoratorClass:  # 1
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print('{} 함수가 호출되기전 입니다.'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)

@DecoratorClass  # 2
def display():
    print('display 함수가 실행됐습니다.')

@DecoratorClass  # 3
def display_info(name, age):
    print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

display()
print()
display_info('John', 25)



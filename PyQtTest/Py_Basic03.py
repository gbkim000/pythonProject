# %% QObject 사용하는 singleton 객체 만들기
# https://freeprog.tistory.com/364  : QObject 사용하는 singleton 만들기
# https://wikidocs.net/3693         : 여러가지 싱글톤(singleton) 구현방법
# https://wikidocs.net/book/536     : Python Snippets - 파이썬 조각 코드 모음집

from PyQt5.QtCore import QObject

class QtSingleton(QObject):
    __instance = None

    # def __init__(self, *args, **kwargs):
    # #def __init__(self): 
    #     super().__init__()
        
    def __new__(cls, *args, **kwargs):
        print("From new ---------------------------------------------------")
        print(cls)      # 클래스 이름('__main__.AA')이 출력됨
        print(args)     # 빈 튜플 '()'이 출력됨, AA()클래스의 init 메서드의 인수값이 없으므로
        print(kwargs)   # 빈 딕셔너리 '{}'가 출력됨, AA()클래스의 init 메서드에 arg='값' 형태의 인수가 없으므로
 
        # cls.__instance가 존재하지 않으면 새로 생성, 그렇지 않으면 기존 인스턴스를 리턴함(싱글톤)
        if not isinstance(cls.__instance, cls):
            # cls.__instance = QObject.__new__(cls, *args, **kwargs)
            # cls.__instance = super().__new__(cls, *args, **kwargs)
            # cls.__instance = super().__new__(cls)
            cls.__instance = QObject.__new__(cls, *args, **kwargs)            
        return cls.__instance # 인스턴스의 주소를 리턴함.
        
        # obj = super().__new__(cls)
        # # obj = QObject.__new__(cls)
        # return obj

class AA(QtSingleton): # QtSingleton 클래스 상속
    def __init__(self, *args, **kwargs):
    # def __init__(self): 
        # super().__init__()
        self.num = 123
        self.city = kwargs['city']

class KK:   # 상속 없음.
    def __init__(self, *args, **kwargs):
    # def __init__(self):
        self.num = 456
        self.city = kwargs['city']
            
if __name__ == "__main__":
    print("\n< Singletone 사용한 경우 : aa,bb 객체 주소와 값이 동일함 >")
    aa = AA(1, 2, city = 'Seoul')
    bb = AA(city = 'Jeonju')
    print('aa:', aa)
    print('bb:', bb)

    print('aa.num:', aa.num)
    print('bb.num:', bb.num)
    print('aa.city:', aa.city)
    print('bb.city:', bb.city)
    
    aa.num = 3
    bb.city = 'Daejon'
    print('aa.num:', aa.num)
    print('bb.num:', bb.num)
    print('aa.city:', aa.city)
    print('bb.city:', bb.city)
    
    print("\n< Singleton 아닌 경우 : kk,mm 객체 주소와 값이 서로 다름 >")
    kk = KK(1, 2, city = 'Seoul')
    mm = KK(city = 'Jeonju')
    print('kk:', kk)
    print('mm:', mm)
    
    print('kk.num:', kk.num)
    print('mm.num:', mm.num)
    print('kk.city:', kk.city)
    print('mm.city:', mm.city)
    
    kk.num=5
    mm.city = 'Daejon'
    print('kk.num:',kk.num)
    print('mm.num:',mm.num)
    print('kk.city:', kk.city)
    print('mm.city:', mm.city)    


# %% 파이썬의 객체 생성 과정 
# __new__() 메소드 실행후 객체를 반환, 그리고 __init__() 메소드 실행됨

from PyQt5.QtCore import QObject

class Point(QObject):
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        print("\nFrom __new__")
        print(cls)
        print(args)
        print(kwargs)
        
        # create our object and return it
        obj = super().__new__(cls)
        # obj = QObject.__new__(cls)
        return obj
    
        # return cls # 이 경우 클래스 자체를 리턴한다. id(p1), id(p2)가 동일
        # if not isinstance(cls.__instance, cls):
        #     cls.__instance = QObject.__new__(cls, *args, **kwargs)
        # return cls.__instance
    
    def __init__(self, x = 0, y = 0):
        print("\nFrom __init__")
        self.x = x
        self.y = y
      
    def __call__(self, x, y):
        print('\nFrom __call__')
        self.x = x
        self.y = y
        
p1 = Point(1, 2)
p2 = Point(3, 4)

print('p1:', p1)
print('p2:', p2)

print('p1:', p1.x, p1.y)
print('p2:', p2.x, p2.y)

p1(5, 6) # __call__ 함수 호출됨(p1 객체를 마치 p1() 함수처럼 사용가능하게 해줌)
print('p1:', p1.x, p1.y)

p2(10, 20)
print('p2:', p2.x, p2.y)


# %% static method 예제(1)
class Calc:
    @staticmethod
    def add(a, b):
        print(a + b)

Calc.add(10, 20)
a = Calc()
a.add(10, 20) # 인스턴스 a에는 add()함수가 없으므로 바깥쪽의 클래스 이름 공간에서 찾음.


# %% class method 예제(2)
import sys, inspect

class Person:
    cnt = 0
    def __init__(self):
        Person.cnt += 1
        
    @classmethod
    def print_count(cls):
        print('{0}명 생성...'.format(cls.cnt))
    
    @classmethod
    def mul(cls, a, b):
        print(cls)      # <class '__main__.Person'>
        p = cls()       # 인스턴스 p 생성, 'cls'는 다른 문자열로 대체해도 동일함.
        print(p)
        print("p.cnt =", p.cnt)
        print("cls.cnt =", cls.cnt)
        print("a*b =", a*b)
        
james = Person()
maria = Person()

Person.print_count()    # 2명 생성
print(Person.cnt)       # 2
print('-------------------------------------')
Person.mul(10, 20)
Person.print_count()    # 3명 생성
print(Person.cnt) 


# %% 클래스 변수 예제
# '클래스.power'와 '인스턴스.power'가 서로 다른 변수임.
# 인스턴스 공간에 변수가 없으면 클래스 공간에서 찾음
# 인스턴스 변수는 클래서 초기화 함수 뿐마아니라 다른 임의 위치에서도 생성 가능

class Human:
    power = 5
 
    def __init__(self, name, age):
        self.name = name
        self.age = age
        # self.power = 500
        
    def info(self):
        print("Human.power=", Human.power)
        print("나의 이름은", self.name, "나이는", self.age, "입니다", "힘은", self.power, "입니다.")

man1 = Human("짱구", 10)
man2 = Human("철수", 12)
print("Human.power=", Human.power)  # 5 : Human 클래스 공간에 있는 power 참조
print("man1.power =", man1.power)   # 5 : man1 공간에 power가 없으므로 클래스 공간 참조

man1.power += 10    # 이 시점에서 man1.power라는 인스턴스 변수 생성, 원래값+10의 결과가 저장
man2.power += 20    # 이 시점에서 man2.power라는 인스턴스 변수 생성, 원래값+20의 결과가 저장
Human.power += 100  # 클래스 변수의 값을 100 증가 (5 -> 105)
man3 = Human("길동", 13)

man1.info()  # Human.power = 105, name = '짱구', age = 10, power = 15
man2.info()  # Human.power = 105, name = '철수', age = 12, power = 25
man3.info()  # Human.power = 105, name = '길동', age = 13, power = 105

print("Human.power=", Human.power)  # 105
print("man1.power =", man1.power)   # 15
print("man2.power =", man2.power)   # 25
print("man3.power =", man3.power)   # 105 :  man3 공간에는  power가 없으므로 클래스 공간에서 찾음


# %% 클래스 변수, 인스턴스 변수 접근하기

class Aclass:
    a1 = 1  # 클래스 변수 선언
    a2 = 2
    a3 = 3

class Bclass:
    def __init__(self): 
        self.a1 = 11    # 인스턴스 변수 선언
        self.a2 = 12
        self.a3 = 13

a = Aclass()    # 인스턴스 a 생성
b = Bclass()    # 인스턴스 b 생성

print('\nAclass member:', end='')
for k in a.__dict__: 
    print (k, end=" ")
#(결과) A member:
print('\n', a.a1, Aclass.a2, Aclass.a3)     #인스턴스명.변수 or 클래스명.변수

print('\nBclass member:', end='')
for k in b.__dict__:
# for k, v in b.__dict__.items(): #keys, values
    print (k, end=" ")
#(결과) B member:a1 a2 a3 
print('\n', b.a1, b.a2, b.a3)   # 인스턴스명.변수

# %% iterator 속성 부여하기
class Counter:
    
    def __init__(self, stop):
        self.current = 0
        self.stop = stop
        
    # def __iter__(self):
    #     return self
    
    # def __next__(self):
    #     if self.current<self.stop:
    #         r=self.current
    #         self.current+=1
    #         return r
    #     else:
    #         raise StopIteration
            
    def __getitem__(self, index):   # __iter__, __next__ 없어도 됨
        if index < self.stop:
            return index
        else:
            raise IndexError
            
print(Counter(3)[0], Counter(3)[1], Counter(3)[2])

for i in Counter(5):    # Counter 클래스는 위에서 반복 기능이 부여되었음
    print(i, end=' ')


# %% iterator
    
it = iter(range(5))
print(it)
print(list(it))
print(*list(it))

it = iter(range(5))
for i in range(0, 5):
    print(next(it), end= ' ')
print()

it = iter(range(5))
for i in it:
     print(i, end=' ')
print()

print('*list(it) = ', *list(it))
    
# %% generator
def number_generator(stop):
    n = 0              # 숫자는 0부터 시작
    while n < stop:    # 현재 숫자가 반복을 끝낼 숫자보다 작을 때 반복
        yield n        # 현재 숫자를 바깥으로 전달
        n += 1         # 현재 숫자를 증가시킴

for i in number_generator(3):
    print(i)


def upper_generator(x):
    for i in x:
        yield i.upper()    # 함수의 반환값을 바깥으로 전달

fruits = ['apple', 'pear', 'grape', 'pineapple', 'orange']
g = upper_generator(fruits)

for i in g:
    print(i)


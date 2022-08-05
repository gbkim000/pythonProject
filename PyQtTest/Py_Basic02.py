# %% 초기화 함수를 사용하여 멤버 변수 생성
class FourCal:
    def __init__(self, first, second):
        self.first = first
        self.second = second
        
    def printData(self):
        print(self.first, self.second)
        
a1 = FourCal(10,20)
a1.printData()
print(a1.first, a1.second)
print()

a2 = FourCal(20,30)
a2.printData()
print(a2.first, a2.second)

# %% 초기화 함수 사용하지 않고 멤버변수 생성
class FourCal:
    def setdata(self, first, second):
        self.first = first
        self.second = second
    
    def printData(self):
        print(self.first, self.second)
        
a1 = FourCal()
a1.setdata(10, 20)             # 인스턴스명으로 메서드에 접근
a1.printData()
print(a1.first, a1.second)
print()

a2 = FourCal()
FourCal.setdata(a2, 20, 30)    # 클래스명으로 메서드에 접근
a2.printData()
print(a2.first, a2.second)


# %% abstractmethod
from abc import *

class StudentBase(metaclass = ABCMeta):
    @abstractmethod
    def study(self):
        pass

    @abstractmethod
    def gotoScool(self):
        pass

class Student(StudentBase):
    def __init__(self):
        print('안녕하세요')
        
    def study(self):
        print('공부하기')
        
    def gotoScool(self):
        print('학교가기')
        
james = Student()
james.study()
james.gotoScool()

# %%

class A:
    def __init__(self):  
        self.a = 10     # 인스턴스 변수('객체명.a'로 접근)
        self.setUI()
            
    def setUI(self):
        self.b = 20     # 인스턴스 변수('객체명.b'로 접근)
        d = 40          # d : 이 함수 내부에서만 유효한 지역변수
        self.func1(d)
    
    def func1(self, d):
        self.c = d      # 인스턴스 변수('객체명.c'로 접근)
        
v1 = A()
v2 = A()
v1.c = 50

print(v1.a, v1.b, v1.c)
print(v2.a, v2.b, v2.c)

# %% *args와 **kwargs
            
def nameSplit(*names):
    for name in names:
        print("%s:%s" % (name[0], name[1:]))

nameSplit('홍길동')
nameSplit('이천수','안정환', '홍명보')

def fruitInfo(**kwargs):
    for key, value in kwargs.items():
        #print('{0} : {1}'.format(key, value))
        print(f'{key} : {value}')
        
fruitInfo(apple = 1000, orange = 500, banana = 300)
print()
fruits = {'apple': 500, 'orange':300}
fruitInfo(**fruits)

# %% str, __str__(), repr, __repr__()
# https://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__

'''
# __str__, __repr__의 공통점 : 두 메소드는 객체의 문자열 표현을 반환한다.
# __str__는 태생적인 목적 자체가 인자를 ‘문자열화’해 반환하라는 것이다.
# __str__ 메소드는 interface로서의 역할을 수행하기 위해 존재합니다. 
# 즉, 서로 다른 타입을 가진 데이터끼리 상호작용 할 때 문자열로 변환시킴으로서 상호간의 호환이 가능하도록 만들어줍니다
# __repr__은 본 목적이 객체를 인간이 이해할 수 있는 평문으로 ‘표현’하라는 것이다.
# repr 함수는 어떤 객체의 ‘출력될 수 있는 표현’(printable representation)을 문자열의 형태로 반환한다.
'''
import math

print(repr(3))          # type : <class 'str'>
print(repr([1, 2, 3]))  # type : <class 'str'>
print(repr(math))       # type : <class 'str'>
print()

print(str(3)) # print 함수는 내부적으로 __str__를 호출합니다.
print(str([1, 2, 3]))
print(str(math))
print()

class A:
    def hello(self):
        print('hello')
        
    def __str__(self):
        return 'str method is called'

    def __repr__(self):
        return 'repr method is called'

a = A()
 
print(str(a))   # str method is called
print(repr(a))  # repr method is called
print(a)        # str method is called

# %% __str__과 __repr__의 차이
# https://tibetsandfox.tistory.com/39

'''
1. 파이썬에 존재하는 str() 메소드와 repr()메소드에 객체를 주고 실행하면 
   내부적으로 해당 객체의 __str__ 메소드와 __repr__ 메소드를 실행합니다.
   
2. __str__ 메소드를 정의하지 않았다면 __repr__ 메소드가 대신 쓰입니다. 
   __str__ 메소드가 정의되었다면 __str__ 메소드를 사용합니다.
   
3. __str__메소드는 정의되었는데 __repr__ 메소드를 정의하지 않은 상태로 repr()메소드를 사용하면 
   __str__메소드를 대신 사용하지 않고 __repr__ 메소드의 디폴트 값을 사용합니다.
   
4. __str__ 메소드의 반환값은 informal, __repr__ 메소드의 반환값은 formal 하다고 표현하기도 합니다.
'''

class Test:
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Hello, my name is {self.name}"

a = 1
b = "hi"
c = [1, 2, 3]
test_ = Test("fox")
print(a, b, c, test_)

# %% 상속 예제
# https://rednooby.tistory.com/56 [개발자의 취미생활]

class Father():  # 부모 클래스
    def __init__(self, who):
        self.who = who
 
    def handsome(self):
        print("{}를 닮아 잘생겼다".format(self.who))
 
class Sister(Father):  # 자식클래스(부모클래스) father 메소드를 상속
    def __init__(self, who, where):
        super().__init__(who)
        #super(sister, self).__init__(who)
        self.where = where
 
    def choice(self):
        print("{} 말이야".format(self.where))
 
    def handsome(self):
       super().handsome()
       self.choice()
 
girl = Sister("엄마", "얼굴")
girl.handsome()


# %% 한글 <--> 영어 단어 맞추기
import random

menus = [(1,'영어->한글'), (2,"한글->영어"), (3,'종료')]
english_list = ['apple','bed','clock','cat','dog']
hangul_list  = ['사과','침대','시계','고양이','개']

while True:
    for i, n in menus:
        print(i, n)
    c = int(input(">"))
    # print(c)

    if c == 1:
        n = random.randrange(5)
        eng_word = english_list[n]
        print('영어', eng_word,'의 뜻?')
        kor_word = input()
        
        if kor_word == hangul_list[n]:
            print("네 맞았어요.", eng_word,"의 뜻은 한글로 ", kor_word,"입니다")
        else:
            print("틀렸습니다")

    elif c == 2:
        n = random.randrange(5)
        kor_word = hangul_list[n]
        print(kor_word,'은 영어로 무엇?')
        eng_word = input()
        
        if eng_word == english_list[n]:
            print("네 맞았어요.", kor_word,"은 영어로 ",eng_word,"입니다")
        else:
            print("틀렸습니다")

    elif c == 3:
        break

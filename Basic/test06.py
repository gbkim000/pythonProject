class Shape:
    
    area = 0

    def __add__(self, other): #self는 관례적으로 사용, 다른이름으로 변경도 가능.
        return  self.area+other.area
    
if __name__ == '__main__':
    a=Shape()
    a.area=20
    b=Shape()
    b.area=10
    print(a+b)
    print(a.__add__(b))
    print('-------------------------------------------------')

##########################################
class A:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        print("init")

    def __call__(self, x, y):
        self.x=x
        self.y=y
        print("call")
a=A(1,2)
a(2,3)
print(a.x, a.y)
print('-------------------------------------------------')

##########################################
class Point():
    def __new__(cls, *args, **kwargs):
        print("From new")
        print(cls)
        print(args)
        print(kwargs)
        # create our object and return it
        obj = super().__new__(cls)
        return obj
    def __init__(self, x = 0, y = 0):
        print("From init")
        self.x = x
        self.y = y
p1=Point(3,4)
p2=Point(1,2)
print('-------------------------------------------------')        
##########################################        


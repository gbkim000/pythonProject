class Person:
    name = None
    
    def __init__(self, name): # constructor
        self.name = name
        
    def __get_trailing_text(self): # private method
        return "Nice to meet you !!!"
    
    def _hello(self): # protected method
        return "Hello {}, {}".format( self.name, self.__get_trailing_text())
    
    def hello(self): # public method
        print(self._hello())

class Man(Person):
##    def __init__(self, name):
##        self.name=name+" sir"
    
    def _hello(self):
        # self.__get_trailing_text() 사용 불가
        return "Hello Mr.{}".format(self.name)

p = Person("mark")
p.hello() # Hello mark, Nice to meet you !!!

try:
    p.__get_trailing_text()
except Exception as e:
    print(e) # AttributeError

m = Man("silva")
m.hello() # Hello Mr.silva

# 가능은 하지만 좋지 않은 용법
print(m._hello()) # Hello Mr.silva

try:
    print(m.__get_trailing_text())
except Exception as e:
    print(e) # AttributeError
    

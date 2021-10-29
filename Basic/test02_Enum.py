from enum import Enum
    
Menu = Enum('Me', ['추가', '삭제', '검색', '덤프', '종료'])

print(Menu)              # <enum 'Me'>
print(Menu.종료)          # Me.종료
print(Menu.종료.name)     # 종료
print(Menu.종료.value)    # 5
print(Menu['종료'])       # Me.종료
print(type(Menu.추가))    # <enum 'Me'>
a = list(Menu)
print(a)                 # [<Me.추가: 1>, <Me.삭제: 2>, <Me.검색: 3>, <Me.덤프: 4>, <Me.종료: 5>]

## class Menu(Enum):
##    추가 = 1
##    삭제 = 2
##    검색 = 3
##    덤프 = 4
##    종료 = 5

s = [f'({m.value}){m.name}' for m in Menu]

print(s)                        # ['(1)추가', '(2)삭제', '(3)검색', '(4)덤프', '(5)종료']
print(*s, sep='   ', end='')    # (1)추가   (2)삭제   (3)검색   (4)덤프   (5)종료

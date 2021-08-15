from enum import Enum
    
Menu=Enum('Me', ['추가', '삭제', '검색', '덤프', '종료'])
print(Menu)
print(Menu.종료)
print(Menu.종료.name)
print(Menu.종료.value)
print(Menu['종료'])
print(type(Menu.추가))
aa=list(Menu)
print(aa)
##class Menu(Enum):
##    추가 = 1
##    삭제 = 2
##    검색 = 3
##    덤프 = 4
##    종료 = 5

s=[f'({m.value}){m.name}' for m in Menu]
# print(*s, sep='   ', end='')

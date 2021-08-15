from enum import Enum
from chained_hash import ChainedHash, Node
from os import system

system("sys")

Menu=Enum('Menu', ['추가', '삭제', '검색', '덤프', '종료'])

##class Menu(Enum):
##    추가 = 1
##    삭제 = 2
##    검색 = 3
##    덤프 = 4
##    종료 = 5

def select_menu() -> Menu:
    s=[f'({m.value}){m.name}' for m in Menu]
    while True:
        print(*s, sep='   ', end='')
        n=int(input(': '))
        if 1<= n <= len(Menu):
            return Menu(n)

hash=ChainedHash(13)

addNode=Node(40, 50, None) ; hash.table[1]=addNode
a=[1,14,27,40]
for key in a:
    if not hash.addFirst(key, 20):
        print('추가를 실패했습니다.')

addNode=Node(41, 50, None) ; hash.table[2]=addNode
b=[a[i]+1 for i in range(len(a))]
for key in b:
    if not hash.addLast(key, 30):
        print('추가를 실패했습니다.')

hash.dump()

while True:
    menu=select_menu()

    if menu==Menu.추가:
        key=int(input('추가할 키를 입력하세요.: '))
        val=input('추가할 값을 입력하세요.: ')

        if not hash.addFirst(key, val):
            print('추가를 실패했습니다.')

        if not hash.addLast(key+1, val):
            print('추가를 실패했습니다.')
            
    elif menu==Menu.삭제:
        key=int(input('삭제할 키를 입력하세요.: '))
        if not hash.remove(key):
            print('삭제를 실패했습니다!')
            
    elif menu==Menu.검색:
        key=int(input('검색할 키를 입력하세요.: '))
        t=hash.search(key)
        if t is not None:
            print(f'검색한 키를 갖는 값은 {t}입니다.')
        else:
            print('검색할 데이터가 없습니다.')
            
    elif menu==Menu.덤프:
        hash.dump()
        
    else:
        break
        
        


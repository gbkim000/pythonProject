from enum import Enum
from linked_list import LinkedList

Menu = Enum('Menu', ['머리삽입', '꼬리삽입', '머리삭제', '꼬리삭제',
                     '주목출력', '주목이동', '주목삭제', '모두삭제',
                     '노드검색', '멤버십판단', '모두출력', '스캔하기', '종료하기'])


def select_Menu() -> Menu:
    s = [f'({m.value}){m.name}' for m in Menu]
    while True:
        print(*s, sep=' ', end='')
        n = int(input(': '))
        if 1 <= n <= len(Menu):
            return Menu(n)


lst = LinkedList()

while True:
    menu = select_Menu()

    if menu == Menu.머리삽입:
        lst.add_first(int(input("머리노드에 삽입할 값 : ")))
    elif menu == Menu.꼬리삽입:
        lst.add_last(int(input("꼬리노드에 삽입할 값 : ")))
    elif menu == Menu.머리삭제:
        lst.remove_first()
    elif menu == Menu.꼬리삭제:
        lst.remove_last()
    elif menu == Menu.주목출력:
        lst.print_current_node()
    elif menu == Menu.주목이동:
        lst.next()
    elif menu == Menu.주목삭제:
        lst.remove_current_node()
    elif menu == Menu.모두삭제:
        lst.clear()
    elif menu == Menu.노드검색:
        pos = lst.search(int(input('검색할 값 : ')))
        if pos >= 0:
            print(f'검색값은 {pos + 1}번째에 있습니다.')
        else:
            print('해당 데이터가 존재하지 않습니다.')
    elif menu == Menu.멤버십판단:
        temp = int(input('멤버십인지 판단할 값 : '))
        print('멤버십에 포함되어 있습니다.') if temp in lst else print('멤버십이 아닙니다.')
    elif menu == Menu.모두출력:
        lst.print()
    elif menu == Menu.스캔하기:
        for e in lst:
            print(e)
    else:
        break

import random
from MineSweeper.settings import *


class GameLogic():
    def __init__(self):  # 게임 초기화 지점
        pass

    def run(self):  # 실행 부분
        level = self.getLevel()
        map = self.createMap(level)

    def getLevel(self):  # 난이도 가져오기
        while True:
            level = input("난이도를 입력하세요 (초급, 중급, 고급): ")
            if level == '초보':
                return BEGINNER
            elif level == '중급':
                return INTERMEDIATE
            elif level == '고급':
                return ADVANCED
            else:
                print("난이도를 제대로 입력해주세요.")

    def createMap(self, level):  # 레벨에 따른 맵 생성 + 레벨에 따른 지뢰 심기 + 지뢰 근처에 적절한 숫자 생성 한번에 처리함.
        width = level[0]
        height = level[1]
        mine = level[2]
        arr = [[0 for row in range(width)] for column in range(height)]
        num = 0
        while num < mine:
            x = random.randint(0, width - 1)  # 지뢰의 x축 범위 랜덤으로 설정
            y = random.randint(0, height - 1)  # 지뢰의 y축 범위 랜덤으로 설정
            print(num)
            if arr[y][x] == 'X':
                print(num)
                continue
            print("[HINT]생성된 지뢰 위치 : (x:", x, ", y:", y, ")")  # 테스트를 용이하게 하기 위해 넣음 (GUI에서는 출력되지 않아야함.)
            arr[y][x] = 'X'  # 생성된 지뢰 좌표에 X로 표현

            # 지뢰 주변 힌트 숫자 생성
            if (x >= 0 and x <= width - 2) and (y >= 0 and y <= height - 1):
                if arr[y][x + 1] != 'X':
                    arr[y][x + 1] += 1  # center right
            if (x >= 1 and x <= width - 1) and (y >= 0 and y <= height - 1):
                if arr[y][x - 1] != 'X':
                    arr[y][x - 1] += 1  # center left
            if (x >= 1 and x <= width - 1) and (y >= 1 and y <= height - 1):
                if arr[y - 1][x - 1] != 'X':
                    arr[y - 1][x - 1] += 1  # top left
            if (x >= 0 and x <= width - 2) and (y >= 1 and y <= height - 1):
                if arr[y - 1][x + 1] != 'X':
                    arr[y - 1][x + 1] += 1  # top right
            if (x >= 0 and x <= width - 1) and (y >= 1 and y <= height - 1):
                if arr[y - 1][x] != 'X':
                    arr[y - 1][x] += 1  # top center
            if (x >= 0 and x <= width - 2) and (y >= 0 and y <= height - 2):
                if arr[y + 1][x + 1] != 'X':
                    arr[y + 1][x + 1] += 1  # bottom right
            if (x >= 1 and x <= width - 1) and (y >= 0 and y <= height - 2):
                if arr[y + 1][x - 1] != 'X':
                    arr[y + 1][x - 1] += 1  # bottom left
            if (x >= 0 and x <= width - 1) and (y >= 0 and y <= height - 2):
                if arr[y + 1][x] != 'X':
                    arr[y + 1][x] += 1  # bottom center
            num += 1
        return arr

    def displayMap(self, map):  # 콘솔 출력용 (GUI랑은 상관 없음)
        for row in map:
            print(" ".join(str(cell) for cell in row))
            print("")

    def checkMine(self, map, x, y):  # 지뢰 찾는 함수. 이기면 True, 지면 False 라는 의미로 설정함.
        if map[y][x] == 'X':
            return False
        return True

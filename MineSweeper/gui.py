import pygame
import sys

import MineSweeper.gameLogic
from MineSweeper.gameLogic import GameLogic
from MineSweeper.settings import *
from pygame.locals import *


# 내 생각에는 일단 " "(스페이스 한칸)로 채워져 있는 판을 만들고, 해당 칸을 클릭했을 때, map에 있는 해당 칸으로 바꿔주는게 어떨까 싶음.

class GUI():  # 임시. pygame 안써도 됨.
    def __init__(self, level):  # 초기화
        pygame.init()  # pygame 초기화. 초기화를 해야 pygame을 사용할 수 있다고 함.
        super().__init__()
        SCREEN_SIZE = self.getScreenSize(level)
        SCREEN_WIDTH = self.getScreenSize(level)[0]
        SCREEN_HEIGHT = self.getScreenSize(level)[1]
        self.count = 0
        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # 디스플레이 크기 설정
        pygame.display.set_caption('Minesweeper')  # 프로그램 이름 설정
        gameLevel = self.getLevel(level)  # 레벨을 tuple 형태로 받아옴.
        arr = GameLogic.createMap(self, gameLevel)  # 맵을 생성하고 저장
        OPENED = [[False for column in range(len(arr[0]))] for row in range(len(arr))]  # 오픈한 칸인지 확인
        CHECKED = [[False for column in range(len(arr[0]))] for row in range(len(arr))]  # 깃발을 체크한 칸인지 확인
        self.draw_Cells(arr)  # 칸 그리기

        while True:  # main game loop (게임에 필요한 메소드 불러오기)
            for event in pygame.event.get():  # 창 안의 이벤트를 받는 영역. 예를 들면 종료키, 키보드키, 마우스 클릭 등
                if event.type == QUIT:  # 상단의 X키 누를 때 까지 프로그램 종료 안하고 유지하기 (필수임)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 마우스 왼쪽 클릭시
                        column_index = event.pos[0] // CELL_SIZE
                        row_index = event.pos[1] // CELL_SIZE
                        num = 0
                        print(column_index, row_index)
                        if arr[row_index][column_index] == 'X':  # 선택된 칸이 X이면 종료
                            self.open_All(arr, OPENED)  # 모든 칸 열기
                            print("패배")
                            fail_font = pygame.font.SysFont('Sans', 70)
                            fail_image = fail_font.render('Lose', True, RED)
                            self.screen.blit(fail_image,
                                             fail_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
                        else:  # 선택된 칸 오픈
                            OPENED = self.open_Cell(arr, OPENED, column_index, row_index)
                        for i in range(len(arr)):  # 열리지 않은 칸 수 셈
                            for j in range(len(arr[0])):
                                if not OPENED[i][j]:
                                    num += 1
                        if num == gameLevel[2]:  # 열리지 않은 칸의 수와 지뢰의 수가 같으면 성공 출력 == 지뢰가 없는 칸 모두 오픈
                            success_font = pygame.font.SysFont('Sans', 70)
                            success_image = success_font.render('Win', True, RED)
                            self.screen.blit(success_image,
                                             success_image.get_rect(centerx=SCREEN_WIDTH // 2,
                                                                    centery=SCREEN_HEIGHT // 2))
                    elif event.button == 3:  # 마우스 우클릭시 깃발
                        column_index = event.pos[0] // CELL_SIZE
                        row_index = event.pos[1] // CELL_SIZE
                        flag_font = pygame.font.SysFont('Sans', 30)
                        flag_image = flag_font.render('V', True, WHITE)
                        if CHECKED[row_index][column_index]:  # 이미 깃발이 체크된 칸을 선택시 체크 지우기
                            flag_image.fill(GRAY)
                            CHECKED[row_index][column_index] = False
                        else:
                            CHECKED[row_index][column_index] = True
                        self.screen.blit(flag_image, (column_index * CELL_SIZE + 10, row_index * CELL_SIZE + 5))
                        '''while num>4: # 승리표시가 되는지 확실히 모르겠음
                            if GameLogic().createMap(self) == arr[row_index][column_index]:
                                num+=1
                                continue
                            success_font = pygame.font.SysFont('malgungothic', 70)
                            success_image = success_font.render('승리', True, RED)
                            self.screen.blit(success_image,success_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))'''
            #               self.draw_Cells(arr)  # 칸 그리기
            pygame.display.update()

    def getLevel(self, level):  # 레벨 가져오기(나중에 수정 필요)
        if level == '초급':
            return BEGINNER
        elif level == '중급':
            return INTERMEDIATE
        elif level == '고급':
            return ADVANCED

    def getScreenSize(self, level):
        if level == '초급':
            return SCREEN_SIZE_BEGINNER
        elif level == '중급':
            return SCREEN_SIZE_INTERMEDIATE
        elif level == '고급':
            return SCREEN_SIZE_ADVANCED

    def draw_Cells(self, arr):
        COLUMN_COUNT = len(arr[0])
        ROW_COUNT = len(arr)

        for column_index in range(COLUMN_COUNT):
            for row_index in range(ROW_COUNT):
                rect = (CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def open_Cell(self, arr, OPENED, col, row):
        if col < 0 or col >= len(arr[0]) or row < 0 or row >= len(arr):
            return arr
        cell = arr[row][col]  # 선택된 칸
        if OPENED[row][col]:  # 이미 확인한 칸
            return arr
        OPENED[row][col] = True
        if cell == 0:  # 셀이 0이면 1 이상의 수가 나올때까지 반복해서 여는 재귀함수 생성 / for 문으로 고쳐야할 듯
            self.open_Cell(arr, OPENED, col + 1, row)
            self.open_Cell(arr, OPENED, col, row + 1)
            self.open_Cell(arr, OPENED, col + 1, row + 1)
            self.open_Cell(arr, OPENED, col - 1, row)
            self.open_Cell(arr, OPENED, col, row - 1)
            self.open_Cell(arr, OPENED, col - 1, row - 1)
            self.open_Cell(arr, OPENED, col + 1, row - 1)
            self.open_Cell(arr, OPENED, col - 1, row + 1)
        # font5 = pygame.font.SysFont('notarisation', 50)
        font5 = pygame.font.SysFont('Sans', 30)
        img5 = font5.render(str(cell), True, BLACK)
        self.screen.blit(img5, (CELL_SIZE * col + 10, CELL_SIZE * row + 10))
        return OPENED

    def open_All(self, arr, OPENED):
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                self.open_Cell(arr, OPENED, j, i)

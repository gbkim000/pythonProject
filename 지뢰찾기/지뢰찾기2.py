import random
import sys

inputMN = input('M N :')
landminesMN = inputMN.split(' ')

M = int(landminesMN[0])
N = int(landminesMN[1])

if N <= 0 or M > 100:
    sys.exit()

K = random.randrange(0, M * N)  # spidermine count
landminesMap = [['.'] * M for i in range(N)]
showminesMap = [['*'] * M for i in range(N)]


def createLandMine(M, N, K):
    landmineMark = M * N - K
    ttL = [i for i in range(landmineMark)]
    for i in range(K):
        ttL.append(landmineMark)
    random.shuffle(ttL)  # random spread mine

    cnt = 0
    for i in range(N):
        for j in range(M):
            mark = '*' if ttL[cnt] == landmineMark else '.'
            print(mark, end=' ')
            landminesMap[i][j] = mark
            cnt += 1
        print()


def showMap(M, N):
    for i in range(N):
        for j in range(M):
            if landminesMap[i][j] == '.':
                mineCnt = 0
                for a in range(i - 1, i + 2):
                    for b in range(j - 1, j + 2):
                        if a == i and b == j:
                            pass
                        elif a >= 0 and a < N and b >= 0 and b < M and landminesMap[a][b] == '*':
                            mineCnt += 1
                showminesMap[i][j] = str(mineCnt)
            print(showminesMap[i][j], end=' ')
        print()


createLandMine(M, N, K)
print("\n\nanswewr :")
showMap(M, N)

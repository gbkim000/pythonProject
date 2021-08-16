import numpy as np
size = list(map(int, input('격자의 크기를 입력하세요. m*n -> m n : ').split()))
datas = []
if len(size) != 2:기
    print('사이즈를 잘못 입력하셨습니다.')
    raise ValueError
else:
    m, n = size[0], size[1]
    count = 1
    while count <= m:
        data = list(input("%d번째 줄을 입력하세요. 지뢰는 '*', 지뢰가 아니면 '.'(dot) : " % count))
        if len(data) != n:
            print('잘못 입력하셨습니다.')
            raise ValueError
        elif set(data) - {'.', '*'}:
            print('잘못 입력하셨습니다.')
            raise ValueError
        else:
            datas.append(['.'] + data + ['.'])
            count += 1
    data = [['.' for x in range(n+2)]] + datas + [['.' for x in range(n+2)]]
mine = np.array(data)
for k in range(1, m+1):
    for j in range(1, n+1):
        if mine[k, j] == '*':
            pass
        else:
            mine[k, j] = [mine[k-1, j-1], mine[k-1, j], mine[k-1, j+1],
                          mine[k, j-1],                 mine[k, j+1],
                          mine[k+1, j-1], mine[k+1, j], mine[k+1, j+1]].count('*')
print(mine[1:m+1, 1:n+1])
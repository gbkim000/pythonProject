col, row = map(int, input().split())
matrix = []
for i in range(row):
    matrix.append(list(input()))
for x in range(row):
    for y in range(col):
        if matrix[x][y] == '*':
            print(matrix[x][y], sep='', end='')
        else:
            count = 0
            for xo in range(-1, 2):
                for yo in range(-1, 2):
                    if 0 <= x + xo < row and 0 <= y + yo < col and matrix[x + xo][y + yo] == '*':
                        count += 1
            print(count, sep='', end='')
    print()

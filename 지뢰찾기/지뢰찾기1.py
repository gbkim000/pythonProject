import random
m = int(input("M:"))
n = int(input("N:"))
if not(n > 0 and m <= 100):
    raise Exception("N > 0, M <= 100")
mn = [[random.choice(['.','.','.','.','*']) for x in range(n)] for y in range(m)]
for y in mn:
    print(''.join(y))
r = mn.copy()
for y, yd in enumerate(r):
    for x, xd in enumerate(yd):
        if r[y][x] == '*': continue
        count = 0
        c = [[''] if y - 1 < 0 else r[y-1][0 if x - 1 < 0 else x - 1:x+2],
             r[y][0 if x - 1 < 0 else x - 1:x+2],
             [''] if y + 1 >= m else r[y+1][0 if x - 1 < 0 else x - 1:x+2]]
        for z in c:
            count+=z.count('*')
        r[y][x] = str(count)

print("output")
for y in r:
    print(''.join(y))
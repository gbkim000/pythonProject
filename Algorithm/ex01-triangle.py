a = 'Happy'
b = len(a)

def display(num):
    for k in range(num):
        print(' ', end='')

for i in range(1, b+1):
    display(b - i)
    for j in range(i):
        #print("*", end='')
        print(a[j], end='')
    print()

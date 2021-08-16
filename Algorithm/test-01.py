a = 'Happy'
b = len(a) + 1

name = input('name:')
print(name)


def display(num):
    for k in range(num):
        print(' ', end='')


for i in range(b):
    display(b - i + 1)
    for j in range(i):
        print(a[j], end='')
    print('')

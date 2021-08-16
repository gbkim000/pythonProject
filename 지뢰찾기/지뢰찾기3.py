import os
import sys

def main():
    if len(sys.argv) == 1:
        print("set input file")

    else:
        f = open(sys.argv[1],'r')
        line = f.readline()
        a=int(line.split()[0])
        b=int(line.split()[1])
        mineLoc = f.read()
        #print(mineLoc)
        for i in range (0, a):
            for j in range (0, b):기
                if mineLoc[i*(b+1)+j] == ".":
                    num = 0
                    if decFun(i-1,j-1,a,b):
                        if mineLoc[(i-1)*(b+1)+j-1] == "*":
                            num=num+1
                    if decFun(i-1,j,a,b):
                        if mineLoc[(i-1)*(b+1)+j] == "*":
                            num=num+1
                    if decFun(i-1,j+1,a,b):
                        if mineLoc[(i-1)*(b+1)+j+1] == "*":
                            num = num + 1
                    if decFun(i,j-1,a,b):
                        if mineLoc[i*(b+1)+j-1] == "*":
                            num = num + 1
                    if decFun(i,j+1,a,b):
                        if mineLoc[i*(b+1)+j+1] == "*":
                            num = num + 1
                    if decFun(i+1,j-1,a,b):
                        if mineLoc[(i+1)*(b+1)+j-1] == "*":
                            num = num + 1
                    if decFun(i+1,j,a,b):
                        if mineLoc[(i+1)*(b+1)+j] == "*":
                            num = num + 1
                    if decFun(i+1,j+1,a,b):
                        if mineLoc[(i+1)*(b+1)+j+1] == "*":
                            num = num + 1
                    print(num),
                else:
                    print(mineLoc[i*(b+1)+j]),
            print()
    return None

def decFun(x,y,a,b):
    if x < 0:
        return 0
    if x >= a:
        return 0
    if y < 0:
        return 0
    if y >= b:
        return 0
    return 1


if __name__ == '__main__':
    main()
    sys.exit(0)
data = enumerate((1, 2, 3))         # tuple 형의 자료
print(data, type(data))
for i, value in data:
    print(i, ":", value)
print()

data = enumerate({1, 2, 3})         # Set 형의 자료
for i, value in data:
    print(i, ":", value)
print()

data = enumerate([1, 2, 3])         # list 형의 자료
for i, value in data:
    print(i, ":", value)
print()

dict1 = {'이름': '한사람', '나이': 33} # dictionary 형의 자료
data = enumerate(dict1)
for i, key in data:
    print(i, ":", key, dict1[key])
print()

data = enumerate("재미있는 파이썬")    # 문자열 자료
for i, value in data:
    print(i, ":", value)
print()



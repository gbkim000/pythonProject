# # %% test
# print('홍길동')
# print('저팔계')
#
# # %% test
# print('홍길동2')
# print('저팔계2')


data1 = 10
data2 = "%d" % 100  # data2는 문자열 타입임.
print(data1, data2)
print(type(data2))

# %% format test2
# "문자열값".format()
data1 = 10
data2 = 10.4231
data3 = 'A'
data4 = "ABC"
print("data : {}".format(data1))
print("data1 : {}\ndata2 : {}".format(data1, data2))
print("data3 : %s" % data3)
print("data3 : %c" % data3)
print("data : %c" % 65)
print("data4 : %s" % data4)
print("data4 : {}".format(data4))

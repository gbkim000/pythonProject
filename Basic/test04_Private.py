# class cTest():
#     __test__ = "public"
#
#     def __init__(self):
#         print("Creat cTest")
#
# if __name__ == '__main__':
#     t1 = cTest()
#     print(t1.__test__)

class Spam:
    __attr = 100            # private 변수(왼쪽에만 '__'를 붙임)

    def __init__(self):     # public 함수
        self.__attr = 999

    def method(self):       # public 함수
        self.__method()

    def __method(self):     # private 함수
        print('self.__attr', self.__attr)
        print('Spam.__attr', Spam.__attr)

spam = Spam()
spam.method()

# spam.__method()	    # private 메소드이므로 접근 불가
# Spam.__attr           # private 변수이므로 접근 불가.


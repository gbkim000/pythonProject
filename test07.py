class Car:
    def __init__(self, id):
        self.id = id  # 차량 번호

    def __len__(self):
        return len(self.id)

    def __str__(self):
        return '차량 번호 : ' + self.id

    def __call__(self):
        print('__call__ 함수')

    def __iter__(self):
        return iter(self.id)  # iter 함수로 변수 id의 iterator 객체를 반환


def main():
    cc = Car('12가3456')
    cc()  # __call__ 메서드 호출
    print(len(cc))  # __len__ 메서드 호출
    print(str(cc))  # __str__ 메서드 호출
    print(cc)  # __str__ 메서드 호출  / print(str(cc))와 동일

    for i in cc:  # Car 객체가 iterable 객체이므로 가능.(특수 메서드 __iter__(self))
        print(i, end=' ')

main()

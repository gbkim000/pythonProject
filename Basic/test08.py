class Coll:
    def __init__(self, values):
        self.values = values  # 인자로 전달된 값 저장
        self.call_count = 0  # __next__ 메서드 호출 횟수
        
    def __next__(self):
        if len(self.values) <= self.call_count:
            raise StopIteration
            
        self.call_count += 1
        return self.values[self.call_count - 1]
    
    def __iter__(self):  
        self.call_count = 0    # iter 함수 호출 시 next 호출 횟수 초기화하고,
        return self             # 객체 자체를 반환 --> 몇 번이고 호출 가능토록 함
    
def main():
    co = Coll([1, 2, 3, 4, 5])  # 리스트, 튜플, 문자열 등 iterable 객체 전달
    while True:
        try:
            i = next(co)
            print(i, end=' ')  # 1 2 3 4 5
        except StopIteration:
            break

    print('')
    for i in co:
        print(i,end='  ')

    print('')
    for i in co:
        print(i, end=', ')
    print("\n------------------")
main()


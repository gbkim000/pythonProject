# 문자열 검색하는 보이어 무어 알고리즘
def boyer_moore(pattern, text):
    # 길이를 자주쓰므로 길이를 받아둔다.
    M = len(pattern)
    N = len(text)
    i = 0
    # 반복은 최대 긴텍스트 길이 - 작은텍스트 길이
    while i <= N - M:
        # 보이어 무어 알고리즘은 뒤에서부터 접근하므로 pattern길이의 -1을 해준다.
        # -1을 해주는 이유는 인덱스가 0부터 시작하기 때문이다.
        j = M - 1
        # 뒤에서부터 검사하고 인덱스를 감소하는 형식이므로 0보다 이상일때만 동작한다.
        while j >= 0:
            # 끝글자부터 비교하면서 같다면 하나씩 감소하면서 비교한다.
            if pattern[j] != text[i + j]:
                # 글자가 틀리다면 제일마지막 글자 기준으로 find 함수를 호출한다.
                move = find(pattern, text[i + M - 1])
                break
        j = j - 1
    # 인덱스가 -1이라는 뜻은 모든 글자가 맞았다는 이야기이다.
    if j == -1:
        # 찾았으므로 true를 리턴한다.
        # return True
        # 인덱스 위치를 찾는다면
        return i
    else:
        # -1이 아니라면 글자를 못찾은 것이므로 find에서 넘겨준 값만큼 옆으로 이동한다.
        i += move

    # 여기까지 왔다면 끝까지 찾지 못한것이므로 False를 리턴한다.
    # return False
    # 인데스 위치로 한다면
    return -1


# 불필요한 비교를 건너뛰기 위한 함수
def find(pattern, char):
    # 마지막 부분과 일치하는 부분이 있는지 검색한다.
    # 마지막 부분은 이미 가능성이 없으므로 그전부터 검사한다.
    for i in range(len(pattern) - 2, -1, -1):
        # 마지막글자와 패턴중 일치하는 숫자가 있다면 그만큼 이동한다.
        if pattern[i] == char:
            return len(pattern) - i - 1
    # 일치하는 글자가 없다면 패턴의 길이만큼 이동한다.
    return len(pattern)


print(boyer_moore('ABC', 'ABABCDEFGHA'))
print(boyer_moore("ATION", "VISOINQUESTIONONIONCAPTIONGRADUATION"))

def initSkip(p):
    NUM = 27  # 알파벳 수
    plen = len(p)  # 패턴의 길이
    skip = [plen for i in range(NUM)]  # skip 함수를 모두 M값으로 초기화
    for i in range(plen):
        skip[ord(p[i]) - ord('A')] = plen - i - 1
    return skip  # skip 배열 반환

    # print(initSkip("ATION"))  # 임시로 ATION 이란 패턴을 입력


def BM(p, txt):
    plen = len(p)
    tlen = len(txt)
    skip = initSkip(p)


    i = plen - 1
    j = plen - 1

    while j >= 0:
        while txt[i] != p[j]:
            k = skip[ord(txt[i]) - ord('A')]
            if plen - j > k:
                i = i + plen - j
            else:
                i = i + k
            if i >= tlen:
                return tlen  # 검색 실패한 경우.
            j = plen - 1
        i = i - 1
        j = j - 1
    return i + 1

print(BM('ABC', 'ABABCDEFGHA'))
print(BM("ATION", "VISOINQUESTIONONIONCAPTIONGRADUATION"))

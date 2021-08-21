def kmp_match(txt: str, pat: str) -> int:
    index = 1
    cnt = 0
    skip = [0] * (len(pat) + 1)

    skip[index] = 0
    skip[0] = -1
    # ----- 교재에 있는 코드 -----
    while index != len(pat):
        if pat[index] == pat[cnt]:
            index += 1
            cnt += 1
            skip[index] = cnt
        elif cnt == 0:
            index += 1
            skip[index] = 0  # cnt
        else:
            cnt = skip[cnt]

    # ----- 내가 수정한 코드 -----
    # while index != len(pat):
    #     if pat[index] == pat[cnt]:
    #         cnt += 1
    #         index += 1
    #         skip[index] = cnt
    #     else:
    #         if cnt == 0:
    #             index += 1
    #             skip[index] = 0  # = cnt
    #         else:
    #             cnt = skip[cnt]

    index = cnt = 0

    # ----- 내가 수정한 코드 -----
    dist = 0
    flag = -1

    while True:
        index = 0
        if (index + dist) + len(pat) > len(txt):
            break

        while txt[index + dist] == pat[cnt]:
            cnt += 1
            index += 1

            if cnt == len(pat):
                print(f'{dist + 1}번째에서 찾기 완료!')
                flag += 1
                break

        dist = dist + (cnt - skip[cnt])
        cnt = 0
    return flag

    # ----- 교재에 있는 코드 -----
    # while index != len(txt) and cnt != len(pat):
    #     if txt[index] == pat[cnt]:
    #         index += 1
    #         cnt += 1
    #     elif cnt == 0:
    #         index += 1
    #     else:
    #         cnt = skip[cnt]
    #
    # return index - cnt if cnt == len(pat) else -1


if __name__ == '__main__':

    # s1 = input('텍스트 입력: ')
    # s2 = input('패턴 입력: ')

    s1 = 'ABAABACABAACCABACABACABAACABACABAAC'
    s2 = "ABACABAAC"

    idx = kmp_match(s1, s2)

    if idx == -1:
        print('텍스트 안에 패턴이 존재하지 않습니다.')
    else:
        # print(f'({idx + 1})번째 문자가 일치합니다.')
        print(f'총({idx + 1})번의 문자열이 일치합니다.')

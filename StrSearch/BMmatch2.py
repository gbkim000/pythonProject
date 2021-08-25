def BM(pat: str, txt: str) -> int:
    skip = [None] * 256

    for pt in range(256):
        skip[pt] = len(pat)

    for pt in range(len(pat)):
        skip[ord(pat[pt])] = len(pat) - pt - 1

    while pt < len(txt):
        pp = len(pat) - 1
        while txt[pt] == pat[pp]:
            if pp == 0:
                return pt
            pt -= 1
            pp -= 1
        # pt += skip[ord(txt[pt])] if skip[ord(txt[pt])] > len(pat) - pp \
        #    else len(pat) - pp
        if skip[ord(txt[pt])] > len(pat) - pp:
            pt += skip[ord(txt[pt])]
        else:
            pt += len(pat) - pp

    return -1


print(BM('ABC', 'ABABCDEFGHA'))
print(BM("ATION", "VISOINQUESTIONONIONCAPTIONGRADUATION"))
print(BM('ABCXYABCXY', 'saaABCXYABCXY'))

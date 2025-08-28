import sys
import re


def check_1(s):
    """
    정규식 사용한 풀이
    """
    regex = re.compile("(100+1+|01)+")
    return regex.fullmatch(s)


def check_2(s):
    """
    정규식 사용하지 않은 풀이
    """
    index = 0

    while index < len(s):
        # 01 패턴
        if index + 2 <= len(s) and s[index : index + 2] == "01":
            index += 2
            continue

        # 100+1+ 패턴
        if index < len(s) and s[index : index + 3] == "100":
            index += 3
            # 0+ 처리
            while index < len(s) and s[index] == "0":
                index += 1

            # 최소한의 1
            if index >= len(s) or s[index] != "1":
                return False

            # 1+ 처리
            one_start = index
            while index < len(s) and s[index] == "1":
                index += 1

            # 끝까지 1로 가는 경우
            if index == len(s):
                return True

            # 끝까지 1로 가지 않는 경우, 1을 하나 덜먹고 남은 부분 검사 
            for split in range(one_start + 1, index + 1):
                if check_2(s[split:]):
                    return True
            return False
        return False
    return True


T = int(sys.stdin.readline())

for _ in range(T):
    s = sys.stdin.readline().strip()
    if check_2(s):
        print("YES")
    else:
        print("NO")

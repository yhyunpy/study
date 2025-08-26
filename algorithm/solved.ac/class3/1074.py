import sys

N, r, c = map(int, sys.stdin.readline().split())


def dfs(n, r, c, val):
    if n == 1:
        if (r, c) == (0, 0):
            print(val)
        elif (r, c) == (0, 1):
            print(val + 1)
        elif (r, c) == (1, 0):
            print(val + 2)
        else:
            print(val + 3)
        return
    else:
        n -= 1
        # 1사분면
        if r < 2**n and c < 2**n:
            dfs(n, r, c, val)
        # 2사분면
        elif r < 2**n and c >= 2**n:
            c -= 2**n
            val += 4**n * 1
            dfs(n, r, c, val)
        # 3사분면
        elif r >= 2**n and c < 2**n:
            r -= 2**n
            val += 4**n * 2
            dfs(n, r, c, val)
        # 4사분면
        else:
            r -= 2**n
            c -= 2**n
            val += 4**n * 3
            dfs(n, r, c, val)


dfs(N, r, c, 0)

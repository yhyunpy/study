import sys
from collections import deque


def D(n):
    return n * 2 % 10000


def S(n):
    return n - 1 if n != 0 else 9999


def L(n):
    return (n // 1000) + (n % 1000) * 10


def R(n):
    return (n % 10) * 1000 + n // 10


# 주의 : 문자열 +는 매번 새로운 문자열을 만들어서 느리다 
def solution(n, m):
    q = deque()
    path = [(-1, "") for _ in range(10000)]
    q.append((n))
    path[n] = (n, "")
    while q:
        now_n = q.popleft()
        if now_n == m:
            ans = []
            prev = m
            while prev != n:
                ans.append(path[prev][1])
                prev = path[prev][0]
            return "".join(reversed(ans))
        next_n = D(now_n)
        if path[next_n][0] == -1:
            path[next_n] = (now_n, "D")
            q.append(next_n)
        next_n = S(now_n)
        if path[next_n][0] == -1:
            path[next_n] = (now_n, "S")
            q.append(next_n)
        next_n = L(now_n)
        if path[next_n][0] == -1:
            path[next_n] = (now_n, "L")
            q.append(next_n)
        next_n = R(now_n)
        if path[next_n][0] == -1:
            path[next_n] = (now_n, "R")
            q.append(next_n)


T = int(sys.stdin.readline())

ans = []
for _ in range(T):
    n, m = map(int, sys.stdin.readline().split())
    ans.append(solution(n, m))

sys.stdout.write("\n".join(ans))

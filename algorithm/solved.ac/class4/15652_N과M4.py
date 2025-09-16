import sys

N, M = map(int, sys.stdin.readline().split())
nums = []


def dfs(start):
    if len(nums) == M:
        print(" ".join(map(str, nums)))

    for i in range(start, N + 1):
        if nums.count(i) < M:
            nums.append(i)
            dfs(i)
            nums.pop()


dfs(1)

import sys

N, M = map(int, sys.stdin.readline().split())
nums = []


def dfs(now):
    if len(nums) == M:
        print(" ".join(map(str, nums)))
        return

    for i in range(now, N + 1):
        if i not in nums:
            nums.append(i)
            dfs(i + 1)
            nums.pop()


dfs(1)

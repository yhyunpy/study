import sys

N, M = map(int, sys.stdin.readline().split())
nums = list(map(int, sys.stdin.readline().split()))
sorted_nums = sorted(nums)

ans = []


def dfs(idx):
    if len(ans) == M:
        print(" ".join(map(str, ans)))

    for i in range(N):
        if sorted_nums[i] not in ans:
            ans.append(sorted_nums[i])
            dfs(i + 1)
            ans.pop()


dfs(0)

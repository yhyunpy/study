import sys

N, M = map(int, sys.stdin.readline().split())
nums = list(map(int, sys.stdin.readline().split()))
sorted_nums = sorted(nums)

ans = []
ans_list = []


def dfs(idx):
    if len(ans) == M:
        if tuple(ans) not in ans_list:
            ans_list.append(tuple(ans))
            print(" ".join(map(str, ans)))
        return

    for i in range(idx, N):
        ans.append(sorted_nums[i])
        dfs(i)
        ans.pop()


dfs(0)

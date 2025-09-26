import sys

N, M = map(int, sys.stdin.readline().split())
nums = list(map(int, sys.stdin.readline().split()))
sorted_nums = sorted(nums)


ans = []
visited = [False for _ in range(N)]


def dfs():
    if len(ans) == M:
        print(" ".join(map(str, ans)))
        return

    prev = None
    for i in range(N):
        if not visited[i] and sorted_nums[i] != prev:
            ans.append(sorted_nums[i])
            visited[i] = True
            dfs()
            ans.pop()
            visited[i] = False
            prev = sorted_nums[i]


dfs()

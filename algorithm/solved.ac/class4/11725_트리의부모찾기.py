import sys

sys.setrecursionlimit(10**6)


def solution(graph):
    visited = [False for _ in range(N + 1)]
    route = []

    def dfs(start: int, before: int | None = None):
        route.append([start, before])
        for next in graph[start]:
            if not visited[next]:
                visited[next] = True
                dfs(next, start)

    visited[1] = True
    dfs(1)
    route.sort(key=lambda x: x[0])
    route.pop(0)
    for x in route:
        print(x[1])


N = int(sys.stdin.readline())

graph = {}

for _ in range(N - 1):
    a, b = map(int, sys.stdin.readline().split())
    if a in graph:
        graph[a].append(b)
    else:
        graph[a] = [b]
    if b in graph:
        graph[b].append(a)
    else:
        graph[b] = [a]


solution(graph)

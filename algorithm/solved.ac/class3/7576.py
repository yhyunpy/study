import sys
from collections import deque

M, N = map(int, sys.stdin.readline().split())

graph = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

move = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def main():
    queue = deque()
    for i in range(N):
        for j in range(M):
            if graph[i][j] == 1:
                queue.append((i, j))

    def bfs():
        while queue:
            now_x, now_y = queue.popleft()
            for dx, dy in move:
                x = now_x + dx
                y = now_y + dy
                if 0 <= x < N and 0 <= y < M:
                    if graph[x][y] == 0:
                        graph[x][y] = graph[now_x][now_y] + 1
                        queue.append((x, y))

    bfs()

    res = 0
    for i in range(N):
        for j in range(M):
            if graph[i][j] == 0:
                return -1
            res = max(res, graph[i][j])
    return res - 1


if __name__ == "__main__":
    print(main())

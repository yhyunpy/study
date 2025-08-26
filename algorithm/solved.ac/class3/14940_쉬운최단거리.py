import sys
from collections import deque

N, M = map(int, sys.stdin.readline().split())

graph = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

move = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def main():
    """
    처음 주어진 그래프대로 not visit을 1로 설정하면 실제 거리 1인 칸에서는 visit 여부를 알 수 없게 된다.
    """
    queue = deque()

    def bfs():
        while queue:
            now_x, now_y = queue.popleft()
            for dx, dy in move:
                x = now_x + dx
                y = now_y + dy
                if 0 <= x < N and 0 <= y < M:
                    if graph[x][y] == -1:
                        graph[x][y] = graph[now_x][now_y] + 1
                        queue.append((x, y))


    for i in range(N):
        for j in range(M):
            if graph[i][j] == 2:
                graph[i][j] = 0
                queue.append((i, j))
            # -1로 not visit를 표시
            if graph[i][j] == 1:
                graph[i][j] = -1

    bfs()

    for i in range(N):
        temp = ""
        for j in range(M):
            temp += str(graph[i][j])
            temp += " "
        print(temp)

if __name__ == "__main__":
    main()
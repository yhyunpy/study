import sys

N, M = map(int, sys.stdin.readline().split())

graph = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

shapes = [
    # -
    [(0, 1), (0, 2), (0, 3)],
    [(1, 0), (2, 0), (3, 0)],
    # ㅁ
    [(0, 1), (1, 0), (1, 1)],
    # ㄴ
    [(1, 0), (2, 0), (2, 1)],
    [(1, 0), (2, 0), (2, -1)],
    [(1, 0), (2, 0), (0, 1)],
    [(1, 0), (2, 0), (0, -1)],
    [(0, 1), (0, 2), (-1, 2)],
    [(0, 1), (0, 2), (1, 2)],
    [(0, 1), (0, 2), (-1, 0)],
    [(0, 1), (0, 2), (1, 0)],
    # ㄴㄱ
    [(1, 0), (1, 1), (2, 1)],
    [(1, 0), (1, -1), (2, -1)],
    [(0, -1), (1, -1), (1, -2)],
    [(0, 1), (1, 1), (1, 2)],
    # ㅗ
    [(0, 1), (0, 2), (1, 1)],
    [(0, 1), (0, 2), (-1, 1)],
    [(1, 0), (2, 0), (1, 1)],
    [(1, 0), (2, 0), (1, -1)],
]


def main():
    res = 0

    def calc(i, j):
        nonlocal res
        for shape in shapes:
            shape_sum = graph[i][j]
            for dx, dy in shape:
                x = i + dx
                y = j + dy
                if 0 <= x < N and 0 <= y < M:
                    shape_sum += graph[x][y]
                else:
                    break
            else:
                res = max(res, shape_sum)

    for i in range(N):
        for j in range(M):
            calc(i, j)

    print(res)


if __name__ == "__main__":
    main()

import sys

sys.setrecursionlimit(10**6)

N = int(sys.stdin.readline())

n_dict = {}
for _ in range(N):
    info = list(map(int, sys.stdin.readline().split()))

    temp = []
    for i in range(1, len(info) - 1, 2):
        temp.append((info[i], info[i + 1]))
    n_dict[info[0]] = temp


def main():
    """
    트리의 지름이란
    1. 임의의 정점에서 가장 먼 노드를 찾는다
    2. 그 노드에서 가장 먼 노드까지의 거리가 트리의 지름이다

    모든 정점에서 DFS/BFS 시도하면 타임오버 발생
    """

    def find_fartest(start_point):
        total_len = [-1 for _ in range(N + 1)]
        total_len[start_point] = 0

        def dfs(start_point):
            now_len = total_len[start_point]
            for next_point, part_len in n_dict[start_point]:
                if total_len[next_point] == -1:
                    total_len[next_point] = now_len + part_len
                    dfs(next_point)

        dfs(start_point)

        fartest_node = total_len.index(max(total_len))
        return fartest_node, max(total_len)

    # 임의의 정점에서 가장 먼 노드
    fartest_node, _ = find_fartest(1)
    # 그 노드에서 가장 먼 노드까지의 거리
    _, ans = find_fartest(fartest_node)

    print(ans)


main()

import sys


def solution(N, K, items):
    """
    0-1 냅색문제
    dp[i][w] = i번째 물건까지 고려했을 때 가방 무게 w일 때의 최대 가치
    """
    dp = [[0] * (K + 1) for _ in range(N + 1)]

    for i in range(1, N + 1):  # 1번 물건부터 N번까지
        weight, value = items[i - 1]
        for w in range(K + 1):  # 가방 무게 0부터 K까지
            if w < weight:
                # 못 담음
                dp[i][w] = dp[i - 1][w]
            else:
                # 안 담는 경우 : dp[i-1][w]
                # 담는 경우 : dp[i-1][w-weight] + value
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)

    print(dp[N][K])


N, K = map(int, sys.stdin.readline().split())

items = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

solution(N, K, items)

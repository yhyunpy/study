import sys
from collections import deque

N, K = map(int, sys.stdin.readline().split())

queue = deque()

queue.append((N, 0))


visited = [False for _ in range(100001)]
visited[N] = True

while queue:
    now, cnt = queue.popleft()
    # visited[now] = 1 bfs에서 visited 처리를 큐에서 꺼낼 때 하면 중복 발생 가능함
    if now == K:
        print(cnt)
        break
    else:
        for move in (now - 1, now + 1, now * 2):
            if 0 <= move <= 100000 and not visited[move]:
                visited[move] = True
                queue.append((move, cnt + 1))

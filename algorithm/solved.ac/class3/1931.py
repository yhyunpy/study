import sys

N = int(sys.stdin.readline())

times = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

times.sort(key=lambda x: (x[1], x[0]))

start, end = times[0]
cnt = 1
for i in range(1, N):
    now_start, now_end = times[i]
    if now_start >= end:
        cnt += 1
        end = now_end

print(cnt)
import sys

T = int(sys.stdin.readline())


ans_list = [None for _ in range(41)]
ans_list[0] = (1, 0)
ans_list[1] = (0, 1)


def fibo_2(n):
    if ans_list[n] is not None:
        return ans_list[n]
    else:
        a1, b1 = fibo_2(n - 1)
        a2, b2 = fibo_2(n - 2)
        ans_list[n] = a1 + a2, b1 + b2
        return ans_list[n]


for _ in range(T):
    n = int(sys.stdin.readline())
    a, b = fibo_2(n)
    print(a, b)

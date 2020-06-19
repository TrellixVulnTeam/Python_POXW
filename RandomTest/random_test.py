"""
@file: random_test.py
@time: 2020/1/2
@author: alfons
"""
import random

def func(num):
    for _ in range(10):
        if _ == num:
            return
    else:
        print("{} -> hahah".format(num))

func(1)
func(10)

lun_path = "/dev/qdisk/LUN2"
index = lun_path.rfind('LUN') +3
qlink_port = int(lun_path[index:]) + 3260
r1 = random.sample([1, 2, 3, 4, 5, 6], 2)
print(r1)
pass

r = random.Random()

for i in range(20):
    print(r.gauss(0, 1))


def random_split(N, K):
    if K == 1:
        return [N]

    points = random.sample(list(range(1, N)), K - 1)
    points.sort()

    splits = [points[0]]
    for idx in range(K - 2):
        splits.append(points[idx + 1] - points[idx])
    splits.append(N - points[-1])

    return splits


l = random_split(200, 20)
print("l={}".format(l))
print(sum(l))
pass


def random_split_with_limit(N, K, L):
    if K * (L + 1) < 2 * N:
        N = K * (L + 1) - N
        splits, times = random_split_with_limit(K * (L + 1) - N, K, L)
        return [L + 1 - x for x in splits], times

    times = 0
    while True:
        times += 1
        splits = random_split(N, K)
        if max(splits) <= L:
            return splits, times


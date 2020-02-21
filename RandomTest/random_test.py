"""
@file: random_test.py
@time: 2020/1/2
@author: alfons
"""
import random

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


import difflib
import string

url1 = '''{"nvme13n2": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme13n2", "writes": 4525734, "used_size": "1.267 TB", "reads": 1053183}, "nvme1n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme1n1", "writes": 4463199, "used_size": "1.267 TB", "reads": 1044875}, "nvme12n2": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme12n2", "writes": 4326266, "used_size": "1.267 TB", "reads": 687821}, "nvme9n1": {"state": "not used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme9n1", "writes": 0, "used_size": "0", "reads": 0}, "nvme11n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme11n1", "writes": 4321656, "used_size": "1.267 TB", "reads": 676567}, "nvme0n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme0n1", "writes": 4345844, "used_size": "1.267 TB", "reads": 821567}, "nvme6n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme6n1", "writes": 3270959, "used_size": "1.267 TB", "reads": 564048}, "nvme3n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme3n1", "writes": 4319878, "used_size": "1.267 TB", "reads": 735499}, "nvme5n1": {"state": "not used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme5n1", "writes": 0, "used_size": "0", "reads": 0}, "nvme7n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme7n1", "writes": 3528687, "used_size": "1.267 TB", "reads": 554395}, "nvme8n1": {"state": "not used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme8n1", "writes": 0, "used_size": "0", "reads": 0}}'''
url2 = '''{"nvme13n2": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme13n2", "writes": 4209563, "used_size": "1.267 TB", "reads": 1036476}, "nvme1n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme1n1", "writes": 4154055, "used_size": "1.267 TB", "reads": 1020985}, "nvme12n2": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme12n2", "writes": 4034052, "used_size": "1.267 TB", "reads": 667463}, "nvme9n1": {"state": "not used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme9n1", "writes": 0, "used_size": "0", "reads": 0}, "nvme11n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme11n1", "writes": 4039583, "used_size": "1.267 TB", "reads": 655448}, "nvme0n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme0n1", "writes": 4051750, "used_size": "1.267 TB", "reads": 799583}, "nvme6n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme6n1", "writes": 3086753, "used_size": "1.267 TB", "reads": 560532}, "nvme3n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme3n1", "writes": 4041749, "used_size": "1.267 TB", "reads": 716637}, "nvme5n1": {"state": "not used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme5n1", "writes": 0, "used_size": "0", "reads": 0}, "nvme7n1": {"state": "used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme7n1", "writes": 3294373, "used_size": "1.267 TB", "reads": 550417}, "nvme8n1": {"state": "not used", "type": "NVMe SSD", "total_size": "3.20TB", "path": "/dev/nvme8n1", "writes": 0, "used_size": "0", "reads": 0}}'''

r = reduce(lambda x, y: x ^ y, [ord(c) for c in list(url1)])

l1 = ''.join([i for i in url1 if i in string.ascii_letters + string.digits])
l2 = ''.join([i for i in url2 if i in string.ascii_letters + string.digits])

d = difflib.Differ()
diff = d.compare([l1], [l2])
diff_list = list(diff)
print("\n".join(diff_list))

pv_path, vg_name = "/dev/nvme0n1 volgg2".split(' ')

pv_path = pv_path[pv_path.rfind('/') + 1:]
pass

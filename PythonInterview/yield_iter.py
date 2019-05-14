"""
@author: Alfons
@contact: alfons_xh@163.com
@file: yield_iter.py
@time: 2019/4/6 下午7:22
@version: v1.0 
"""
y = (i for i in range(3))

for i in y:
    print(i)

for j in y:
    print(j)


class Bank:  # let's create a bank, building ATMs
    crisis = False

    def create_atm(self):
        while not self.crisis:
            yield "$100"


bank = Bank()
atm = bank.create_atm()
print(next(atm))
print(next(atm))
bank.crisis = True
try:
    print(next(atm))
    print(next(atm))
except StopIteration:

    bank.crisis = False
    atm_2 = bank.create_atm()
    print(next(atm_2))
    print(next(atm_2))

list_a = [1, 2, 3, 4, 5, 6]
iter_a = iter(list_a)
for i in iter_a:
    if i == 3:
        break
    print(i)

print(list(iter_a))


def gen():
    i = 1
    while True:
        j = yield i
        i *= 2
        print("j = ", j)
        if j == -1:
            break


g = gen()
print(next(g))
print(next(g))
# print(g.send(-1))
from dis import dis
print(dis(gen))

from multiprocessing import Pipe

pipe = Pipe()
pipe[0].recv()

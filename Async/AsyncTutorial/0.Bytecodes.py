"""
@file: 0.Bytecodes.py
@time: 2019/8/26
@author: alfons
"""
import dis


def foo():
    result = yield 111
    print(f'result of yield: {result}\n')
    result2 = yield 222
    print(f'result of 2nd yield: {result2}\n')
    return 'done'


dis.dis(foo)

print("=" * 60, flush=True)

first_res = gen = foo()
print("First -> {}, lasti -> {}".format(first_res, gen.gi_frame.f_lasti), flush=True)

second_res = gen.send(None)      # 触发生成器，并将 111 返回，流程走到第一个yield处暂停
print("Second -> {}, lasti -> {}".format(second_res, gen.gi_frame.f_lasti), flush=True)

third_res = gen.send("hello")   # send方法恢复暂停的生成器，并将hello发送给生成器，yield左边接收hello，并打印，程序继续执行至下一个yield处，此时返回222
print("Third -> {}, lasti -> {}".format(third_res, gen.gi_frame.f_lasti), flush=True)

try:
    gen.send("world")   # 此时send完后，result2接收到world，下面没有了yield语句，抛出StopIteration异常
except StopIteration as e:
    print(str(e))
    try:
        print("Four -> {}".format(gen.gi_frame.f_lasti))
    except:
        pass
    pass

# ===============================output======================================
#  12           0 LOAD_CONST               1 (111)
#               2 YIELD_VALUE
#               4 STORE_FAST               0 (result)
#
#  13           6 LOAD_GLOBAL              0 (print)
#               8 LOAD_CONST               2 ('result of yield: ')
#              10 LOAD_FAST                0 (result)
#              12 FORMAT_VALUE             0
#              14 BUILD_STRING             2
#              16 CALL_FUNCTION            1
#              18 POP_TOP
#
#  14          20 LOAD_CONST               3 (222)
#              22 YIELD_VALUE
#              24 STORE_FAST               1 (result2)
#
#  15          26 LOAD_GLOBAL              0 (print)
#              28 LOAD_CONST               4 ('result of 2nd yield: ')
#              30 LOAD_FAST                1 (result2)
#              32 FORMAT_VALUE             0
#              34 BUILD_STRING             2
#              36 CALL_FUNCTION            1
#              38 POP_TOP
#
#  16          40 LOAD_CONST               5 ('done')
#              42 RETURN_VALUE
# ============================================================
# First -> <generator object foo at 0x000001FB3647B848>, lasti -> -1
# Second -> 111, lasti -> 2
# result of yield: hello
#
# Third -> 222, lasti -> 24
# result of 2nd yield: world

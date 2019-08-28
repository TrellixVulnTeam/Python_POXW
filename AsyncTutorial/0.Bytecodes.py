"""
@file: 0.Bytecodes.py
@time: 2019/8/26
@author: alfons
"""
import dis


def foo():
    result = yield 111
    print(f'result of yield: {result}')
    result2 = yield 222
    print(f'result of 2nd yield: {result2}')
    return 'done'


dis.dis(foo)

print("=" * 60, flush=True)

gen = foo()
print("First -> {}\n".format(gen.gi_frame.f_lasti), flush=True)

gen.send(None)
print("Second -> {}\n".format(gen.gi_frame.f_lasti), flush=True)

gen.send("hello")
print("Third -> {}\n".format(gen.gi_frame.f_lasti), flush=True)

try:
    gen.send("world")
except StopIteration:
    try:
        print("Four -> {}\n".format(gen.gi_frame.f_lasti))
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
# First -> -1
#
# Second -> 2
#
# result of yield: hello
# Third -> 22
#
# result of 2nd yield: world

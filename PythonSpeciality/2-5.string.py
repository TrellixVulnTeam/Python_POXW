"""
@author: Alfons
@contact: alfons_xh@163.com
@file: 2-5.string.py
@time: 2019/8/11 上午10:52
@version: v1.0 
"""
name = "Alfons"
error = 12345678

# 旧式字符串格式化
str_a = "Hey %(name)s, this is a 0x%(error)x error!" % dict(name=name, error=error)
print(str_a)

# 新式字符串格式化
str_b = "Hey {name}, this is a 0x{error:x} error!".format(name=name, error=error)
print(str_b)

# 字符串字面值插值,Python3.6+
str_c = f"Hey {name}, this is a 0x{error:x} error!"
print(str_c)

# 模板字符串
from string import Template

str_d = Template("Hey $name, this is a $error error!")
print(str_d.substitute(name=name, error=hex(error)))

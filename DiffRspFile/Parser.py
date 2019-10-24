"""
@file: Parser.py
@time: 2019/10/23
@author: alfons
"""
grid_19c = "./grid_19c.rsp"
grid_12c = "./grid_12c.rsp"

db_19c = "./db_19c.rsp"
db_12c = "./db_12c.rsp"


def read_config_key(file_path):
    with open(file_path, "r") as f:
        return {line.split('=')[0] for line in f.readlines() if not line.startswith('#')}


def diff(file_a, file_b):
    a_config_key_set = read_config_key(file_a)
    b_config_key_set = read_config_key(file_b)

    print('{a} - {b}:\n{c}'.format(a=file_a, b=file_b, c='\n'.join(a_config_key_set - b_config_key_set)))
    print("\n\n")
    print('{b} - {a}:\n{c}'.format(a=file_a, b=file_b, c='\n'.join(b_config_key_set - a_config_key_set)))


print("=" * 30 + "grid diff" + "=" * 30)
diff(grid_19c, grid_12c)
# diff(grid_19c, "./grid_install.rsp")

print("=" * 30 + "db diff" + "=" * 30)
diff(db_19c, db_12c)
# diff(db_19c, "./db_install.rsp")

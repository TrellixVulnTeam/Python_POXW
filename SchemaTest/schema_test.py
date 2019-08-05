"""
@file: schema_test.py
@time: 2019/8/2
@author: alfons
"""
from schema import Schema, And

print(Schema(int).validate(10))
print(Schema(And(int, lambda a: a > 20)).validate(30))
# Schema(int).validate("10")
print(Schema([int, str]).validate([10]))

print(Schema({"name": str, "age": And(int, lambda a: a > 18, error="此人未成年！")}).validate({"name": "Alfons", "age": 20}))

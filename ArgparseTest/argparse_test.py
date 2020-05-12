"""
@file: argparse_test.py
@time: 2020/1/2
@author: alfons
"""
from pprint import pprint
import argparse
from argparse import _SubParsersAction


def func_a(*args, **kwargs):
    print("I'm func_a, args={}, kwargs={}".format(args, kwargs))


parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--foo', action='store_true', help='foo help')

# sub parser
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('--bar', type=int, help='bar help')
parser_a.set_defaults(func=func_a)

# create the parser for the "b" command
parser_b = subparsers.add_parser('b', help='b help')
parser_b.add_argument('--baz', choices='XYZ', help='baz help')

# parser.format_usage()
help = parser.format_help()

# for action in parser._actions:
#     if not isinstance(action, _SubParsersAction):
#         print("{} -> {}".format(action.option_strings, action.help))
#
for action_group in parser._action_groups:
    pprint(action_group._actions)
    pprint(action_group._group_actions)
    pass
#
#
# print("parser._actions -> {}")
# pprint(parser._actions)
#
# print("parser._option_string_actions -> {}")
# pprint(parser._option_string_actions)
#
# print("parser._action_groups -> {}")
# pprint(parser._action_groups)
#
# print("parser._mutually_exclusive_groups -> {}")
# pprint(parser._mutually_exclusive_groups)
#
# print("parser._defaults -> {}")
# pprint(parser._defaults)
#
# print("parser._has_negative_number_optionals -> {}")
# pprint(parser._has_negative_number_optionals)
#
# pprint(parser._get_args())
# pprint(parser._get_kwargs())
# pprint(subparsers._get_subactions())
# pprint(subparsers._option_string_actions)
# argv = ['-h']
# args = parser.parse_args(argv)
# args.func(argv)
# parse some argument lists
# parser.parse_args(['a', '12'])
# parser.parse_args(['--foo', 'b', '--baz', 'Z'])

"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : UserAgentsParserTest.py
 @Time    : 2019/1/3 16:02
"""
from ua_parser import user_agent_parser
import pprint

pp = pprint.PrettyPrinter(indent=4)

ua_string = "Android 8.1.0; COL-AL10 Build/HUAWEICOL-AL10"
parsed_string = user_agent_parser.Parse(ua_string)
pp.pprint(parsed_string)
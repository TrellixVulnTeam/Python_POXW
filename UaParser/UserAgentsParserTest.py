"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : UserAgentsParserTest.py
 @Time    : 2019/1/3 16:02
"""
from ua_parser import user_agent_parser
import pprint

pp = pprint.PrettyPrinter(indent = 4)

# ua_string = "Android 8.1.0; COL-AL10 Build/HUAWEICOL-AL10"
with open("./android.txt", 'r') as f:
    ua_list = [ua.strip() for ua in f.readlines()]

result = list()
result.append("Ori,family,brand,model")
for ua_string in ua_list:
    parsed_string = user_agent_parser.Parse(ua_string)
    print(parsed_string['device'])
    result.append("{ua},{family},{brand},{model}".format(ua = ua_string.replace(',', ' '),
                                                         family = parsed_string['device']['family'],
                                                         brand = parsed_string['device']['brand'],
                                                         model = parsed_string['device']['model']))

with open("result.csv", "w") as f:
    f.writelines("\n".join(result))

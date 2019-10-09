"""
@file: docopt_test.py
@time: 2019/10/9
@author: alfons
"""
from docopt import docopt

doc = """
Usage:
  alfons config ip <ip>
  alfons config port <port>
  alfons config login
  alfons group list
  alfons group choose <group_name>...
  alfons group clean
  alfons group send -t <content>
  alfons group send -i <media>
  alfons group send -f <file> [<delaytime>]

Options:
  -h --help     Show this screen.
  -v --version     Show version.
"""

argvs = ["config", "ip", "10.10.100.1"]

args = docopt(doc, argv=argvs, version="alfons v0.0.0")

print(args)


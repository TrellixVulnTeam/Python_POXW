"""
@file: DnsParser.py
@time: 2018/12/26
@author: sch
"""
import os
import dns.resolver
import dns.rdtypes
import traceback


def DnsResolver():
    host_list = list()
    host_src_file = "./domain.txt"
    host_store_file = "./host.txt"

    with open(host_src_file, "r") as f:
        dns_list = [line.strip() for line in f.readlines()]

    if os.path.exists(host_store_file):
        with open(host_store_file, 'r') as f:
            for line in f.readlines():
                host_list.append(line.split(":")[-1].strip())

    host_file = open(host_store_file, "a")

    while True:
        for host_name in dns_list:
            try:
                A = dns.resolver.query(host_name, 'A')
                for i in A.response.answer:
                    for j in i.items:
                        if not isinstance(j, dns.rdtypes.IN.A.A):
                            continue

                        if j.address in host_list:
                            continue

                        host_list.append(j.address)
                        host_file.write(str(repr(i.name) + ": " + j.address + "\n"))
                        host_file.flush()
                        print(i.name, ": ", j.address)

                cname = dns.resolver.query(host_name, 'CNAME')
                for i in cname.response.answer:
                    for j in i.items:
                        if not isinstance(j, dns.rdtypes.nsbase.NSBase):
                            continue

                        if j.target in host_list:
                            continue

                        host_list.append(j.target)
                        host_file.write(str(repr(i.name) + ": " + repr(j.target) + "\n"))
                        host_file.flush()
                        print(i.name, " CNAME: ", j.target)
            except dns.resolver.NoAnswer:
                continue
            except:
                traceback.print_exc()
                pass


def IPSort():
    import sys
    print(os.getcwd())
    host_store_file = "./host.txt"
    host_sort_file = "./host2.txt"
    host_list = list()

    if os.path.exists(host_store_file):
        with open(host_store_file, 'r') as f:
            for line in f.readlines():
                host_list.append(line.split(":")[-1].strip())

    host_list = sorted(host_list)

    with open(host_sort_file, 'w') as f:
        f.write("\n".join(host_list))


if __name__ == '__main__':
    # DnsResolver()
    IPSort()

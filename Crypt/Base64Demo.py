#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Base64Demo.py 
@time: 2018/1/23 11:03 
@version: v1.0 
"""
import base64
import AES

key = "i7dcFYk6/qw4AWP1AeAzqPRzX6Tujb6eRPzCFg2qbMer9v1lm3U6ehBDaELoCFOj"
# plaintxt = "YkfIZK9m+SOFFQdcjMFJupcpm/nEaHp9JafWC5FsD8s5CfZDe25oIzs9LF9lN+NFbNjaDZpcjl1wviBMWPHuYA=="
plaintxt = "W2t1bmJhbmcxXQppZD1rdXdvX3VwZGF0ZQp1cmw9aHR0cDovL2Rvd24ua3V3by5jbi9tYm94L2t1d29fam00MTcuZXhlCmZpbGU9a3V3b19qbTQxNy5leGUKcHJvY2Vzcz1bS3dNdXNpYy5leGVdCnRleHQ96YW35oiR6Z+z5LmQJCQkJOS4reWbveacgOaWsOacgOWFqOeahOWcqOe6v+ato+eJiOmfs+S5kOi9r+S7tgpyZWc9W0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxVbmluc3RhbGxcS3dNdXNpYzckJCQkVW5pbnN0YWxsU3RyaW5nXQpyZXBlYXQ9MApzdGF0cz0xCnNob3c9a3VuYmFuZzEKdmVyc2lvbj1IS0VZX0xPQ0FMX01BQ0hJTkVcU09GVFdBUkVcTWljcm9zb2Z0XFdpbmRvd3NcQ3VycmVudFZlcnNpb25cVW5pbnN0YWxsXEt3TXVzaWM3JCQkJERpc3BsYXlWZXJzaW9uJCQkJDguNy40LjAKCltrdW5iYW5nMl0KaWQ9MzYwc2RfdXBkYXRlCnVybD1odHRwOi8vZGwyLjM2MHNhZmUuY29tL3BhcnRuZXIvSW5zdDEzX18yMTEwMDEwLmV4ZQpmaWxlPUluc3QxM19fMjExMDAxMC5leGUKY29tbWFuZD0vUwpwcm9jZXNzPVszNjB0cmF5LmV4ZV1bMzYwc2QuZXhlXVtaaHVEb25nRmFuZ1l1LmV4ZV1bMzYwc2FmZS5leGVdCnRleHQ9MzYw5a6J5YWo5Y2r5aOrJCQkJOi9u+W3p+W/q+mAn+WFjeaJk+aJsO+8jOW8uuWKm+adgOavkuS4jeWNoeacugpyZWc9W0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxVbmluc3RhbGxcMzYw5a6J5YWo5Y2r5aOrJCQkJFVuaW5zdGFsbFN0cmluZ11bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXFVuaW5zdGFsbFwzNjBzZCQkJCRVbmluc3RhbGxTdHJpbmddW0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxBcHAgUGF0aHNcMzYwc2FmZS5leGUkJCQkUGF0aF1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXEFwcCBQYXRoc1wzNjBzZC5leGUkJCQkUGF0aF0KcmVwZWF0PTAKc2hvdz0zNjAKcmVzZXJ2ZT1sdWRhc2hpCgpbbHVkYXNoaV0KaWQ9bHVkYXNoaV91cGRhdGUKdXJsPWh0dHA6Ly9kb3duLjM2MHNhZmUuY29tL2x1ZGFzaGkvaW5zdF9wcHMuZXhlCmZpbGU9aW5zdF9wcHMuZXhlCnByb2Nlc3M9W0NvbXB1dGVyWl9DTi5leGVdCnRleHQ96bKB5aSn5biIJCQkJOacgOaHguS9oOeahOehrOS7tgpyZWc9W0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxVbmluc3RhbGxcTHVkYXNoaV9pczEkJCQkRGlzcGxheUljb25dCnJlcGVhdD0wCnJlZ3N0YXQ9MApzaG93PTBfdXBkYXRlCgpba3VuYmFuZzNdCmlkPWR1YmFfdXBkYXRlCnVybD1odHRwOi8vY2QwMDEud3d3LmR1YmEubmV0L2R1YmEvaW5zdGFsbC8yMDExL2V2ZXIva2luc3RfMTJfOS5leGUKZmlsZT1raW5zdF8xMl85LmV4ZQpwcm9jZXNzPVtreGVzY29yZS5leGVdWzM2MHRyYXkuZXhlXVszNjBzZC5leGVdW1podURvbmdGYW5nWXUuZXhlXVszNjBzYWZlLmV4ZV0KdGV4dD3ph5HlsbHmr5LpnLgkJCQk57qv5YeA5YWN6LS55p2A5q+S77yM5o+Q5Y2H55S16ISR5oCn6IO9CnJlZz1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXFVuaW5zdGFsbFxLaW5nc29mdCBJbnRlcm5ldCBTZWN1cml0eSQkJCRVbmluc3RhbGxTdHJpbmddW0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxVbmluc3RhbGxcMzYw5a6J5YWo5Y2r5aOrJCQkJFVuaW5zdGFsbFN0cmluZ11bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXFVuaW5zdGFsbFwzNjBzZCQkJCRVbmluc3RhbGxTdHJpbmddW0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxBcHAgUGF0aHNcMzYwc2FmZS5leGUkJCQkUGF0aF1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXEFwcCBQYXRoc1wzNjBzZC5leGUkJCQkUGF0aF0KcmVwZWF0PTAKc2hvdz1kdWJhCnJlZ3N0YXQ9MApyZXNlcnZlPWRmc3JmCgpbZGZzcmZdCmlkPWRmc3JmX3VwZGF0ZQp1cmw9aHR0cDovL2Rvd24uem55c2h1cnVmYS5jb20vcWRiL3pueV96bnl3YmtiMDcxLmV4ZQpmaWxlPXpueV96bnl3YmtiMDcxLmV4ZQpjb21tYW5kPS9TCnByb2Nlc3M9W1NDQ2xvdWQuZXhlXVtTQ1dCQ2xvdWQuZXhlXQp0ZXh0PeaZuuiDveS6kei+k+WFpeazlSQkJCTljaDnlKjlhoXlrZjlsI/vvIzmiZPlrZfpgJ/luqblv6sKcmVnPVtIS0VZX0xPQ0FMX01BQ0hJTkVcU09GVFdBUkVcU21hcnRDbG91ZElucHV0JCQkJExhc3RJbnN0YWxsVGltZV1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXFNtYXJ0Q2xvdWRXQklucHV0JCQkJExhc3RJbnN0YWxsVGltZV1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXFUwTkVZWFJsJCQkJExhc3RJbnN0YWxsVGltZV1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxXaW5kb3dzXEN1cnJlbnRWZXJzaW9uXFVuaW5zdGFsbFzmmbrog73kupHovpPlhaXms5UkJCQkRGlzcGxheU5hbWVdW0hLRVlfTE9DQUxfTUFDSElORVxTT0ZUV0FSRVxNaWNyb3NvZnRcV2luZG93c1xDdXJyZW50VmVyc2lvblxVbmluc3RhbGxc5pm66IO95LqR5LqU56yU6L6T5YWl5rOVJCQkJERpc3BsYXlOYW1lXQpyZXBlYXQ9MApzaG93PWRmc3JmCgpba3VuYmFuZzRdCmlkPWt1YWl6aXBfdXBkYXRlCnVybD1odHRwOi8vZGwua2tkb3dubG9hZC5jb20va3phcWkvS3VhaVppcF9TZXR1cF8xMTQ3NTIyNjU2X2FxaV8wMDIuZXhlCmZpbGU9S3VhaVppcF9TZXR1cF8xMTQ3NTIyNjU2X2FxaV8wMDIuZXhlCnByb2Nlc3M9W0t1YWlaaXAuZXhlXQp0ZXh0PeW/q+WOi+WOi+e8qSQkJCTlhY3otLnjgIHmlrnkvr/jgIHlv6vpgJ8KcmVnPVtIS0VZX0xPQ0FMX01BQ0hJTkVcU09GVFdBUkVcTWljcm9zb2Z0XFdpbmRvd3NcQ3VycmVudFZlcnNpb25cVW5pbnN0YWxsXEt1YWlaaXAkJCQkVW5pbnN0YWxsU3RyaW5nXQpyZXBlYXQ9MApzaG93PWt1YWl6aXAKCltrdW5iYW5nNV0KaWQ9c29nb3VfdXBkYXRlCnVybD1odHRwOi8vY2RuMS5pbWUuc29nb3UuY29tL3NvZ291X3Bpbnlpbl84LjQuMC4xMDM5XzcwMTUuZXhlCmZpbGU9c29nb3VfcGlueWluXzguNC4wLjEwMzlfNzAxNS5leGUKcHJvY2Vzcz1bU0dUb29sLmV4ZV0KdGV4dD3mkJzni5fovpPlhaXms5UkJCQk5L2T6aqM5pCc54uX6L6T5YWl5rOV77yM6K+N5bqT5YWo5omT5a2X5YeGCnJlZz1bSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXFNvZ291SW5wdXQkJCQkdmVyc2lvbl0KcmVwZWF0PTAKc2hvdz1zb2dvdQoKW29wdGlvbl0KU2V0SG9tZVN3aXRjaD0wClNldEhvbWVTdGF0ZT0xClNldEhvbWVUeXBlPTEKU2V0SG9tZVVybD1odHRwOi8vOTIyMy5wcHMudHYvClNldEhvbWVUZXh0PTEKQ2xpZW50VmVyc2lvbj02LjEuNTEuNDg4NgpDbGllbnRWZXJzaW9uVGltZT0yMDE3LjguMzEuMTMuMjAuMjcKQ2xpZW50VmVyc2lvblRleHQ95pu05paw5pel5b+XfDEu5pKt5pS+5Zmo55WM6Z2i5LyY5YyWfDIu5pKt5pS+5oCn6IO95LyY5YyWfDMu57K+566A5a6J6KOF5YyFfDQu6Iul5bmyYnVn5L+u5aSNCkNsaWVudFZlcnNpb25UeXBlPTEKS3VuYmFuZ1N3aXRjaD0xCkt1bmJhbmdDb3VudD00Ckt1bmJhbmdTZXRCdXR0b249MApVcGRhdGVTd2l0Y2g9MQpTZXREaXJBY2Nlc3M9MApHZWVQbGF5ZXJTd2l0Y2g9MQpHZWVQbGF5ZXJWZXJzaW9uPTMuMS40Ni40MDE5CgpbQWRkcmVzc0Jhcl0KQWRkcmVzc0JhclN3aXRjaD0wCkFkZHJlc3NCYXJVcmw9aHR0cDovL2RsLnN0YXRpYy5pcWl5aS5jb20vaHovQWRkci5leGUKQWRkcmVzc0JhckZpbGU9QWRkci5leGUKQWRkcmVzc0JhclJlZz1IS0VZX0xPQ0FMX01BQ0hJTkVcU09GVFdBUkVcTWljcm9zb2Z0XFdpbmRvd3NcQ3VycmVudFZlcnNpb25cVW5pbnN0YWxsXEFkZHIyMDEzMDUkJCQkVW5pbnN0YWxsU3RyaW5nCgpbdm1QYWdlXQp2bVBhZ2VVcmw9aHR0cDovL3ZvZGd1aWRlLnBwc3RyZWFtLmlxaXlpLmNvbS9zZWFyY2gucGhwP3Zlcj0kdmVyJAp2bVBhZ2VGaWxlPXNlYXJjaF90b3AuemlwCgpbUmVsb2FkXQpSZWxvYWQ9MQ=="
test = "xOO6w6OsU25haVgNCg0KoaGhodXiysfSu7j2QmFzZTY0tcSy4srU08q8/qOhDQoNCkJlc3QgV2lzaGVzIQ0KIAkJCQkNCqGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaEgICAgICAgICAgICAgICBlU1g/IQ0KoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoSAgICAgICAgICAgICAgIHNuYWl4QHllYWgubmV0DQqhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhICAgICAgICAgMjAwMy0xMi0yNQ0K"
# testCode = test.encode("base64")
# print(testCode)
# print(testCode.decode("base64"))
# print(len(key))
# key_list = set(list(key))
#
# print(len(key_list))
# new_plaint = plaintxt
new_plaint = plaintxt
print(base64.decodestring(new_plaint))
with open(u"spider.pps.tv_6.0.46.4561_升级日志", "wb") as f:
    f.write(base64.decodestring(new_plaint))

# with open("E:\Download\urlBaseG.enc", "rb") as f1:
#     with open("E:\Download\urldecode.txt", "wb") as f2:
#         base64.decode(f1, f2)

import base64
# import AES
#
# with open("update.jar", "rb") as f:
#     print(AES.md5(f.read()))
# with open("request1", "rb") as f:
#     file_binary = f.read()
#     # print(len(file_binary))
#     for i in range(1, 8):
#         try:
#             print("%s: " % i)
#             result = AES.AES_ECB_DECRYPT(cipher_text = file_binary[32:][::-1], key = file_binary[:32][::-1], mode = i)
#             print(result)
#             with open("request1_decode", "wb") as f2:
#                 f2.write(AES.b2a_hex(file_binary[:32]))
#             print("\n")
#         except:
#             pass

# header = {
#     "Accept": "*/*",
#     "User-Agent": "Update.WPS",
#     "Host": "wup1.cache.wps.cn",
#     "Cache-Control": "no-cache"
# }
#
# import requests
# session = requests.session()
# session.headers = header
# content = session.get(url = "http://wup1.cache.wps.cn/newupdate/2052/pertrial/7106_1/selfpatch/wpsupdate.exe")

# pass
# from StringIO import StringIO
# import gzip
#
# request = urllib2.Request('http://outofmemory.cn/')
# request.add_header('Accept-encoding', 'gzip')
# response = urllib2.urlopen(request)
# if response.info().get('Content-Encoding') == 'gzip':
#     buf = StringIO( response.read())
#     f = gzip.GzipFile(fileobj=buf)
#     data = f.read()

pass

try:
    proc = "fhdsfsa"
    raise LookupError
except LookupError:
    print(proc)

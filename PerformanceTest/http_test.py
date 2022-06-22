#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: http.py
# Desc:
# Version: 0.0.1
# LastChange:  2022/4/13 13:42
# History:
#=============================================================================
"""
from typing import Dict, Any
import time
import requests
from multiprocessing.pool import ThreadPool

REQUEST_GET = "get"
REQUEST_POST = "post"

total_num = 0


# ----------------- request -----------------
def func_request(method: str, url: str, headers: Dict[str, Any], num: int = None, lun: int = 0):
    time.sleep(num)
    if method == REQUEST_GET:
        time_start = time.time()
        response = requests.get(url, headers=headers)
        global total_num
        total_num += 1

        print(f"{lun}-{num} time use {time.time() - time_start}'s: {response.content}.")


def request_test():
    start_time = time.time()
    for j in range(10 ** 5):
        with ThreadPool(2) as pool:
            for i in range(2):
                # pool.apply_async(
                #     func_request,
                #     (
                #         REQUEST_GET,
                #         f"http://192.168.1.92/hulk/api/v1/cluster/qdata/5",
                #         {
                #             "Accept": "application/json",
                #             "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTAzNTU1NDMsInVzZXJfaWQiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLCJ1c2VybmFtZSI6ImFkbWluIn0.yhjmD--zp31qrLYA3kTtb7jm2sl_aiOHQz8GfX7OUt4",
                #         },
                #         i,
                #         j,
                #     )
                # )
                pool.apply_async(
                    func_request,
                    (
                        REQUEST_GET,
                        f"http://192.168.1.92/hulk/api/v1/cluster/qdata/9/rac",
                        {
                            "Accept": "application/json",
                            "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTAzNTU1NDMsInVzZXJfaWQiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLCJ1c2VybmFtZSI6ImFkbWluIn0.yhjmD--zp31qrLYA3kTtb7jm2sl_aiOHQz8GfX7OUt4",
                        },
                        i,
                        j,
                    )
                )
                # pool.apply_async(
                #     func_request,
                #     (
                #         REQUEST_GET,
                #         f"http://10.10.100.70/hulk/api/v1/cluster/qdata/5/rac",
                #         {
                #             "Accept": "application/json",
                #             "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTA2MTM0OTIsInVzZXJfaWQiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLCJ1c2VybmFtZSI6ImFkbWluIn0.7f8MkvV5bLKipsEENlW2k8tICG4FPnotpzE-1lyah7o",
                #         },
                #         i,
                #         j,
                #     )
                # )

            pool.close()
            pool.join()

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


if __name__ == '__main__':
    # aiohttp_test()
    # httpx_test()
    request_test()

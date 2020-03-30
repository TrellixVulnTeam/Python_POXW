"""
@file: qlink_parse.py
@time: 2020/1/5
@author: alfons
"""
import json

with open("./qlink_29.json", "r") as f:
    qlink_show_c_list = json.load(f)

    lun_info_dict = dict()
    for qlink_info in qlink_show_c_list:
        for targets in qlink_info.get("qlink", list()):
            target_port = targets.get("port")   # target绑定的端口
            for target_info in targets.get("targets", list()):
                target_name = target_info.get("targetname", "")
                if not target_name.startswith("s01"):  # 目前所有的盘都聚合在s01上
                    break

                for lun_info in target_info.get("lun_list", list()):
                    lun_path = lun_info.get("m_path", "")
                    lun_name = lun_path[lun_path.rfind('.') + 1:]
                    lun_info_dict.update({lun_name: dict(port=target_port,
                                                         active_ib=[disk_info.get("ib_ip", "")
                                                                    for disk_info in lun_info.get("disks", list())
                                                                    if disk_info.get("status", "") == "active"],
                                                         noactive_ib=[disk_info.get("ib_ip", "")
                                                                      for disk_info in lun_info.get("disks", list())
                                                                      if disk_info.get("status", "") != "active"]
                                                         )
                                          })
            pass
    print(json.dumps(lun_info_dict, indent=4))
    pass

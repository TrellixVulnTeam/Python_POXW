#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: db_py.py
@time: 2019/12/25
@author: alfons
"""
import re

from collections import namedtuple, defaultdict

resource_cls = namedtuple("rsc", "node,rsc,sp")

node_id_dict = {
    "china-mobile-sto203": 5,
    "china-mobile-sto204": 7,
    "china-mobile-sto205": 9,
    "china-mobile-sto206": 11,
}

pool_id = 1
cluster_id = 1

linstor_info_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))


def get_rsc_info_list(rsc_file_path="./linstor_volume_output.txt"):
    global linstor_info_dict

    with open(rsc_file_path, "rb") as f:
        for volume_info_line in f.readlines():
            volume_info_line = volume_info_line.decode()
            volume_re = re.search(r'┊(.*?)┊(.*?)┊(.*?)┊(.*?)┊.*', volume_info_line)
            if volume_re is None:
                continue

            node_name = volume_re.group(1).strip()
            rsc_name = volume_re.group(2).strip()
            sto_pool_name = volume_re.group(3).strip()
            vol_num = volume_re.group(4).strip()

            if node_name not in node_id_dict:
                continue

            linstor_info_dict[node_name][sto_pool_name]["rsc"].append((rsc_name, vol_num))


def get_sp_info_list(sp_file_path="./linstor_sp_output.txt"):
    global linstor_info_dict

    with open(sp_file_path, "rb") as f:
        for sp_info_line in f.readlines():
            sp_info_line = sp_info_line.decode()
            sp_re = re.search(r'┊(.*?)┊(.*?)┊(.*?)┊(.*?)┊.*', sp_info_line)
            if sp_re is None:
                continue

            sp_name = sp_re.group(1).strip()
            node_name = sp_re.group(2).strip()
            vg_name = sp_re.group(4).strip()

            if node_name not in node_id_dict:
                continue

            linstor_info_dict[node_name][sp_name]["vg"].append(vg_name)


if __name__ == '__main__':

    get_rsc_info_list()
    get_sp_info_list()

    resource_group_insert_list = list()
    volume_insert_list = list()
    for node_name, sp_info in linstor_info_dict.items():
        node_id = node_id_dict.get(node_name)

        for sp_name, sp_value in sp_info.items():
            for vg_name in sp_value.get("vg", list()):
                resource_group_insert_list.append(
                    "({}, {}, {}, {}, '{}', {}, {}, '{}')".format(len(resource_group_insert_list) + 1, "'{}'", "NULL", "NULL", sp_name, pool_id, node_id, vg_name))

            for rsc_name in sp_value.get("rsc", list()):
                volume_insert_list.append(
                    "({}, {}, {}, {}, '{}', {}, {}, '{}', '{}', {}, {})".format(len(volume_insert_list) + 1, "'{}'", "NULL", "NULL", '{}_{}'.format(rsc_name[0], rsc_name[1]), pool_id,
                                                                          cluster_id, sp_name, rsc_name[0], rsc_name[1], 3))

    with open("./resource_group_script.sql", 'w') as f:
        f.write("""DROP TABLE IF EXISTS `resource_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resource_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attr` json DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `name` varchar(32) NOT NULL,
  `pool_id` int(11) DEFAULT NULL,
  `node_id` int(11) DEFAULT NULL,
  `vgname` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`pool_id`,`node_id`),
  KEY `pool_id` (`pool_id`),
  KEY `node_id` (`node_id`),
  CONSTRAINT `resource_group_ibfk_1` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`id`) ON DELETE CASCADE,
  CONSTRAINT `resource_group_ibfk_2` FOREIGN KEY (`node_id`) REFERENCES `qdata_node` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_group`
--

LOCK TABLES `resource_group` WRITE;
/*!40000 ALTER TABLE `resource_group` DISABLE KEYS */;
INSERT INTO `resource_group` VALUES %s;
/*!40000 ALTER TABLE `resource_group` ENABLE KEYS */;
UNLOCK TABLES;""" % ','.join(resource_group_insert_list))

    with open("./volume_script.sql", 'w') as f:
        f.write("""
DROP TABLE IF EXISTS `volume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `volume` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attr` json DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `name` varchar(32) NOT NULL,
  `pool_id` int(11) DEFAULT NULL,
  `cluster_id` int(11) DEFAULT NULL,
  `rg_name` varchar(32) NOT NULL,
  `rd_name` varchar(32) NOT NULL,
  `serial_number` int(11) NOT NULL,
  `copy_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pool_id` (`pool_id`),
  KEY `cluster_id` (`cluster_id`),
  CONSTRAINT `volume_ibfk_1` FOREIGN KEY (`pool_id`) REFERENCES `pool` (`id`) ON DELETE CASCADE,
  CONSTRAINT `volume_ibfk_2` FOREIGN KEY (`cluster_id`) REFERENCES `qdata_cluster` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volume`
--

LOCK TABLES `volume` WRITE;
/*!40000 ALTER TABLE `volume` DISABLE KEYS */;
INSERT INTO `volume` VALUES %s;
/*!40000 ALTER TABLE `volume` ENABLE KEYS */;
UNLOCK TABLES;
""" % ','.join(volume_insert_list))

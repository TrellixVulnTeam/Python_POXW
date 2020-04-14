#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: test.py.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/4/8 下午3:38
# History:
#=============================================================================
"""
list_a = ["instance ",
          "512 byte emulation ",
          "current VDO IO requests in progress",
          "maximum VDO IO requests in progress",
          "dedupe advice valid",
          "dedupe advice stale",
          "dedupe advice timeouts ",
          "flush out",
          "write amplification ratio",
          "bios in read ",
          "bios in write",
          "bios in discard",
          "bios in flush",
          "bios in fua",
          "bios in partial read ",
          "bios in partial write",
          "bios in partial discard",
          "bios in partial flush",
          "bios in partial fua",
          "bios out read",
          "bios out write ",
          "bios out discard ",
          "bios out flush ",
          "bios out fua ",
          "bios meta read ",
          "bios meta write",
          "bios meta discard",
          "bios meta flush",
          "bios meta fua",
          "bios journal read",
          "bios journal write ",
          "bios journal discard ",
          "bios journal flush ",
          "bios journal fua ",
          "bios page cache read ",
          "bios page cache write",
          "bios page cache discard",
          "bios page cache flush",
          "bios page cache fua",
          "bios out completed read",
          "bios out completed write ",
          "bios out completed discard ",
          "bios out completed flush ",
          "bios out completed fua ",
          "bios meta completed read ",
          "bios meta completed write",
          "bios meta completed discard",
          "bios meta completed flush",
          "bios meta completed fua",
          "bios journal completed read",
          "bios journal completed write ",
          "bios journal completed discard ",
          "bios journal completed flush ",
          "bios journal completed fua ",
          "bios page cache completed read ",
          "bios page cache completed write",
          "bios page cache completed discard",
          "bios page cache completed flush",
          "bios page cache completed fua",
          "bios acknowledged read ",
          "bios acknowledged write",
          "bios acknowledged discard",
          "bios acknowledged flush",
          "bios acknowledged fua",
          "bios acknowledged partial read ",
          "bios acknowledged partial write",
          "bios acknowledged partial discard",
          "bios acknowledged partial flush",
          "bios acknowledged partial fua",
          "bios in progress read",
          "bios in progress write ",
          "bios in progress discard ",
          "bios in progress flush ",
          "bios in progress fua ",
          "read cache accesses",
          "read cache hits",
          "read cache data hits ",
          "KVDO module bytes used ",
          "KVDO module peak bytes used",
          "KVDO module bios used",
          "KVDO module peak bio count ",
          "entries indexed",
          "posts found",
          "posts not found",
          "queries found",
          "queries not found",
          "updates found",
          "updates not found",
          "current dedupe queries ",
          "maximum dedupe queries ", ]

print '\n'.join('print "{0}: ", stat.get("{1}")'.format(l.strip().ljust(36), l.strip()) for l in list_a)

# import os
# from statistics.VDOStatistics import VDOStatistics
#
# vdo_statistics = VDOStatistics()
# stat = vdo_statistics._getCClass()()
# exist = os.path.exists("/proc/vdo/QP0B00S08/dedupe_stats")
# with open("/proc/vdo/QP0B00S08/dedupe_stats", 'rb') as f:
#     f.readinto(stat)

# print vdo_statistics.labeled(sample=vdo_statistics.getSamples())

# import re
#
# fieldNames = re.compile(r'\$([a-zA-Z0-9_]+)')
#
#
# def func_a(string):
#     derivation = fieldNames.sub(r'parent.getSampleValue(stats, "\1")',
#                                 string)
#     return lambda stats, parent: eval(derivation)
#
#
# func_a("$physicalBlocks * $blockSize / 1024")
# func_a("((not $inRecoveryMode) and ($mode != 'read-only'))")

import json
from collections import OrderedDict
from ctypes import Structure, c_char, c_bool, c_byte, c_ulonglong, c_uint


def get_lower_case_name(text):
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append(" ")
        lst.append(char)

    return "".join(lst).lower()


class VDOStructure(Structure):

    def __repr__(self):
        tmp_dict = OrderedDict()
        for field in self.__dict__:
            try:
                # tmp_dict.update({field[0]: str(getattr(self, field[0]))})
                print "{}: {}".format(field[0], getattr(self, field[0]))
                tmp_dict.update({field[0]: getattr(self, field[0])})
            except Exception as e:
                print str(e)
                print {field[0]: getattr(self, field[0])}
        return str(tmp_dict)


class PackerStatistics(VDOStructure):
    _fields_ = [
        ("compressedFragmentsWritten", c_ulonglong),
        ("compressedBlocksWritten", c_ulonglong),
        ("compressedFragmentsInPacker", c_ulonglong),
    ]


class BlockAllocatorStatistics(VDOStructure):
    _fields_ = [
        ("slabCount", c_ulonglong),
        ("slabsOpened", c_ulonglong),
        ("slabsReopened", c_ulonglong),
    ]


class CommitStatistics(VDOStructure):
    _fields_ = [
        # ("batching", c_ulonglong),
        ("started", c_ulonglong),
        # ("writing", c_ulonglong),
        ("written", c_ulonglong),
        ("committed", c_ulonglong),
    ]

    @property
    def batching(self):
        return self.started - self.written

    @property
    def writing(self):
        return self.written - self.committed


class RecoveryJournalStatistics(VDOStructure):
    _fields_ = [
        ("diskFull", c_ulonglong),
        ("slabJournalCommitsRequested", c_ulonglong),
        ("entries", CommitStatistics),
        ("blocks", CommitStatistics),
    ]


class SlabJournalStatistics(VDOStructure):
    _fields_ = [
        ("diskFullCount", c_ulonglong),
        ("flushCount", c_ulonglong),
        ("blockedCount", c_ulonglong),
        ("blocksWritten", c_ulonglong),
        ("tailBusyCount", c_ulonglong),
    ]


class SlabSummaryStatistics(VDOStructure):
    _fields_ = [
        ("blocksWritten", c_ulonglong),
    ]


class RefCountsStatistics(VDOStructure):
    _fields_ = [
        ("blocksWritten", c_ulonglong),
    ]


class BlockMapStatistics(VDOStructure):
    _fields_ = [
        ("dirtyPages", c_uint),
        ("cleanPages", c_uint),
        ("freePages", c_uint),
        ("failedPages", c_uint),
        ("incomingPages", c_uint),
        ("outgoingPages", c_uint),
        ("cachePressure", c_uint),
        ("readCount", c_ulonglong),
        ("writeCount", c_ulonglong),
        ("failedReads", c_ulonglong),
        ("failedWrites", c_ulonglong),
        ("reclaimed", c_ulonglong),
        ("readOutgoing", c_ulonglong),
        ("foundInCache", c_ulonglong),
        ("discardRequired", c_ulonglong),
        ("waitForPage", c_ulonglong),
        ("fetchRequired", c_ulonglong),
        ("pagesLoaded", c_ulonglong),
        ("pagesSaved", c_ulonglong),
        ("flushCount", c_ulonglong),
    ]


class ErrorStatistics(VDOStructure):
    _fields_ = [
        ("invalidAdvicePBNCount", c_ulonglong),
        ("noSpaceErrorCount", c_ulonglong),
        ("readOnlyErrorCount", c_ulonglong),
    ]


class VDOStatistics(VDOStructure):
    _fields_ = [
        ("version", c_uint),
        ("releaseVersion", c_uint),
        ("_dataBlocksUsed", c_ulonglong),
        ("_overheadBlocksUsed", c_ulonglong),
        ("_logicalBlocksUsed", c_ulonglong),
        ("physicalBlocks", c_ulonglong),
        ("logicalBlocks", c_ulonglong),
        # ("oneKBlocks", c_ulonglong),
        # ("oneKBlocksUsed", c_ulonglong),
        # ("oneKBlocksAvailable", c_ulonglong),
        # ("usedPercent", c_byte),
        # ("savings", c_byte),
        # ("savingPercent", c_byte),
        ("blockMapCacheSize", c_ulonglong),
        ("writePolicy", c_char * 15),
        ("blockSize", c_ulonglong),
        ("completeRecoveries", c_ulonglong),
        ("readOnlyRecoveries", c_ulonglong),
        ("mode", c_char * 15),
        ("inRecoveryMode", c_bool),
        ("_recoveryPercentage", c_byte),
        ("packer", PackerStatistics),
        ("allocator", BlockAllocatorStatistics),
        ("journal", RecoveryJournalStatistics),
        ("slabJournal", SlabJournalStatistics),
        ("slabSummary", SlabSummaryStatistics),
        ("refCounts", RefCountsStatistics),
        ("blockMap", BlockMapStatistics),
        ("errors", ErrorStatistics),
    ]

    @property
    def dataBlocksUsed(self):
        if (not self.inRecoveryMode) and (self.mode != 'read-only'):
            return self._dataBlocksUsed
        return 0

    @property
    def overheadBlocksUsed(self):
        if not self.inRecoveryMode:
            return self._overheadBlocksUsed
        return 0

    @property
    def logicalBlocksUsed(self):
        if not self.inRecoveryMode:
            return self._logicalBlocksUsed
        return 0

    @property
    def oneKBlocks(self):
        return self.physicalBlocks * self.blockSize / 1024

    @property
    def oneKBlocksUsed(self):
        if not self.inRecoveryMode:
            return (self.dataBlocksUsed + self.overheadBlocksUsed) * self.blockSize / 1024
        return 0

    @property
    def oneKBlocksAvailable(self):
        if not self.inRecoveryMode:
            return (self.physicalBlocks - self.dataBlocksUsed - self.overheadBlocksUsed) * self.blockSize / 1024
        return 0

    @property
    def usedPercent(self):
        if (not self.inRecoveryMode) and (self.mode != 'read-only'):
            return int((100 * (self.dataBlocksUsed + self.overheadBlocksUsed) / self.physicalBlocks) + 0.5)
        return 0

    @property
    def savings(self):
        if not self.inRecoveryMode:
            return int(100 * (self.logicalBlocksUsed - self.dataBlocksUsed) / self.logicalBlocksUsed) if (self.logicalBlocksUsed > 0) else -1
        return 0

    @property
    def savingPercent(self):
        if (not self.inRecoveryMode) and (self.mode != 'read-only'):
            return self.savings if (self.savings >= 0) else "N/A"
        return "N/A"

    @property
    def recoveryPercentage(self):
        if self.inRecoveryMode:
            return self._recoveryPercentage
        return 0


def get_hump_name(text):
    """

    :param str text:
    :return:
    """
    if not text:
        return text
    text = "".join(text.title().split())
    return text[0].lower() + text[1:]


print get_hump_name("block size")
print "compressedFragmentsWritten".title()
VDO_stat = VDOStatistics()
print isinstance(VDO_stat, VDOStatistics)
print isinstance(VDO_stat, Structure)

with open("./dedupe_stats", 'rb') as f:
    f.readinto(VDO_stat)

print VDO_stat.packer
print VDO_stat.dataBlocksUsed
print VDO_stat.overheadBlocksUsed
print VDO_stat.oneKBlocks
print VDO_stat.oneKBlocksUsed
print VDO_stat.oneKBlocksAvailable
print VDO_stat.usedPercent
print VDO_stat.savings
# print VDO_stat.savingPercent
# pass

#!/usr/bin/python

#
# Copyright (c) 2018 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA. 
#

"""
  vdoStats - Report statistics from an Albireo VDO.

  $Id: //eng/vdo-releases/magnesium-rhel7.5/src/python/vdo/vdoStats#1 $
"""

from __future__ import print_function

import errno
import gettext
import locale
import os
import sys

from optparse import OptionParser

# Temporary patch to address layout changes
for dir in sys.path:
    vdoDir = os.path.join(dir, 'vdo')
    if os.path.isdir(vdoDir):
        sys.path.append(vdoDir)
        break

from statistics import *
from utils import Command, CommandError, runCommand

gettext.install('vdo')

parser = OptionParser(usage="%prog [options] [device ...]");
parser.add_option("--all", action="store_true", dest="all",
                  help=_("Equivalent to --verbose"))
parser.add_option("--human-readable", action="store_true",
                  dest="humanReadable",
                  help=_("Display stats in human-readable form"))
parser.add_option("--si", action="store_true", dest="si",
                  help=_("Use SI units, implies --human-readable"))
parser.add_option("--verbose", action="store_true", dest="verbose",
                  help=_("Include verbose statistics"))
parser.add_option("--version", action="store_true", dest="version",
                  help=_("Print the vdostats version number and exit"))

UNITS = ['B', 'K', 'M', 'G', 'T']


def makeDedupeFormatter(options):
    """
    Make the formatter for dedupe stats if needed.

    :param options:  The command line options

    :return: A formatter if needed or None
    """
    if not options.verbose:
        return None

    return StatFormatter([{'namer': '+'},
                          {'indent': '  ', 'namer': True}],
                         hierarchical=False)


def enumerateDevices():
    """
    Enumerate the list of VDO devices on this host.

    :return: A list of VDO device names
    """
    names = []
    try:
        names = [name for name in runCommand(["vdo", "list"]).splitlines()
                 if len(name) > 0]
        paths = [os.path.sep.join(["", "dev", "mapper", name]) for name in names]
        names = filter(os.path.exists, paths)
    except CommandError as e:
        print(_("Error enumerating VDO devices: {0}".format(e)), file=sys.stderr)
    return names


def getDeviceStats(devices, assays):
    """
    Get the statistics for a given device.

    :param devices:  A list of devices to sample. If empty, all VDOs will
                     be sampled.
    :param assays:   The types of samples to take for each device

    :return:  A tuple whose first entry is the Samples and whose second entry
              is the exit status to use if no subsequent error occurs.
    """
    exitStatus = 0
    if not devices:
        mustBeVDO = False
        devices = enumerateDevices()
    else:
        mustBeVDO = True
        # Filter out any specified devices that do not exist.
        #
        # Any specified device that passes os.path.exists is passed through.
        # If it fails os.path.exists and is not a full path it is checked
        # against being an entry in either /dev/mapper or /proc/vdo.
        # If either of those exists the original device is passed through
        # unchanged.
        existingPaths = []
        for device in devices:
            if os.path.exists(device):
                existingPaths.append(device)
            else:
                name = device
                exists = False
                if (not os.path.isabs(device)):
                    exists = os.path.exists(os.path.sep.join(["", "dev", "mapper",
                                                              device]))
                    if (not exists):
                        device = os.path.sep.join(["", "proc", "vdo", device])

                if ((not exists) and (not os.path.exists(device))):
                    print("'{0}': {1}".format(name, os.strerror(errno.ENOENT)),
                          file=sys.stderr)
                    exitStatus = 1
                else:
                    existingPaths.append(name)
        devices = existingPaths

    if len(devices) > 0:
        return (Samples.assayDevices(assays, devices, mustBeVDO), exitStatus)
    return (None, exitStatus)


def formatSize(size, options):
    """
    Format a size (in KB) for printing.

    :param size:    The size in bytes.
    :param options: The command line options

    :return: The size formatted for printing based on the options
    """
    if isinstance(size, NotAvailable):
        return size

    if not options.humanReadable:
        return size

    size *= 1024
    divisor = 1000.0 if options.si else 1024.0
    unit = 0
    while ((size >= divisor) and (unit < (len(UNITS) - 1))):
        size /= divisor
        unit += 1

    return "{0:>.1f}{1}".format(size, UNITS[unit])


def formatPercent(value):
    """
    Format a percentage for printing.

    :param value: The value to format

    :return: The formatted value
    """
    return value if isinstance(value, NotAvailable) else "{0}%".format(value)


def dfStats(sample, options):
    """
    Extract the values needed for df-style output from a sample.

    :param sample:  The sample from which to extract df values
    :param options: The command line options
    """
    return ([formatSize(sample.getStat(statName), options)
             for statName in
             ["oneKBlocks", "oneKBlocksUsed", "oneKBlocksAvailable"]]
            + [formatPercent(sample.getStat(statName))
               for statName in ["usedPercent", "savingPercent"]])


def printDF(stats, options):
    """
    Print stats in df-style.

    :param stats:   A list of samples, one for each device sampled
    :param options: The command line options
    """
    dfFormat = "{0:<20} {1:>9} {2:>9} {3:>9} {4:>4} {5:>13}"
    print(dfFormat.format("Device",
                          "Size" if options.humanReadable else "1K-blocks",
                          "Used", "Available", "Use%", "Space saving%"))
    for stat in stats:
        print(apply(dfFormat.format,
                    [stat.getDevice()] + dfStats(stat.getSamples()[0], options)))


def printYAML(stats, dedupeFormatter):
    """
    Print stats as (pseudo) YAML.

    :param stats:           A list of Samples, one for each device sampled
    :param dedupeFormatter: The formatter for dedupe stats (may be None)
    """
    for stat in stats:
        samples = stat.getSamples()
        if dedupeFormatter:
            dedupeFormatter.output(LabeledValue.make(stat.getDevice(),
                                                     [s.labeled() for s in samples]))


def main():
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        pass

    (options, devices) = parser.parse_args()
    if options.version:
        print("{0}.{1}".format(CURRENT_RELEASE_VERSION_NUMBER,
                               VDOStatistics.statisticsVersion))
        sys.exit(0)

    if options.all:
        options.verbose = True
    if options.si:
        options.humanReadable = True

    dedupeFormatter = makeDedupeFormatter(options)

    if options.verbose:
        statsTypes = [VDOStatistics(), KernelStatistics()]
    else:
        statsTypes = [VDOStatistics()]

    exitStatus = 0
    try:
        (stats, exitStatus) = getDeviceStats(devices, statsTypes)
        if not stats:
            return exitStatus
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    if options.verbose:
        printYAML(stats, dedupeFormatter)
    else:
        printDF(stats, options)

    return exitStatus


if __name__ == "__main__":
    sys.exit(main())

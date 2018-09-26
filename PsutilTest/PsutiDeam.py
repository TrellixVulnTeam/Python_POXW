"""
@author: Alfons
@contact: alfons_xh@163.com
@file: PsutiDeam.py
@time: 18-9-18 上午11:16
@version: v1.0 
"""
import psutil
import pynvml


class DeviceManager:
    MB = 1024 * 1024
    GB = MB * 1024

    def __init__(self):
        try:
            pynvml.nvmlInit()
            self.__gpuHandleList = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(pynvml.nvmlDeviceGetCount())]
        except:
            self.__gpuHandleList = list()

    def CpuInfo(self):
        """
        获取cpu使用情况
        :return: cpu使用情况
        """
        cpuFreqList = psutil.cpu_percent(interval=1, percpu=True)
        cpuTempList = psutil.sensors_temperatures().get("coretemp")[1:]
        cpuIndexList = range(len(cpuFreqList))

        cpuInfoList = list()
        for cpuIndex, cpuFreq, cpuTemp in zip(cpuIndexList, cpuFreqList, cpuTempList):
            cpuInfoList.append(dict(Index=cpuIndex, Percent=cpuFreq, Temp=cpuTemp.current))

        return cpuInfoList

    def GpuInfo(self):
        """
        获取GPU使用情况
        :return: GPU使用情况
        """
        gpuInfoList = list()
        for gpuIndex, gpuHandle in enumerate(self.__gpuHandleList):
            gpuPercent = pynvml.nvmlDeviceGetUtilizationRates(gpuHandle).gpu
            memTotal = format(pynvml.nvmlDeviceGetMemoryInfo(gpuHandle).total / self.MB, ".2f")
            memUsed = format(pynvml.nvmlDeviceGetMemoryInfo(gpuHandle).used / self.MB, ".2f")
            temp = pynvml.nvmlDeviceGetTemperature(gpuHandle, pynvml.NVML_TEMPERATURE_GPU)
            gpuInfoList.append(dict(Index=gpuIndex, Percent=gpuPercent, TotalMem=memTotal, UsedMem=memUsed, Temp=temp))
        return gpuInfoList

    def MemoryInfo(self):
        """
        获取系统内存使用情况
        :return: 内存使用情况
        """
        memInfo = psutil.virtual_memory()
        memTotal = format(memInfo.total / self.MB, ".2f")
        memUsed = format(memInfo.used / self.MB, ".2f")

        return dict(Total=memTotal, Used=memUsed)

    def DiskInfo(self):
        """
        获取系统磁盘使用情况
        :return: 磁盘使用情况
        """
        diskInfo = psutil.disk_usage("/")
        diskTotal = format(diskInfo.total / self.GB, ".2f")
        diskUsed = format(diskInfo.used / self.GB, ".2f")

        return dict(Total=diskTotal, Used=diskUsed)

    def GetDeviceInfo(self):
        """
        获取硬件设备信息
        :return: 成功返回硬件设备信息，失败返回None
        """
        try:
            return dict(CPU=self.CpuInfo(), GPU=self.GpuInfo(), Mem=self.MemoryInfo(), Disk=self.DiskInfo())
        except:
            return None


device = DeviceManager()
deviceInfo = device.GetDeviceInfo()

pass

import os, sys
import time
import wmi


def get_disk_info():
    """
     获取物理磁盘信息。 
     """
    tmp_list = []
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        tmp_dict = {"Caption": physical_disk.Caption, "Size": int(physical_disk.Size) / 1024 / 1024 / 1024}
        tmp_list.append(tmp_dict)
    return tmp_list


def get_fs_info():
    """
     获取文件系统信息。 
     包含分区的大小、已用量、可用量、使用率、挂载点信息。 
     """
    tmp_list = []
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                tmp_dict = {"Caption": logical_disk.Caption, "DiskTotal": int(logical_disk.Size) / 1024 / 1024 / 1024,
                            "UseSpace": (int(logical_disk.Size) - int(logical_disk.FreeSpace)) / 1024 / 1024 / 1024,
                            "FreeSpace": int(logical_disk.FreeSpace) / 1024 / 1024 / 1024, "Percent": int(
                        100.0 * (int(logical_disk.Size) - int(logical_disk.FreeSpace)) / int(logical_disk.Size))}
                tmp_list.append(tmp_dict)
    return tmp_list


if __name__ == "__main__":
    disk = get_disk_info()
    print(disk)
    print('--------------------------------------')
    fs = get_fs_info()
    print(fs)

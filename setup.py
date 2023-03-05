#!/usr/bin/env python3
#
# Copyright (C) 2023 xinrui <zhuzhouxinrui@163.com>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import zipfile
import re
import os
import shutil
import progressbar

def unzip(file_name):
    """解压缩zip接口

    :param file_name: 指定zip文件名称
    :type file_name: str

    :return: 解压缩后的文件夹名称
    :return type: str

    """

    zip_file = zipfile.ZipFile(file_name)
    unzip_directory = re.search(r'[^/]+(?=\.zip)', file_name).group(0)
    if os.path.isdir(unzip_directory):
        pass
    else:
        os.mkdir(unzip_directory)
    for names in zip_file.namelist():
        zip_file.extract(names, unzip_directory + "/")
    zip_file.close()
    return unzip_directory

def setup_alist_rclone():
    """安装alist和rclone"""

    # 初始化进度条
    bar = progressbar.ProgressBar(max_value=100)
    bar.update(1)

    # 使用默认安装包
    alist_zip_file_name = "alist-windows-amd64.zip"
    bar.update(10)
    rclone_zip_file_name = "rclone-v1.61.1-windows-amd64.zip"
    bar.update(20)
    WinFsp_file_name = "winfsp-1.12.22339.msi"
    bar.update(30)

    # 解压缩到指定文件夹
    if os.path.isdir("alist_component"):
        pass
    else:
        os.mkdir("alist_component")
    if os.path.isdir("rclone_component"):
        pass
    else:
        os.mkdir("rclone_component")
    if alist_zip_file_name not in ["null", "error"]:
        alist_unzip_directory = unzip("download_package/" + alist_zip_file_name)
        shutil.copy(alist_unzip_directory + "/alist.exe", "alist_component")
    bar.update(40)
    if rclone_zip_file_name not in ["null", "error"]:
        rclone_unzip_directory = unzip("download_package/" + rclone_zip_file_name)
        directory_list = os.listdir(os.path.join(rclone_unzip_directory, rclone_unzip_directory))
        for files in directory_list:
            file_path = os.path.join(rclone_unzip_directory, rclone_unzip_directory, files)
            shutil.copy(file_path, "rclone_component")
    bar.update(50)

    # 安装WinFsp
    os.system(f'cd download_package && {WinFsp_file_name}')
    bar.update(60)

    # 删除中间过程文件
    shutil.rmtree(alist_unzip_directory)
    shutil.rmtree(rclone_unzip_directory)
    bar.update(70)

    # 初始化alist
    if os.path.isdir("alist_component/data"):
        pass
    else:
        os.mkdir("alist_component/data")
        alist_config_data_list = os.listdir("alist_config/data")
        for files in alist_config_data_list:
            file_path = os.path.join("alist_config/data", files)
            shutil.copy(file_path, "alist_component/data")
        alist_config_VBS_list = os.listdir("alist_config/VBS")
        for files in alist_config_VBS_list:
            file_path = os.path.join("alist_config/VBS", files)
            shutil.copy(file_path, "alist_component")
    bar.update(80)

    # 初始化rclone
    if os.path.isdir(os.environ["APPDATA"] + "/rclone"):
        pass
    else:
        os.mkdir(os.environ["APPDATA"] + "/rclone")
        rclone_config_list = os.listdir("rclone_config/config")
        for files in rclone_config_list:
            file_path = os.path.join("rclone_config/config", files)
            shutil.copy(file_path, os.environ["APPDATA"] + "/rclone")
        rclone_config_VBS_list = os.listdir("rclone_config/VBS")
        for files in rclone_config_VBS_list:
            file_path = os.path.join("rclone_config/VBS", files)
            shutil.copy(file_path, "rclone_component")
    shutil.copy("rclone_config/VBS/rclone_start.VBS", "rclone_component")
    if os.path.isdir("TempCache"):
        pass
    else:
        os.mkdir("TempCache")
    bar.update(90)

    # 设置系统环境变量
    current_directory = os.popen("chdir").read().split("\n")
    os.system(f'setx ALIST_RCLONE_ROOT {current_directory[0]}')
    bar.update(100)


if __name__ == '__main__':

    # 安装alist和rclone
    setup_alist_rclone()

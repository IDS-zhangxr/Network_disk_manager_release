#!/usr/bin/env python3
#
# Copyright (C) 2023 xinrui <zhuzhouxinrui@163.com>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import requests
import zipfile
import os
import re
import shutil
import progressbar
from requests.adapters import HTTPAdapter

def get_github_release_file(owner, repository, release_file_name):
    """下载GitHub指定仓库最新发布版本文件接口

    :param owner: 指定仓库的所有者
    :type owner: str

    :param repository: 指定仓库的名称
    :type repository: str

    :param release_file_name: 发布版本压缩包文件名，可以是全名也可以是部分字段匹配
    :type release_file_name: str

    :return: 下载的压缩包文件名，如果GitHub仓库Release中没有包含发布版本压缩包文件名的文件则返回“null”，如果是网络问题则返回“error”
    :return type: str

    """

    request_session = requests.Session()
    request_session.mount('https://', HTTPAdapter(max_retries=20))
    if os.path.isdir("download_package"):
        pass
    else:
        os.mkdir("download_package")
    try:
        latest_version_info = request_session.get("https://api.github.com/repos/" + owner + "/" + repository + "/releases/latest")
        for item in latest_version_info.json()["assets"]:
            if release_file_name in item["name"]:
                download_url = "https://github.com/" + owner + "/" + repository + "/releases/download/" + latest_version_info.json()["tag_name"] + "/" + item["name"]
                download_file = request_session.get(download_url)
                open("./download_package/" + item["name"], "wb").write(download_file.content)
                return "./download_package/" + item["name"]
        return "null"
    except requests.exceptions.RequestException as e:
        print(e)
        return "error"

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

def update_alist_rclone():
    """更新alist和rclone"""

    # 初始化进度条
    bar = progressbar.ProgressBar(max_value=100)
    bar.update(1)

    # 下载GitHub上的最新版本
    alist_zip_file_name = get_github_release_file("alist-org", "alist", "windows-amd64.zip")
    bar.update(10)
    rclone_zip_file_name = get_github_release_file("rclone", "rclone", "windows-amd64.zip")
    bar.update(20)
    WinFsp_file_name = get_github_release_file("winfsp", "winfsp", ".msi")
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
        alist_unzip_directory = unzip(alist_zip_file_name)
        shutil.copy(alist_unzip_directory + "/alist.exe", "alist_component")
    bar.update(40)
    if rclone_zip_file_name not in ["null", "error"]:
        rclone_unzip_directory = unzip(rclone_zip_file_name)
        directory_list = os.listdir(os.path.join(rclone_unzip_directory, rclone_unzip_directory))
        for files in directory_list:
            file_path = os.path.join(rclone_unzip_directory, rclone_unzip_directory, files)
            shutil.copy(file_path, "rclone_component")
    bar.update(50)

    # 安装WinFsp
    os.system(WinFsp_file_name.replace("/", "\\"))
    bar.update(60)

    # 删除中间过程文件
    if alist_zip_file_name not in ["null", "error"]:
        shutil.rmtree(alist_unzip_directory)
    if rclone_zip_file_name not in ["null", "error"]:
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

    # 更新alist和rclone
    update_alist_rclone()

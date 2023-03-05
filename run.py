#!/usr/bin/env python3
#
# Copyright (C) 2023 xinrui <zhuzhouxinrui@163.com>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import os
import time

def kill_exe(exe_name):
    """关闭exe进程

    :param exe_name: 指定exe进程名称
    :type exe_name: str

    """

    # 调用系统命令关闭进程
    os.system('taskkill /f /t /im ' + exe_name)

def stop_alist_rclone():
    """关闭alist和rclone"""

    # 关闭rclone
    kill_exe('rclone.exe')

    # 等待1s
    time.sleep(1)

    # 关闭alist
    kill_exe('alist.exe')

def run_alist_rclone():
    """运行alist和rclone"""

    # 关闭alist和rclone
    stop_alist_rclone()

    # 运行alist
    os.system("cd alist_component && alist_start.VBS")

    # 等待2s
    time.sleep(2)

    # 运行rclone
    os.system("cd rclone_component && rclone_start.VBS")


if __name__ == '__main__':

    # 运行alist和rclone
    run_alist_rclone()

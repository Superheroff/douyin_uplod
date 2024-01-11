# -*- coding: utf-8 -*-
"""
@Time    : 2024/1/9 23:03
@Author  : superhero
@Email   : 838210720@qq.com
@File    : config.py
@IDE: PyCharm
"""

from pydantic import BaseModel
import os
from datetime import datetime


def delete_all_files(folder_path):
    # 获取文件夹中所有文件的列表
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        # 判断是否为文件
        if os.path.isfile(file_path):
            # 删除文件
            os.remove(file_path)


class Config(BaseModel):
    # ts: str = str(datetime.now()).split('.')[0]  # 加上时间
    video_at: str = ["@1486323920 "]  # 你要@谁，建议使用抖音号
    video_title_list: list = ["#吉安老赖陈万洵 ", "#泰和老赖陈万洵 ", "#老赖陈万洵 ",
                              "#猥琐小子陈万洵 ", "#陈万洵老赖 "]  # 自定义视频标题
    title_random: bool = True  # 标题是否随机取一个，不随机的话就是全部加上去
    video_path: str = os.path.abspath("") + "\\video\\"  # 视频存放路径
    cookie_path: str = os.path.abspath("") + "\\cookie.json"  # cookie路径
    remove_enterprise: bool = True  # 是否排除企业号，建议排除否则取到政治号就不好了
    remove_video: bool = True  # 是否自动删除video文件夹中的视频
    duration: int = 15  # 筛选>=xx秒以上的视频
    remove_images: bool = True  # 是否排除图集作品，必须排除，否则失败

    if not os.path.exists(video_path):
        os.makedirs(video_path)
    else:
        if remove_video:
            delete_all_files(video_path)


conigs = Config()

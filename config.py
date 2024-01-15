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
    day: int = datetime.now().day
    video_at: list = ["@庐陵老街陈万洵 "]  # 你要@的人的昵称，默认是必须@作者的
    video_at2: list = ["1486323920"]  # 你要@的人的抖音号
    # 单双日不同的话题
    today: bool = True
    video_title_list: list = []

    video_title_list1: list = ["#吉安老赖陈万洵 ", "#泰和老赖陈万洵 ", "#老赖陈万洵 ",
                              "#陈万洵破产 ", "#庐陵人文谷老赖陈万洵 ", "#庐陵老街倒闭 "]  # 单号取这个自定义视频标题

    video_title_list2: list = ["庐陵老街=庐陵人文谷≠后河梦回庐陵，庐陵老街=老赖，请勿上当受骗，游玩去后河", "#庐陵老街 ", "#庐陵人文谷 ", "#后河梦回庐陵景区 "]  # 双号取这个自定义视频标题

    title_random: bool = True  # 标题是否随机取一个，不随机的话就是全部加上去
    if today:
        # video_title_list = video_title_list2 if day % 2 == 0 else video_title_list1
        if day % 2 != 0:
            title_random = False
            video_title_list = video_title_list2
        else:
            video_title_list = video_title_list1
    else:
        video_title_list = video_title_list1

    if not title_random:
        if len(video_title_list) > 5:
            print("错误，话题数不能大于5")

    video_path: str = os.path.abspath("") + "\\video\\"  # 视频存放路径
    cookie_path: str = os.path.abspath("") + "\\cookie.json"  # cookie路径
    remove_enterprise: bool = True  # 是否排除企业号，建议排除否则取到政治号就不好了
    remove_custom_verify: bool = True  # 排除普通认证号
    remove_video: bool = True  # 是否自动删除video文件夹中的视频
    duration: int = 15  # 筛选>=xx秒以上的视频
    remove_images: bool = True  # 是否排除图集作品，必须排除，否则失败
    city_list: list = ["庐陵老街", "庐陵人文谷", "澄江广场"]  # 添加位置信息，从中随机，固定的话输入一个就行

    if not os.path.exists(video_path):
        os.makedirs(video_path)
    else:
        if remove_video:
            delete_all_files(video_path)


conigs = Config()

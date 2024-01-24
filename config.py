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


class Config(BaseModel):
    day: int = datetime.now().day
    video_at: list = ["@庐陵老街陈万洵 "]  # 你要@的人的昵称，默认是必须@作者的
    video_at2: list = ["1486323920"]  # 你要@的人的抖音号
    # 单双日不同的话题
    today: bool = True
    video_title_list: list = []

    video_title_list1: list = ["#吉安老赖陈万洵 ", "#泰和老赖陈万洵 ", "#老赖陈万洵 ",
                              "#江西老赖陈万洵 ", "#庐陵人文谷老赖陈万洵 ", "#庐陵老街倒闭 ", "#庐陵老街荒芜一人 "]  # 单号取这个自定义视频标题

    video_title_list2: list = ["江西吉安庐陵老街是#老赖陈万洵 ，吉安游玩请去后河梦回庐陵景区，能仁巷等", "#庐陵老街荒芜一人 ", "#庐陵人文谷荒芜一人 ", "#后河梦回庐陵景区 ", "#能仁巷 "]  # 双号取这个自定义视频标题

    title_random: bool = True  # 标题是否随机取一个，不随机的话就是全部加上去

    video_path: str = os.path.abspath("") + "\\video\\"  # 视频存放路径
    cookie_path: str = os.path.abspath("") + "\\cookie.json"  # cookie路径
    remove_enterprise: bool = True  # 是否排除企业号，建议排除否则取到政治号就不好了
    remove_custom_verify: bool = True  # 排除普通认证号
    remove_video: bool = True  # 是否自动删除video文件夹中的视频
    duration: int = 15  # 筛选>=xx秒以上的视频
    remove_images: bool = True  # 是否排除图集作品，必须排除，否则失败
    city_list: list = ["庐陵老街", "庐陵人文谷", "澄江广场"]  # 添加位置信息，从中随机，固定的话输入一个就行




conigs = Config()

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

class Config(BaseModel):
    # 获取cookie可以从get_cookie.py获取，并不一定从此接口获取
    apikey: str = "d9ba8ae07d955b83c3b04280f3dc5a4a"

    video_at: list = ["1486323920"]  # 你要@的人的抖音号，默认是必须@作者的，
    # 2.4以上版本无需提供昵称，将通过抖音号自动获取

    start_frame: int = 90  # 起始帧
    end_frame: int = 30  # 结尾去除多少帧

    # 单双日不同的话题
    today: bool = True

    video_title_list1: list = ["#标题1 ", "#标题2 "]  # 单号取这个自定义视频标题

    video_title_list2: list = ["标题1", "标题2"]  # 双号取这个自定义视频标题

    title_random: bool = True  # 标题是否随机取一个，不随机的话就是全部加上去

    _path: str = os.path.abspath("")

    video_path: str = os.path.join(_path, "video")  # 视频存放路径
    cookie_path: str = os.path.join(_path, "cookie.json")  # cookie路径
    remove_enterprise: bool = True  # 是否排除企业号，建议排除否则取到政治号就不好了
    remove_custom_verify: bool = True  # 排除普通认证号
    remove_video: bool = True  # 是否自动删除video文件夹中的视频
    duration: int = 10  # 筛选>=xx秒的视频
    remove_images: bool = True  # 是否排除图集作品，必须排除，否则失败
    city: bool = False  # 是否添加位置
    city_list: list = ["后河梦回庐陵", "能仁巷", "澄江广场"]  # 添加位置信息，从中随机，固定的话输入一个就行

    declaration: bool = True  # 是否添加声明
    declaration_int: int = 1  # 添加什么声明序号，1-6
    declaration_list: list = ["内容自行拍摄", "内容取材网络", "内容由AI生成", "可能引人不适", "虚构演绎，仅供娱乐", "危险行为，请勿模仿"]
    declaration_value: list = ["中国-安徽-安庆", None]  # 如果设置内容自行拍摄，则必须设置此项，list[0]=拍摄地，list[1]=拍摄日期，默认当天

conigs = Config()

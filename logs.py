# -*- coding: utf-8 -*-
"""
@Time    : 2024/1/9 16:20
@Author  : superhero
@Email   : 838210720@qq.com
@File    : logs.py
@IDE: PyCharm
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os


def config_log(is_debug=False, when="D"):
    """
    日志方法
    :param is_debug: 级别
    :param when: 按照规则切分
    """
    file_path = os.path.abspath("") + r"\\logs.log"
    if is_debug:
        fmt = '[%(asctime)s]-%(filename)s-%(lineno)d-%(threadName)s-%(message)s'
    else:
        fmt = '[%(asctime)s]-%(filename)s-%(lineno)d-%(threadName)s-%(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler(file_path, when, 1, 3, encoding="utf-8")
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.INFO, format=fmt)
    log.addHandler(fileTimeHandler)
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)
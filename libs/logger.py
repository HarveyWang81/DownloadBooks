#!/bin/env python3
# coding:utf-8

"""
# Author:   Harvey.Wang
# Data:     
# Desc:     
"""

import logging, os
from logging import handlers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(module)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        # %(name)s Logger的名字
        # %(levelno)s 数字形式的日志级别
        # %(levelname)s 文本形式的日志级别
        # %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
        # %(filename)s 调用日志输出函数的模块的文件名
        # %(module)s 调用日志输出函数的模块名
        # %(funcName)s 调用日志输出函数的函数名
        # %(lineno)d 调用日志输出函数的语句所在的代码行
        # %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
        # %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
        # %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
        # %(thread)d 线程ID。可能没有
        # %(threadName)s 线程名。可能没有
        # %(process)d 进程ID。可能没有
        # %(message)s 用户输出的消息
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
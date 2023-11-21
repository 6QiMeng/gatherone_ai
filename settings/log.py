# -*- coding: utf-8 -*-
import sys
import time
from loguru import logger
import os


def creat_time_os():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    log_path_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    logs_path = os.path.join(log_path_dir, "logs")
    if os.path.exists(logs_path):
        return logs_path
    else:
        os.makedirs(logs_path)
        return logs_path


class Loguru_logger:
    logger.remove()  # 这里是不让他重复打印

    # 输出日志格式
    def __init__(self):
        creat_time = time.strftime("%Y-%m-%d", time.localtime())

        logger.remove(handler_id=None)  # 这里是不让他重复打印
        # logger.add(sys.stderr,  # 这里是不让他重复打印
        #            level="INFO"
        #            )
        # 输出到文件，并按天分割和压缩
        logs_path = creat_time_os()
        # 日志文件名：由用例脚本的名称，结合日志保存路径，得到日志文件的绝对路径
        logname = os.path.join(logs_path, creat_time + '.log')
        logger.add(
            logname,
            encoding="utf-8",
            level="INFO",
            rotation="500MB",
            retention="5 days",
            # colorize=True,
            compression="zip")
        self.creat_time = time.strftime("%Y-%m-%d", time.localtime())
        self.log = logger

    def check_format(self):
        if time.strftime("%Y-%m-%d", time.localtime()) != self.creat_time:
            self.__init__()


def log_info(*args):
    my_logger = Loguru_logger()
    my_logger.check_format()
    my_logger.log.info(args[0] if len(args) == 1 else args)


def log_debug(*args):
    my_logger = Loguru_logger()
    my_logger.check_format()
    my_logger.log.debug(args[0] if len(args) == 1 else args)


def log_error(*args):
    my_logger = Loguru_logger()
    my_logger.check_format()
    my_logger.log.error(args[0] if len(args) == 1 else args)

"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : Test_logger.py
 @Time    : 2019/5/7 16:41
"""
import os
import logging


def Init(level, filename, console):
    """
    日志初始化函数
    :param level: 日志等级
    :param filename: 日志输出文件名
    :param console: 是否在控制台输出
    :return:
    """
    logger = logging.getLogger()

    # 设置等级
    # 可以为数字： FATAL = 50, ERROR = 40, WARN = WARNING = 30, INFO = 20, DEBUG = 10, NOTSET = 0
    # 也可以为字符：'CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET',
    logger.setLevel(level.upper() if str(level) == level else level)

    # 日志格式
    BASIC_FORMAT = '%(asctime)s [%(name)s] %(filename)s[%(lineno)d] [%(levelname)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

    # 设置文件日志
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file_handler = logging.FileHandler(filename)  # 输出到文件的handler
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 设置控制台输出日志
    if console:
        console_handler = logging.StreamHandler()  # 输出到控制台的handler
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


if __name__ == '__main__':
    Init(logging.DEBUG, "/logger.log", True)
    # Init(logging.DEBUG, "/tmp/logger.log", False)

    logging.info('this is info')
    logging.debug('this is debug')

    import unit
    pass
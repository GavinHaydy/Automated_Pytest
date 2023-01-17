# coding=utf-8
import logging
import datetime
import os


class AutoTestLog:

    def __init__(self, level):
        level_dict = {'debug':logging.DEBUG,
                      'info':logging.INFO,
                      'warning':logging.WARNING,
                      'error':logging.ERROR}
        self.logger = logging.getLogger()  # 创建一个logger
        self.logger.setLevel(level_dict[level])  # 指定日志级别

        # 以时间命名log文件名
        base_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件路径
        log_path = base_path + '/../logs/'  # log文件路径
        file_name = datetime.datetime.now().strftime("%y-%m-%d-%H-%M") + '.log'  # 以时间命名文件名
        log_name = log_path + file_name  # log文件名

        # 将日志写入磁盘
        self.file_handle = logging.FileHandler(log_name, 'a', encoding='utf-8')
        self.file_handle.setLevel(level_dict[level])
        """
        设置日志格式
            %(asctime)s         日志事件发生的时间
            %(filename)s        pathname的文件名部分，包含文件后缀
            %(funcName)s        调用日志记录函数的函数名
            %(levelname)s       该日志记录的文字形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）
            %(message)s         日志记录的文本内容
        """
        file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        self.file_handle.setFormatter(file_formatter)
        # 给logger添加handler
        self.logger.addHandler(self.file_handle)

    def get_log(self):
        return self.logger

    def level(self, level):
        match str(level).lower():
            case 'debug':
                return logging.DEBUG
            case 'info':
                return logging.INFO
            case 'warning':
                return logging.WARNING
            case 'error':
                return logging.ERROR
    # 关闭handle
    def close_handle(self):
        self.logger.removeHandler(self.file_handle)
        self.file_handle.close()

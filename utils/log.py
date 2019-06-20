# encoding: utf8

import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

log_dir4_posixos = "/tmp/"
log_dir4_windows = "C:\\windows\\"
log_name = "all.log"
err_log_name = "err.log"


def init_logger(logger_name, log_level=logging.DEBUG):
    global log_dir4_posixos
    global log_dir4_windows
    global log_name
    global err_log_name
    if logger_name not in Logger.manager.loggerDict:
        universal_logger = logging.getLogger(logger_name)
        universal_logger.setLevel(log_level)  # 设置全局日志级别
        df = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
        formatter = logging.Formatter(format_str, df)
        # handler all
        try:
            full_log_handler = TimedRotatingFileHandler(log_dir4_posixos + log_name, when='D', interval=1, backupCount=7)
        except Exception:
            full_log_handler = TimedRotatingFileHandler(log_dir4_windows + log_name, when='D', interval=1, backupCount=7)
        except PermissionError:
            print()
        full_log_handler.setFormatter(formatter)
        full_log_handler.setLevel(log_level)
        universal_logger.addHandler(full_log_handler)
        try:
            error_log_handler = TimedRotatingFileHandler(log_dir4_posixos + err_log_name, when='D', interval=1, backupCount=7)
        except PermissionError:
            print("Access denied, create log file failed")
        except Exception:
            error_log_handler = TimedRotatingFileHandler(log_dir4_windows + err_log_name, when='D', interval=1, backupCount=7)
        error_log_handler.setFormatter(formatter)
        error_log_handler.setLevel(logging.ERROR)
        universal_logger.addHandler(error_log_handler)

        # console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # 设置日志打印格式
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        universal_logger.addHandler(console)
    universal_logger = logging.getLogger(logger_name)
    return universal_logger


logger = init_logger("universal logger")

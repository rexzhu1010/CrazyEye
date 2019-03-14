# rex.zhu
import logging.handlers

def LogHandler(log_file):
        LOG_FILE = log_file
        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)  # 实例化formatter
        handler.setFormatter(formatter)  # 为handler添加formatter
        logger = logging.getLogger('tst')  # 获取名为tst的logger
        logger.addHandler(handler)  # 为logger添加handler
        logger.setLevel(logging.DEBUG)

        return logger




# logger = LogHandler("tst.log")
#
# logger.info("我又来测试了")

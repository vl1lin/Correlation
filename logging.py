import logging
import sys


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


log = setup_logger('CorrelationApp', "app.log")

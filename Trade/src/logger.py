import logging
from logging.handlers import RotatingFileHandler


def init_log():

    _logger = logging.getLogger()

    _logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

    file_handler = RotatingFileHandler("../logfile.log", maxBytes=1024 * 1024 * 1, backupCount=10)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    _logger.addHandler(stream_handler)
    _logger.addHandler(file_handler)

    return _logger

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from configs.config import LOGS_FOLDER


def register_logger(app):
    api_logs_folder = os.path.join(LOGS_FOLDER, "api")
    if not os.path.exists(api_logs_folder):
        os.mkdir(api_logs_folder)

    logger = app.logger
    log_file_path = os.path.join(api_logs_folder, "api.log")

    stream_handler = logging.StreamHandler(sys.stdout)
    rotating_file_handler = TimedRotatingFileHandler(log_file_path)
    formatter = logging.Formatter(
        "[%(asctime)-15s] - [%(levelname)s - %(filename)s - %(threadName)s] %(message)s")

    for handler in [rotating_file_handler]:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)

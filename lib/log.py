import logging


def log_info(message):
    logging.info(f"{'-' * 50}")
    logging.info(f"{message}")
    logging.info(f"{'-' * 50}")

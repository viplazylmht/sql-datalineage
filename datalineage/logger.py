import sys
import logging


def setup_logger(logger_name, log_level=logging.INFO):
    stream_formatter = logging.Formatter(
        fmt="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    )

    log_stream_handler = logging.StreamHandler(sys.stdout)
    log_stream_handler.setFormatter(stream_formatter)
    log_stream_handler.setLevel(log_level)

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.addHandler(log_stream_handler)

    return logger

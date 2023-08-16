import logging


def configure_logging(verbose: bool):
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = "%(levelname)s: [%(filename)s:%(funcName)s] %(message)s"
    logging.basicConfig(format=log_format, level=log_level)


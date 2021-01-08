import logging


# References:
# - https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout


def log_info(message):
    logging.info(message)


def set_log_info():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )


def log_warning(message):
    logging.warning(message)


def set_log_warning():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )


set_log_info()

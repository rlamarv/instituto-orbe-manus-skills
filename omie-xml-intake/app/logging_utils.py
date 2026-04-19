import logging
import os


def get_logger(name: str) -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def log_status(logger: logging.Logger, level: str, message: str) -> None:
    method = {
        "ok": logger.info,
        "warn": logger.warning,
        "err": logger.error,
    }.get(level, logger.info)
    method(message)


def log_section(logger: logging.Logger, title: str) -> None:
    logger.info("=" * 16 + " %s " + "=" * 16, title)

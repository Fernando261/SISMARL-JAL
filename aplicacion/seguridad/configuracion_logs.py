import logging
from logging.handlers import RotatingFileHandler
import os

def obtener_logger():
    logger = logging.getLogger("SISMARL")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    os.makedirs("aplicacion/registros", exist_ok=True)

    handler = RotatingFileHandler(
        "aplicacion/registros/sismarl.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
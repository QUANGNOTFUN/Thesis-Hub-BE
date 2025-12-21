from logging.config import dictConfig


def setup_logging(level: str = "INFO") -> None:
    """
    Call this early (e.g. in FastAPI startup) to configure structured console logs.
    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": level,
                }
            },
            "root": {"level": level, "handlers": ["console"]},
        }
    )

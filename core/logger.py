"""
Project Eagle
core/logger.py

统一日志模块

Features
--------
- Console Logger
- File Logger
- Rotating Log File
- Colored Console(optional)
- Singleton Logger
"""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from .config import RuntimeConfig


_DEFAULT_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

_DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"


class LoggerManager:
    """
    Create project logger.

    Example
    -------
    logger = LoggerManager(config).get_logger(__name__)
    """

    def __init__(
        self,
        config: RuntimeConfig,
        level: int = logging.INFO,
    ) -> None:

        self.config = config
        self.level = level

        self.log_dir = Path(config.log_dir)

        self.log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_file = self.log_dir / "project_eagle.log"

        self._configured = False

    def configure(self) -> None:

        if self._configured:
            return

        root = logging.getLogger()

        root.setLevel(self.level)

        formatter = logging.Formatter(
            fmt=_DEFAULT_FORMAT,
            datefmt=_DEFAULT_DATEFMT,
        )

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        console.setLevel(self.level)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=self.log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        file_handler.setLevel(self.level)

        root.handlers.clear()

        root.addHandler(console)

        root.addHandler(file_handler)

        self._configured = True

    def get_logger(
        self,
        name: Optional[str] = None,
    ) -> logging.Logger:

        if not self._configured:
            self.configure()

        return logging.getLogger(name)


_logger_manager: Optional[LoggerManager] = None


def initialize_logger(
    config: RuntimeConfig,
    level: int = logging.INFO,
) -> LoggerManager:
    """
    Initialize singleton logger manager.
    """

    global _logger_manager

    if _logger_manager is None:

        _logger_manager = LoggerManager(
            config=config,
            level=level,
        )

        _logger_manager.configure()

    return _logger_manager


def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Get logger.

    initialize_logger()
    must be called first.
    """

    if _logger_manager is None:

        raise RuntimeError(
            "Logger has not been initialized."
        )

    return _logger_manager.get_logger(name)

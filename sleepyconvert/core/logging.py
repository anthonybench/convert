"""Shared logging configuration for the sleepyconvert CLI."""

from __future__ import annotations

import logging


def setupLogging(log_level: str) -> None:
    """Configure application logging once for the current process.

    Parameters:
        log_level: The logging level name to apply to the root logger.

    Returns:
        None.
    """

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )


def getLogger(name: str) -> logging.Logger:
    """Return a logger instance for the provided module name.

    Parameters:
        name: The logger name.

    Returns:
        A configured logger instance.
    """

    return logging.getLogger(name)

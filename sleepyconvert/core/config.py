"""Application configuration for supported conversions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from sleepyconvert.core.sleepy_params import loadSleepyParams, requireParam


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the sleepyconvert CLI.

    Parameters:
        supported_extensions: Mapping of category names to supported file extensions.
        log_level: The configured logging level name.
        output_archive_dir: Optional directory to receive a dated copy of every
            conversion output. ``None`` disables archiving.
    """

    supported_extensions: dict[str, tuple[str, ...]]
    log_level: str
    output_archive_dir: Path | None = None

    def getCategoryForExtension(self, extension: str) -> str | None:
        """Return the category associated with a supported extension.

        Parameters:
            extension: The lowercase file extension without a leading dot.

        Returns:
            The category name when supported, otherwise ``None``.
        """

        for category_name, extensions in self.supported_extensions.items():
            if extension in extensions:
                return category_name
        return None


def loadAppConfig() -> AppConfig:
    """Load application configuration from defaults, environment, and shared params.

    The optional output archive directory is sourced from the shared sleepy
    config at ``~/sleepyconfig/params.yml`` (created with defaults on first run).

    Parameters:
        None.

    Returns:
        The populated application configuration.
    """

    supported_extensions = {
        "data": ("csv", "parquet", "json", "pkl", "xlsx"),
        "img": ("png", "jpg", "jpeg"),
        "doc": ("html", "pdf", "md"),
    }
    log_level = os.getenv("CONVERT_LOG_LEVEL", "INFO").upper()

    params = loadSleepyParams()
    raw_archive_dir = requireParam(params, "convert_output_archive_dir")
    output_archive_dir = Path(raw_archive_dir).expanduser() if raw_archive_dir else None

    return AppConfig(
        supported_extensions=supported_extensions,
        log_level=log_level,
        output_archive_dir=output_archive_dir,
    )

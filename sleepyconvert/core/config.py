"""Application configuration for supported conversions."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the sleepyconvert CLI.

    Parameters:
        supported_extensions: Mapping of category names to supported file extensions.
        log_level: The configured logging level name.
    """

    supported_extensions: dict[str, tuple[str, ...]]
    log_level: str

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
    """Load application configuration from defaults and environment variables.

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
    return AppConfig(supported_extensions=supported_extensions, log_level=log_level)

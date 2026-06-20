"""Tests for application configuration."""

from __future__ import annotations

from sleepyconvert.core.config import loadAppConfig


def testLoadAppConfigIncludesSupportedCategories() -> None:
    """Verify the default config exposes the expected categories.

    Parameters:
        None.

    Returns:
        None.
    """

    config = loadAppConfig()

    assert config.getCategoryForExtension("csv") == "data"
    assert config.getCategoryForExtension("jpeg") == "img"
    assert config.getCategoryForExtension("pdf") == "doc"
    assert config.getCategoryForExtension("zip") is None

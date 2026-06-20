"""Conversion handler registry."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from sleepyconvert.utils.csv_json import convertCsvJson
from sleepyconvert.utils.csv_parquet import convertCsvParquet
from sleepyconvert.utils.csv_pkl import convertCsvPkl
from sleepyconvert.utils.csv_xlsx import convertCsvXlsx
from sleepyconvert.utils.html_md import convertHtmlMd
from sleepyconvert.utils.html_pdf import convertHtmlPdf
from sleepyconvert.utils.json_parquet import convertJsonParquet
from sleepyconvert.utils.json_pkl import convertJsonPkl
from sleepyconvert.utils.json_xlsx import convertJsonXlsx
from sleepyconvert.utils.md_pdf import convertMdPdf
from sleepyconvert.utils.parquet_pkl import convertParquetPkl
from sleepyconvert.utils.parquet_xlsx import convertParquetXlsx
from sleepyconvert.utils.pkl_xlsx import convertPklXlsx
from sleepyconvert.utils.png_jpg import convertPngJpg

ConversionHandler = Callable[[Path, Path], None]

_HANDLERS: dict[frozenset[str], ConversionHandler] = {
    frozenset({"csv", "json"}): convertCsvJson,
    frozenset({"csv", "parquet"}): convertCsvParquet,
    frozenset({"csv", "pkl"}): convertCsvPkl,
    frozenset({"csv", "xlsx"}): convertCsvXlsx,
    frozenset({"json", "parquet"}): convertJsonParquet,
    frozenset({"json", "pkl"}): convertJsonPkl,
    frozenset({"json", "xlsx"}): convertJsonXlsx,
    frozenset({"parquet", "pkl"}): convertParquetPkl,
    frozenset({"parquet", "xlsx"}): convertParquetXlsx,
    frozenset({"pkl", "xlsx"}): convertPklXlsx,
    frozenset({"png", "jpg"}): convertPngJpg,
    frozenset({"png", "jpeg"}): convertPngJpg,
    frozenset({"jpg", "jpeg"}): convertPngJpg,
    frozenset({"html", "md"}): convertHtmlMd,
    frozenset({"html", "pdf"}): convertHtmlPdf,
    frozenset({"md", "pdf"}): convertMdPdf,
}


def getConversionHandler(input_extension: str, output_extension: str) -> ConversionHandler:
    """Return the registered handler for a conversion pair.

    Parameters:
        input_extension: The source file extension.
        output_extension: The destination file extension.

    Returns:
        The conversion handler matching the pair.
    """

    extension_pair = frozenset({input_extension, output_extension})
    handler = _HANDLERS.get(extension_pair)

    if handler is None:
        raise ValueError(
            f"No conversion handler registered for .{input_extension} -> .{output_extension}"
        )

    return handler

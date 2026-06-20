"""Verify convert test outputs against their source fixtures.

tools/test.sh writes outputs to _ephemeral/test_output/ named from_<srcext>.<dstext>:

    data : from_<ext>.csv         <- test.<ext>   (compared as CSV text)
    img  : from_<ext>.<png|jpg>   <- img.<ext>    (compared as decoded images)
    doc  : from_<ext>.md          <- test.<ext>   (compared by surviving text)

Exits non-zero if any output is missing or differs from its source.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

from sleepyconvert.utils.data_shared import readDataFrame
from sleepyconvert.utils.doc_shared import extractTextFromHtml, extractTextFromPdf

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "_ephemeral" / "test_data"
OUT_DIR = ROOT_DIR / "_ephemeral" / "test_output"

_IMAGE_FORMATS: dict[str, str] = {"png": "PNG", "jpg": "JPEG", "jpeg": "JPEG"}
_DOC_EXTENSIONS: frozenset[str] = frozenset({"html", "md", "pdf"})

# Document conversions are lossy (text is prioritized over layout), so outputs
# are checked by how much of the source's text survives rather than byte-equality.
_DOC_TEXT_COVERAGE = 0.9


def verifyDataOutput(source_path: Path, output_path: Path) -> bool:
    """Confirm a CSV output matches the CSV serialization of its source.

    Parameters:
        source_path: The original data fixture (e.g. test.parquet).
        output_path: The generated from_<ext>.csv to validate.

    Returns:
        True when the output matches the expected CSV.
    """

    expected_csv = readDataFrame(input_path=source_path).to_csv(index=False)
    actual_csv = output_path.read_text()

    if expected_csv != actual_csv:
        print(f"  MISMATCH: {output_path.name} differs from {source_path.name}", file=sys.stderr)
        return False

    print(f"  OK: {output_path.name} matches {source_path.name}")
    return True


def verifyImageOutput(source_path: Path, output_path: Path) -> bool:
    """Confirm an image output decodes to the expected format and dimensions.

    Re-encoded rasters are not byte-identical to their source, so this checks
    the decoded format matches the output extension and the size is preserved.

    Parameters:
        source_path: The original image fixture (e.g. img.png).
        output_path: The generated from_<ext>.<png|jpg> to validate.

    Returns:
        True when the output is a valid image of the expected format and size.
    """

    output_extension = output_path.suffix.lower().lstrip(".")
    expected_format = _IMAGE_FORMATS[output_extension]

    with Image.open(output_path) as output_image:
        output_format = output_image.format
        output_size = output_image.size
    with Image.open(source_path) as source_image:
        source_size = source_image.size

    if output_format != expected_format:
        print(
            f"  MISMATCH: {output_path.name} is {output_format}, expected {expected_format}",
            file=sys.stderr,
        )
        return False

    if output_size != source_size:
        print(
            f"  MISMATCH: {output_path.name} is {output_size}, expected {source_size}",
            file=sys.stderr,
        )
        return False

    print(f"  OK: {output_path.name} is a {output_format} matching {source_path.name}")
    return True


def extractDocText(path: Path) -> str:
    """Extract plain text from a supported document file.

    Parameters:
        path: The document path (html, md, or pdf).

    Returns:
        The document's plain-text content.
    """

    match path.suffix.lower():
        case ".html":
            return extractTextFromHtml(html_content=path.read_text(encoding="utf-8"))
        case ".pdf":
            return extractTextFromPdf(input_path=path)
        case ".md":
            return path.read_text(encoding="utf-8")
        case _:
            raise ValueError(f"Unsupported document format: {path.suffix}")


def _tokenize(text: str) -> set[str]:
    """Split text into a set of lowercase alphanumeric word tokens.

    Parameters:
        text: The text to tokenize.

    Returns:
        The set of distinct word tokens.
    """

    return set(re.findall(r"[a-z0-9]+", text.lower()))


def verifyDocOutput(source_path: Path, output_path: Path) -> bool:
    """Confirm a document output preserves the source's textual content.

    Parameters:
        source_path: The original document fixture (e.g. test.html).
        output_path: The generated from_<ext>.md to validate.

    Returns:
        True when at least ``_DOC_TEXT_COVERAGE`` of the source words survive.
    """

    source_words = _tokenize(extractDocText(source_path))
    output_words = _tokenize(extractDocText(output_path))

    if not source_words:
        print(f"  MISMATCH: {source_path.name} has no extractable text", file=sys.stderr)
        return False

    coverage = len(source_words & output_words) / len(source_words)
    if coverage < _DOC_TEXT_COVERAGE:
        print(
            f"  MISMATCH: {output_path.name} keeps only {coverage:.0%} of {source_path.name} text",
            file=sys.stderr,
        )
        return False

    print(f"  OK: {output_path.name} keeps {coverage:.0%} of {source_path.name} text")
    return True


def main() -> int:
    """Verify every from_<srcext>.<dstext> output against its source fixture.

    Returns:
        The process exit code: 0 when all outputs match, 1 otherwise.
    """

    outputs = sorted(OUT_DIR.glob("from_*.*"))
    if not outputs:
        print("No outputs found to verify.", file=sys.stderr)
        return 1

    failures = 0
    for output_path in outputs:
        source_extension = output_path.stem.removeprefix("from_")
        output_extension = output_path.suffix.lower().lstrip(".")

        match output_extension:
            case "csv":
                source_path = DATA_DIR / f"test.{source_extension}"
                verify = verifyDataOutput
            case extension if extension in _IMAGE_FORMATS:
                source_path = DATA_DIR / f"img.{source_extension}"
                verify = verifyImageOutput
            case extension if extension in _DOC_EXTENSIONS:
                source_path = DATA_DIR / f"test.{source_extension}"
                verify = verifyDocOutput
            case _:
                print(f"  UNKNOWN: cannot verify {output_path.name}", file=sys.stderr)
                failures += 1
                continue

        if not source_path.exists():
            print(f"  MISSING SOURCE: {source_path.name}", file=sys.stderr)
            failures += 1
            continue

        if not verify(source_path=source_path, output_path=output_path):
            failures += 1

    if failures > 0:
        print(f"{failures} verification(s) failed.", file=sys.stderr)
        return 1

    print("All outputs verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

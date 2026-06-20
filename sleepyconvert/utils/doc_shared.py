"""Shared helpers for document conversions."""

from __future__ import annotations

from html import escape
from pathlib import Path

from bs4 import BeautifulSoup
from markdown import markdown
from markdownify import markdownify
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas


def convertHtmlMd(input_path: Path, output_path: Path) -> None:
    """Convert between HTML and Markdown documents.

    Parameters:
        input_path: The source document path.
        output_path: The destination document path.

    Returns:
        None.
    """

    match (input_path.suffix.lower(), output_path.suffix.lower()):
        case (".html", ".md"):
            output_path.write_text(
                markdownify(input_path.read_text(encoding="utf-8")), encoding="utf-8"
            )
        case (".md", ".html"):
            html_content = markdown(input_path.read_text(encoding="utf-8"))
            output_path.write_text(html_content, encoding="utf-8")
        case _:
            raise ValueError(
                f"Unsupported HTML/Markdown conversion: {input_path.suffix} -> {output_path.suffix}"
            )


def convertHtmlPdf(input_path: Path, output_path: Path) -> None:
    """Convert between HTML and PDF documents.

    Parameters:
        input_path: The source document path.
        output_path: The destination document path.

    Returns:
        None.
    """

    match (input_path.suffix.lower(), output_path.suffix.lower()):
        case (".html", ".pdf"):
            html_content = input_path.read_text(encoding="utf-8")
            plain_text = extractTextFromHtml(html_content=html_content)
            writePdfFromText(output_path=output_path, text_content=plain_text)
        case (".pdf", ".html"):
            plain_text = extractTextFromPdf(input_path=input_path)
            output_path.write_text(renderHtmlFromText(text_content=plain_text), encoding="utf-8")
        case _:
            raise ValueError(
                f"Unsupported HTML/PDF conversion: {input_path.suffix} -> {output_path.suffix}"
            )


def convertMdPdf(input_path: Path, output_path: Path) -> None:
    """Convert between Markdown and PDF documents.

    Parameters:
        input_path: The source document path.
        output_path: The destination document path.

    Returns:
        None.
    """

    match (input_path.suffix.lower(), output_path.suffix.lower()):
        case (".md", ".pdf"):
            markdown_content = input_path.read_text(encoding="utf-8")
            html_content = markdown(markdown_content)
            plain_text = extractTextFromHtml(html_content=html_content)
            writePdfFromText(output_path=output_path, text_content=plain_text)
        case (".pdf", ".md"):
            plain_text = extractTextFromPdf(input_path=input_path)
            output_path.write_text(plain_text, encoding="utf-8")
        case _:
            raise ValueError(
                f"Unsupported Markdown/PDF conversion: {input_path.suffix} -> {output_path.suffix}"
            )


def extractTextFromHtml(html_content: str) -> str:
    """Extract visible text from an HTML string.

    Parameters:
        html_content: The HTML content to parse.

    Returns:
        The extracted plain-text content.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def extractTextFromPdf(input_path: Path) -> str:
    """Extract plain text from a PDF file.

    Parameters:
        input_path: The source PDF file path.

    Returns:
        The extracted plain-text content.
    """

    pdf_reader = PdfReader(str(input_path))
    page_text = [page.extract_text() or "" for page in pdf_reader.pages]
    return "\n\n".join(text.strip() for text in page_text if text.strip())


def renderHtmlFromText(text_content: str) -> str:
    """Render plain text as a simple HTML document.

    Parameters:
        text_content: The text content to wrap in HTML.

    Returns:
        An HTML document string.
    """

    escaped_text = escape(text_content)
    return f"<html><body><pre>{escaped_text}</pre></body></html>"


def writePdfFromText(output_path: Path, text_content: str) -> None:
    """Write plain text content into a basic PDF file.

    Parameters:
        output_path: The destination PDF file path.
        text_content: The text content to render into the PDF.

    Returns:
        None.
    """

    pdf_canvas = Canvas(str(output_path), pagesize=letter)
    page_width, page_height = letter
    x_position = 72
    y_position = page_height - 72
    line_height = 16

    for line in text_content.splitlines() or [""]:
        if y_position <= 72:
            pdf_canvas.showPage()
            y_position = page_height - 72
        pdf_canvas.drawString(x_position, y_position, line[:110])
        y_position -= line_height

    pdf_canvas.save()

from pathlib import Path

from pypdf import PdfReader


def ingest_pdf(path: str | Path) -> list[dict]:
    """Extract the text of a PDF, one item per page.

    Pages are numbered from 1, as in a PDF viewer, so citations match what the user sees.
    """
    path = Path(path)
    reader = PdfReader(path)

    pages = []
    for number, page in enumerate(reader.pages, start=1):
        pages.append(
            {
                "document": path.name,
                "page": number,
                "text": page.extract_text() or "",
            }
        )
    return pages

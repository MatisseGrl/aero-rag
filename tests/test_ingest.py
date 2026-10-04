from rag.ingest import ingest_pdf


def test_ingest_returns_one_item_per_page(two_page_pdf):
    pages = ingest_pdf(two_page_pdf)

    assert len(pages) == 2


def test_ingest_numbers_pages_from_one(two_page_pdf):
    pages = ingest_pdf(two_page_pdf)

    assert [p["page"] for p in pages] == [1, 2]


def test_ingest_keeps_text_on_the_right_page(two_page_pdf):
    pages = ingest_pdf(two_page_pdf)

    assert "Alpha" in pages[0]["text"]
    assert "Beta" in pages[1]["text"]


def test_ingest_records_document_name(two_page_pdf):
    pages = ingest_pdf(two_page_pdf)

    assert all(p["document"] == "sample.pdf" for p in pages)

from typing import Optional

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a text-based PDF.
    If the PDF is scanned images, it will return little/no text (OCR needed).
    """
    from pypdf import PdfReader
    import io

    reader = PdfReader(io.BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        t = page.extract_text() or ""
        texts.append(t)
    return "\n".join(texts).strip()

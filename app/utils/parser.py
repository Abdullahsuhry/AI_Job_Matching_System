import os
from typing import Optional

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import docx
except Exception:
    docx = None


def extract_text_from_pdf(path: str) -> str:
    if pdfplumber is None:
        return ''
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return '\n'.join(text)


def extract_text_from_docx(path: str) -> str:
    if docx is None:
        return ''
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return '\n'.join(paragraphs)


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    if ext == '.docx':
        return extract_text_from_docx(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''

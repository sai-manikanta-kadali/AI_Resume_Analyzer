import io
import re
from pathlib import Path
import fitz
from docx import Document

ALLOWED = {'.pdf', '.docx'}

def extract_text(filename: str, content: bytes):
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED:
        raise ValueError('Unsupported file type. Upload a PDF or DOCX resume.')
    if not content:
        raise ValueError('The uploaded resume is empty.')
    try:
        if suffix == '.pdf':
            with fitz.open(stream=content, filetype='pdf') as pdf:
                text = '\n'.join(page.get_text() for page in pdf)
                page_count = len(pdf)
        else:
            doc = Document(io.BytesIO(content))
            text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
            text += '\n' + '\n'.join(cell.text for table in doc.tables for row in table.rows for cell in row.cells)
            page_count = None
    except Exception as exc:
        raise ValueError('The document could not be read. It may be corrupted or image-only.') from exc
    cleaned = re.sub(r'[ \t]+', ' ', text).strip()
    if len(cleaned) < 40:
        raise ValueError('Very little readable text was found in the resume.')
    return cleaned, {'filename': filename, 'file_type': suffix[1:].upper(), 'page_count': page_count, 'character_count': len(cleaned)}

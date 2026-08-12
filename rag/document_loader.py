from pathlib import Path
from docx import Document
from pypdf import PdfReader

SUPPORTED={".pdf",".docx",".txt",".md"}

def is_supported(filename):
    return Path(filename).suffix.lower() in SUPPORTED

def load_document(path):
    path=Path(path)
    suffix=path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError("Unsupported document type")
    if suffix==".pdf":
        pages=[]
        for number,page in enumerate(PdfReader(str(path)).pages,1):
            text=page.extract_text() or ""
            if text.strip():
                pages.append({"text":text,"page":number})
        return pages
    if suffix==".docx":
        doc=Document(str(path))
        text="\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return [{"text":text,"page":None}]
    return [{"text":path.read_text(encoding="utf-8",errors="ignore"),"page":None}]

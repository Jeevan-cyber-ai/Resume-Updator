# backend/services/parser.py
import fitz  # PyMuPDF
import docx
import os

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    links = []
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
            for link in page.get_links():
                if "uri" in link:
                    links.append(link["uri"])
                    
        if links:
            unique_links = list(set(links))
            text += "\n\n--- Extracted Hidden URLs ---\n"
            text += "\n".join(unique_links)
            
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    text = ""
    links = []
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
            
        for rel in doc.part.rels.values():
            if "hyperlink" in rel.reltype:
                links.append(rel._target)
                
        if links:
            unique_links = list(set(links))
            text += "\n\n--- Extracted Hidden URLs ---\n"
            text += "\n".join(unique_links)
            
        return text
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return ""

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

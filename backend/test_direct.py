import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.direct_extractor import extract_from_file_directly

def test():
    import docx
    doc = docx.Document()
    doc.add_paragraph("Alice Smith\nalice@example.com\nData Scientist with 3 years experience in SQL and Python.")
    doc.save("dummy_direct.docx")
    
    print("Testing direct extractor...")
    data = extract_from_file_directly("dummy_direct.docx")
    print(f"Extracted Data:\n{data}")
    
    os.remove("dummy_direct.docx")

if __name__ == "__main__":
    test()

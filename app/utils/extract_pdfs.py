import fitz
import os

PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pdfs")

def extract_text(filename):
    path = os.path.join(PDF_DIR, filename)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return ""
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text

def extract_all():
    for f in os.listdir(PDF_DIR):
        if f.endswith(".pdf"):
            print(f"=== {f} ({os.path.getsize(os.path.join(PDF_DIR, f))} bytes) ===")
            text = extract_text(f)
            # Print first 500 chars to preview
            print(text[:500])

if __name__ == "__main__":
    extract_all()

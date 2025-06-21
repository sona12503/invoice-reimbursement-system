from PyPDF2 import PdfReader
import zipfile
import os

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_invoices_from_zip(zip_path, extract_to="invoices/"):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return [os.path.join(extract_to, f) for f in os.listdir(extract_to) if f.endswith(".pdf")]

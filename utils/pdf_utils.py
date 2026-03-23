from pypdf import PdfReader

def extract_pdf_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

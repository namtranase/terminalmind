import PyPDF2
import sys

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text

def main():
    if len(sys.argv) != 2:
        print("Usage: extract_text.py <PDF file path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    print(text)

if __name__ == "__main__":
    main()
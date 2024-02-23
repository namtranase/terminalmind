"""Extract PDF content based on user's input.
"""
import sys
import PyPDF2


def extract_text_from_pdf(pdf_path):
    """Extract text from pdf file."""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text


def main():
    """Main function to extract txt by keyword."""
    if len(sys.argv) != 2:
        print("Usage: extract_text.py <PDF file path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    print(text)


if __name__ == "__main__":
    main()

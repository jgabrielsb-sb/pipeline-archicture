import pdfplumber

from pathlib import Path

def extract_text_from_pdf(pdf_path: Path):
    """
    Extracts and returns the text content from a PDF file.

    This function validates the input path to ensure it is a valid Path object
    pointing to an existing PDF file. It then opens the PDF using `pdfplumber`
    and extracts the text from all pages, concatenating it into a single string.

    Args:
        pdf_path (Path): The path to the PDF file to be read.

    Raises:
        ValueError: If `pdf_path` is not a Path object, is not a file, or does not have a '.pdf' extension.
        FileNotFoundError: If the file at `pdf_path` does not exist.
        PermissionError: If the file cannot be accessed due to insufficient permissions.
    Returns:
        str: The concatenated text extracted from all pages of the PDF.
    """
    if not isinstance(pdf_path, Path):
        raise ValueError('pdf_path must be a Path object')
    
    if not pdf_path.exists():
        raise FileNotFoundError(f'File {pdf_path} not found')
    
    if not pdf_path.is_file() or not pdf_path.suffix == '.pdf':
        raise ValueError('pdf_path must be a file and must have a .pdf extension')
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            return text
    except PermissionError as e: # pragma: no cover
        raise 
    
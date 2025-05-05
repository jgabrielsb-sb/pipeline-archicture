import pytest
from pathlib import Path
import stat

from reportlab.pdfgen import canvas

from packag.modules.pdf_operations import extract_text_from_pdf

@pytest.fixture
def create_temporary_dir_with_permissions(tmp_path):
    """
    Creates a temporary directory with write permission.
    """
    # Step 1: Create the base directory
    protected_dir = tmp_path / "read_write"
    protected_dir.mkdir()

    # Step 2: Remove write permission (Unix only)
    protected_dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)

    yield protected_dir
    
@pytest.fixture
def create_temporary_pdf_file_with_permissions(tmp_path) -> Path:
    protected_dir = tmp_path / "protected"
    protected_dir.mkdir()

    file_path = protected_dir / "test_file.pdf"

    # Create a real PDF file
    c = canvas.Canvas(str(file_path))
    c.drawString(100, 750, "Hello, this is a test PDF!")
    c.save()

    yield file_path

    # Teardown: restore permissions
    protected_dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
    
@pytest.fixture
def create_temporary_pdf_file_without_permissions(tmp_path) -> Path:
    protected_dir = tmp_path / "protected"
    protected_dir.mkdir()

    file_path = protected_dir / "test_file.pdf"

    # Create a real PDF file
    c = canvas.Canvas(str(file_path))
    c.drawString(100, 750, "Hello, this is a test PDF!")
    c.save()

    # Remove write permission from the directory
    protected_dir.chmod(0)

    yield file_path

    # Teardown: restore permissions
    protected_dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)

@pytest.fixture
def create_temporary_txt_file(tmp_path: Path) -> Path:
    txt_path = tmp_path / 'test.txt'
    txt_path.write_text('test')
    return txt_path

@pytest.fixture
def create_temporary_pdf_file(tmp_path: Path) -> Path:
    pdf_path = tmp_path / 'test.pdf'
    return pdf_path

def test_if_extract_text_from_pdf_raises_value_error_when_pdf_path_is_not_a_path_object():
    with pytest.raises(ValueError):
        extract_text_from_pdf('not_a_path')

def test_if_extract_text_from_pdf_raises_file_not_found_error_when_pdf_path_does_not_exist():
    with pytest.raises(FileNotFoundError):
        non_existent_path = Path('non_existent_path')
        extract_text_from_pdf(non_existent_path)

def test_if_extract_text_from_pdf_raises_value_error_when_pdf_path_is_not_a_file(
    create_temporary_dir_with_permissions: Path
):
    with pytest.raises(ValueError):
        extract_text_from_pdf(create_temporary_dir_with_permissions)
        
def test_if_extract_text_from_pdf_raises_value_error_when_path_is_not_a_pdf(
    create_temporary_txt_file: Path
):
    with pytest.raises(ValueError):
        extract_text_from_pdf(create_temporary_txt_file)
        
def test_if_extract_text_from_pdf_raises_permission_error_when_does_not_have_permissions(
    create_temporary_pdf_file_without_permissions: Path
):
    with pytest.raises(PermissionError):
        extract_text_from_pdf(create_temporary_pdf_file_without_permissions)
       
def test_if_extract_text_from_pdf_returns_text_when_pdf_file_has_permissions(
    create_temporary_pdf_file_with_permissions: Path
):
    text = extract_text_from_pdf(create_temporary_pdf_file_with_permissions)
    assert text == 'Hello, this is a test PDF!'
        
        
        
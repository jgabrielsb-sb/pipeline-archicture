from pydantic import BaseModel
from pathlib import Path
from enum import Enum


class FileExtensionEnum(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    XLSX = "xlsx"
    XLS = "xls"
    CSV = "csv"
    XML = "xml"

class File(BaseModel):
    """
    This is the base class for all files.
    It is used to validate the file path and the file extension.
    """
    file_path: Path
    file_extension: FileExtensionEnum
    
    
    


from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToPrestadorExtractor import FileToPrestadorExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class PenedoFileToPrestadorExtractor(FileToPrestadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
        self.text = self.extract_data()

    def extract_data(self):
        try:
            self.text = extract_text_from_pdf(self.file_path)
            return self.text
        
        except FileNotFoundError as e:
            logger.error(f"Error extracting data from file: {e}")
            raise OperationError(
                message=f"File {self.file_path} not found",
                original_exception=e
            ) from e
            
        except ValueError as e:
            logger.error(f"Error extracting data from file: {e}")
            raise OperationError(
                message=f"Error extracting data from file: {e}",
                original_exception=e
            ) from e
            
        except PermissionError as e:
            logger.error(f"Error extracting data from file: {e}")
            raise OperationError(
                message=f"Error extracting data from file: {e}",
                original_exception=e
            ) from e

    def _find(self, pattern):
        if not self.text:
            self.extract_data()
        
        match = re.search(pattern, self.text)
        return match.group(1) if match else None
    
    def _extract_cpf(self):
        return None

    def _extract_cnpj(self):
        match = re.search(r'CPF/CNPJ:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_inscricao_municipal(self):
        match = re.search(r'Inscrição Municipal:\s*(\d+)', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_razao_social(self):
        match = re.search(r'Nome/Razão Social:\s*([^\n]+)', self.text)
        if match:
            return match.group(1).strip()
        return None

    def _extract_endereco(self):
        match = re.search(r'Endereço:\s*([^\n]+)', self.text)
        if match:
            return match.group(1).strip()
        return None

    def _extract_municipio(self):
        match = re.search(r'Municipio:\s*([A-ZÇÃÕÁÉÍÓÚ ]+)\s*UF:', self.text)
        if match:
            return match.group(1).strip().title()
        return None

    def _extract_uf(self):
        match = re.search(r'UF:\s*([A-Z]{2})', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_cep(self):
        match = re.search(r'CEP:\s*(\d{8})', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_numero(self):
        return None
    
    def _extract_bairro(self):
        return None
    
    def _extract_telefone(self):
        match = re.search(r'TEL:\s*(\d+)', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_email(self):
        match = re.search(r'E-mail:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', self.text)
        if match:
            return match.group(1)
        return None


if __name__ == "__main__":
    dtoFile = File(
        file_path=Path('static/notas_fiscais/penedo/document.pdf'),
        file_extension='pdf'
    )
    extractor = PenedoFileToPrestadorExtractor(dtoFile)
    print(extractor.get_all_extracted_info())
from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToPrestadorExtractor import FileToPrestadorExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class ArapiracaFileToPrestadorExtractor(FileToPrestadorExtractor):
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
        match = re.search(r'CPF/CNPJ\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_inscricao_municipal(self):
        match = re.search(r'Inscrição Municipal\s*(\d+)', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_razao_social(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Prestador de Serviços" in line:
                # Next line should be the company name
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        return None

    def _extract_endereco(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Prestador de Serviços" in line:
                if i + 3 < len(lines):
                    addr1 = lines[i + 2].strip().rstrip(',.')
                    addr2 = lines[i + 3].strip().rstrip(',.')
                    
                    # Remove 'Telefone:' and everything after if present
                    if "Telefone:" in addr2:
                        addr2 = addr2.split("Telefone:")[0].strip().rstrip(',.')
                    
                    return f"{addr1}, {addr2}"
        return None

    def _extract_municipio(self):
        match = re.search(r'Cidade\s+([A-ZÇÃÕÁÉÍÓÚ ]+)\s*-\s*[A-Z]{2}', self.text)
        if match:
            return match.group(1).strip().title()
        return None

    def _extract_uf(self):
        match = re.search(r'Cidade\s+[A-ZÇÃÕÁÉÍÓÚ ]+\s*-\s*([A-Z]{2})', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_cep(self):
        match = re.search(r'CEP\s*(\d{8})', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_numero(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Prestador de Serviços" in line:
                # Address line usually contains the number
                if i + 3 < len(lines):
                    address_line = lines[i + 3].strip()
                    match = re.search(r',\s*(\d+)', address_line)
                    if match:
                        return match.group(1)
        return None
    
    def _extract_bairro(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Prestador de Serviços" in line:
                # Bairro is usually after the address line
                if i + 4 < len(lines):
                    bairro_line = lines[i + 4].strip()
                    match = re.search(r'([A-ZÇÃÕÁÉÍÓÚ ]+),', bairro_line)
                    if match:
                        return match.group(1).strip().title()
        return None
    
    def _extract_telefone(self):
        return None
    
    def _extract_email(self):
        match = re.search(r'Email\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', self.text)
        if match:
            return match.group(1)
        return None


if __name__ == "__main__":
    dtoFile = File(
        file_path=Path('static/notas_fiscais/arapiraca/205.pdf'),
        file_extension='pdf'
    )
    text = extract_text_from_pdf(dtoFile.file_path)
    print(text)
    extractor = ArapiracaFileToPrestadorExtractor(dtoFile)
    print(extractor.get_all_extracted_info())
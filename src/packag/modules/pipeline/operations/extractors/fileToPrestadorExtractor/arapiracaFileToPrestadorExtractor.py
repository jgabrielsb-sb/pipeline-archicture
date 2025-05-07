from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToPrestadorExtractor.fileToPrestadorExtractor import FileToPrestadorExtractor
from packag.modules.pipeline.utils.exceptions import (
    OperationError,
    ExtractMethodError
)

from packag.modules.pipeline.utils.messages import (
    OperationErrorMessage,
    ExtractMethodErrorMessage
)
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class ArapiracaFileToPrestadorExtractor(FileToPrestadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
        self.text = None

    def extract_data(self):
        try:
            self.text = extract_text_from_pdf(self.file_path)
            return self.text
        
        except (
            FileNotFoundError, 
            PermissionError, 
            ValueError
        ) as e:
            message = ExtractMethodErrorMessage(
                method_name='extract_data',
                original_exception=e
            )
            
            logger.error(message.get_message())
            
            raise ExtractMethodError(message) 
            
    def _extract_cpf(self):
        return None

    def _extract_cnpj(self):
        if not self.text:
            self.extract_data()
            
        match = re.search(r'CPF/CNPJ\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_inscricao_municipal(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Inscrição Municipal\s*(\d+)', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_razao_social(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Prestador de Serviços" in line:
                # Next line should be the company name
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        return None

    def _extract_endereco(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
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
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Cidade\s+([A-ZÇÃÕÁÉÍÓÚ ]+)\s*-\s*[A-Z]{2}', self.text)
        if match:
            return match.group(1).strip().title()
        return None

    def _extract_uf(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Cidade\s+[A-ZÇÃÕÁÉÍÓÚ ]+\s*-\s*([A-Z]{2})', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_cep(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'CEP\s*(\d{8})', self.text)
        if match:
            return match.group(1)
        return None
    
    def _extract_numero(self):
        return None
    
    def _extract_bairro(self):
        return None
    
    def _extract_telefone(self):
        return None
    
    def _extract_email(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Email\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', self.text)
        if match:
            return match.group(1)
        return None


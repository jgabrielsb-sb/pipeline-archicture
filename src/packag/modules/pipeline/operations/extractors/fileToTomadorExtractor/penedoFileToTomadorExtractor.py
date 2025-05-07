from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor.fileToTomadorExtractor import FileToTomadorExtractor
from packag.modules.pipeline.utils.exceptions import (
    OperationError, ExtractMethodError
    ) 
from packag.modules.pipeline.utils.exceptions import ExtractMethodErrorMessage

from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class PenedoFileToTomadorExtractor(FileToTomadorExtractor):
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
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "CPF/CNPJ" in line:
                match = re.search(r'CPF/CNPJ:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', line)
                if match:
                    return match.group(1)
        return None

    def _extract_inscricao_municipal(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "Inscrição Municipal" in line:
                match = re.search(r'Inscrição Municipal:\s*(\d+)', line)
        if match:
            return match.group(1)
        return None

    def _extract_razao_social(self):
        if not self.text:
            self.extract_data() # pragma: no cover
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "Nome/Razão Social" in line:
                match = re.search(r'Nome/Razão Social:\s*([^\n]+)', line)
        if match:
            return match.group(1).strip()
        return None

    def _extract_endereco(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "Endereço" in line:
                match = re.search(r'Endereço:\s*([^\n]+)', line)
        if match:
            return match.group(1).strip()
        return None

    def _extract_municipio(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "Municipio" in line:
                match = re.search(r'Municipio:\s*([A-ZÇÃÕÁÉÍÓÚ ]+)\s*UF:', line)
        if match:
            return match.group(1).strip().title()
        return None

    def _extract_uf(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "UF" in line:
                match = re.search(r'UF:\s*([A-Z]{2})', line)
        if match:
            return match.group(1)
        return None
    
    def _extract_cep(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "CEP" in line:
                match = re.search(r'CEP:\s*(\d{8})', line)
        if match:
            return match.group(1)
        return None
    
    def _extract_numero(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        match = None
        
        return None
    
    def _extract_bairro(self):
        return None
    
    def _extract_telefone(self):
        return None
    
    def _extract_email(self):
        return None

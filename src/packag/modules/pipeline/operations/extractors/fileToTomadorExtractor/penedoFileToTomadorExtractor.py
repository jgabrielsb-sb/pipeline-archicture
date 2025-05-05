from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor import FileToTomadorExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class PenedoFileToTomadorExtractor(FileToTomadorExtractor):
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
        return None
    
    def _extract_bairro(self):
        return None
    
    def _extract_telefone(self):
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "TEL" in line:
                match = re.search(r'TEL:\s*(\d+)', line)
        if match:
            return match.group(1)
        return None
    
    def _extract_email(self):
        lines = self.text.splitlines()
        capture = False
        match = None
        
        for line in lines:
            if "TOMADOR DE SERVIÇOS" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "E-mail" in line:
                match = re.search(r'E-mail:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
        if match:
            return match.group(1)
        return None


if __name__ == "__main__":
    dtoFile = File(
        file_path=Path('static/notas_fiscais/penedo/document.pdf'),
        file_extension='pdf'
    )
    text = extract_text_from_pdf(dtoFile.file_path)
    print(text)
    
    extractor = PenedoFileToTomadorExtractor(dtoFile)
    print(extractor.get_all_extracted_info())
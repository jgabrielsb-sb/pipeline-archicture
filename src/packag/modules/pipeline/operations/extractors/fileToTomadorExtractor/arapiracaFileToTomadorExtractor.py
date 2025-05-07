from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor.fileToTomadorExtractor import FileToTomadorExtractor
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError
)
from packag.modules.pipeline.utils.messages import (
    ExtractMethodErrorMessage
)
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class ArapiracaFileToTomadorExtractor(FileToTomadorExtractor):
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
        
        matches = re.findall(r'CPF/CNPJ\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', self.text)
        if len(matches) >= 2:
            return matches[1]  # pega a segunda ocorrência (tomador)
        return None

    def _extract_inscricao_municipal(self):
        if not self.text:
            self.extract_data() # pragma: no cover
        
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Tomador de Serviço" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "Inscrição Municipal" in line:
                match = re.search(r'Inscrição Municipal\s*(\d+)', line)
                if match:
                    return match.group(1)
        return None


    def _extract_razao_social(self):
        if not self.text:
            self.extract_data() # pragma: no cover
        
        for line in self.text.splitlines():
            if "Nome do tomador do serviço" in line:
                match = re.search(r'Nome do tomador do serviço\s*(.*)', line)
                if match:
                    return match.group(1).strip()
        return None


    def _extract_endereco(self):
        if not self.text:
            self.extract_data() # pragma: no cover
        
        for line in self.text.splitlines():
            if line.strip().startswith("Endereço"):
                endereco = line.replace("Endereço", "").strip().rstrip(',.')
                return endereco
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
        
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Tomador de Serviço" in line:
                capture = True  # começa a buscar depois dessa linha
            if capture and "Cep" in line:
                match = re.search(r'Cep\s*(\d{5}-?\d{3})', line, re.IGNORECASE)
                if match:
                    return match.group(1).replace('-', '')
        return None

    
    def _extract_numero(self):
        return None
    
    def _extract_bairro(self):
        if not self.text:
            self.extract_data() # pragma: no cover
        
        lines = self.text.splitlines()
        for line in lines:
            if line.strip().startswith("Bairro"):
                # Remove 'Bairro' e pega antes de 'Telefone:'
                bairro = line.replace("Bairro", "").strip()
                if "Telefone:" in bairro:
                    bairro = bairro.split("Telefone:")[0].strip().rstrip(',.')
                return bairro
        return None

    def _extract_telefone(self):
        return None
    
    def _extract_email(self):
        if not self.text:
            self.extract_data() # pragma: no cover
        
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Tomador de Serviço" in line:
                capture = True  # começa a capturar após essa linha
            if capture and "Email" in line:
                match = re.search(r'Email\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line, re.IGNORECASE)
                if match:
                    return match.group(1)
        return None


    def get_all_extracted_info(self):
        return {
            'cpf': self._extract_cpf(),
            'cnpj': self._extract_cnpj(),
            'inscricao_municipal': self._extract_inscricao_municipal(),
            'razao_social': self._extract_razao_social(),
            'endereco': self._extract_endereco(),
            'municipio': self._extract_municipio(),
            'uf': self._extract_uf(),
            'cep': self._extract_cep(),
            'numero': self._extract_numero(),
            'bairro': self._extract_bairro(),
            'telefone': self._extract_telefone(),
            'email': self._extract_email(),
        }


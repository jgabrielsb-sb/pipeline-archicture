from pathlib import Path
import re
import xml.etree.ElementTree as ET
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor.fileToTomadorExtractor import FileToTomadorExtractor
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError,
)

from packag.modules.pipeline.utils.messages import (
    ExtractMethodErrorMessage
)
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type

logger = get_logger('operations')

class MaceioFileToTomadorExtractor(FileToTomadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
        
        self.namespaces = {
            'ns2': 'http://www.giss.com.br/tipos-v2_04.xsd',
        }
        
        self.xml_content = None

    def extract_data(self):
        try:
            if self.file.file_extension.lower() != 'xml':
                raise ValueError("Invalid file type for XML extractor")
            
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
            
        except (
            FileNotFoundError,
            PermissionError,
            ValueError,
            UnicodeDecodeError  # <- aqui é onde entra o erro real
        ) as e:
            message = ExtractMethodErrorMessage(
                method_name='extract_data',
                original_exception=e
            )
            logger.error(message.get_message())
            raise ExtractMethodError(message)


    def _find(self, xpath):
        try:
            if self.xml_content is None:
                self.xml_content = self.extract_data()
                
            root = ET.fromstring(self.xml_content)
            element = root.find(xpath, self.namespaces)
            return element.text if element is not None else None
        except Exception as e:
            message = ExtractMethodErrorMessage(
                method_name='_find',
                original_exception=e
            )
            
            logger.error(message.get_message())
            
            raise ExtractMethodError(message)

    def _extract_cnpj(self):
        return self._find('.//ns2:TomadorServico/ns2:IdentificacaoTomador/ns2:CpfCnpj/ns2:Cnpj')

    def _extract_cpf(self):
        return self._find('.//ns2:TomadorServico/ns2:IdentificacaoTomador/ns2:CpfCnpj/ns2:Cpf')

    def _extract_inscricao_municipal(self):
        return self._find('.//ns2:TomadorServico/ns2:IdentificacaoTomador/ns2:InscricaoMunicipal')

    def _extract_razao_social(self):
        return self._find('.//ns2:TomadorServico/ns2:RazaoSocial')

    def _extract_endereco(self):
        return self._find('.//ns2:TomadorServico/ns2:Endereco/ns2:Endereco')
        
    def _extract_municipio(self):
        return self._find('.//ns2:TomadorServico/ns2:Endereco/ns2:CodigoMunicipio')

    def _extract_uf(self):
        return self._find('.//ns2:TomadorServico/ns2:Endereco/ns2:Uf')
    
    def _extract_cep(self):
        return self._find('.//ns2:TomadorServico/ns2:Endereco/ns2:Cep')
    
    def _extract_numero(self):
        return self._find('.//ns2:TomadorServico/ns2:Endereco/ns2:Numero')
    
    def _extract_bairro(self):
        return self._find('.//ns2:TomadorServico/ns2:Endereco/ns2:Bairro')
    
    def _extract_telefone(self):
        return self._find('.//ns2:TomadorServico/ns2:Contato/ns2:Telefone')
    
    def _extract_email(self):
        return self._find('.//ns2:TomadorServico/ns2:Contato/ns2:Email')

    def get_all_extracted_info(self):
        return {
            'cnpj': self._extract_cnpj(),
            'cpf': self._extract_cpf(),
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
    
    
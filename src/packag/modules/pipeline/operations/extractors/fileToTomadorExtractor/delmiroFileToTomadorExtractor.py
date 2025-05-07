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

class DelmiroFileToTomadorExtractor(FileToTomadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
    
        self.namespaces = {'ns': 'http://www.agili.com.br/nfse_v_1.00.xsd'}

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
            if xpath.startswith('//'):
                xpath = '.' + xpath[1:]
            element = root.find(xpath, self.namespaces)
            return element.text if element is not None else None
        except Exception as e:
            message = ExtractMethodErrorMessage(
                method_name='_find',
                original_exception=e
            )
            
            logger.error(message.get_message())
            
            raise ExtractMethodError(message)

    def _extract_cpf(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cpf') 
    
    def _extract_cnpj(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cnpj')
    
    def _extract_cpf(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cpf')

    def _extract_inscricao_municipal(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:IdentificacaoTomador/ns:InscricaoMunicipal')

    def _extract_razao_social(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:RazaoSocial')

    def _extract_endereco(self):
        tipo_logradouro = self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:TipoLogradouro')
        logradouro = self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:Logradouro')
        if tipo_logradouro and logradouro:
            return f"{tipo_logradouro} {logradouro}"
        return logradouro

    def _extract_municipio(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:Municipio/ns:Descricao')

    def _extract_uf(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:Municipio/ns:Uf')
    
    def _extract_cep(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:Cep')
    
    def _extract_numero(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:Numero')
    
    def _extract_bairro(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Endereco/ns:Bairro')
    
    def _extract_telefone(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Contato/ns:Telefone')
    
    def _extract_email(self):
        return None

    
    
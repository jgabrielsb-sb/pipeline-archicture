from pathlib import Path
import re
import xml.etree.ElementTree as ET
from packag.modules.pipeline.operations.extractors.fileToPrestadorExtractor import FileToPrestadorExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type

logger = get_logger('operations')

class DelmiroFileToPrestadorExtractor(FileToPrestadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
        self.xml_content = self.extract_data()
        self.namespaces = {'ns': 'http://www.agili.com.br/nfse_v_1.00.xsd'}

    def extract_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
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

    def _find(self, xpath):
        try:
            root = ET.fromstring(self.xml_content)
            if xpath.startswith('//'):
                xpath = '.' + xpath[1:]
            element = root.find(xpath, self.namespaces)
            return element.text if element is not None else None
        except Exception as e:
            logger.error(f"Error finding element with xpath {xpath}: {e}")
            return None
        
    def _extract_cpf(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cpf')

    def _extract_cnpj(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:IdentificacaoPrestador/ns:CpfCnpj/ns:Cnpj')

    def _extract_inscricao_municipal(self):
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:IdentificacaoPrestador/ns:InscricaoMunicipal')

    def _extract_razao_social(self):
        return self._find('.//ns:DadosPrestador/ns:RazaoSocial')

    def _extract_nome_fantasia(self):
        return self._find('.//ns:DadosPrestador/ns:NomeFantasia')

    def _extract_endereco(self):
        return self._find('.//ns:DadosPrestador/ns:Endereco/ns:Logradouro')
        
    def _extract_municipio(self):
        return self._find('.//ns:DadosPrestador/ns:Endereco/ns:Municipio/ns:Descricao')

    def _extract_uf(self):
        return self._find('.//ns:DadosPrestador/ns:Endereco/ns:Municipio/ns:Uf')
    
    def _extract_cep(self):
        return self._find('.//ns:DadosPrestador/ns:Endereco/ns:Cep')
    
    def _extract_numero(self):
        return self._find('.//ns:DadosPrestador/ns:Endereco/ns:Numero')
    
    def _extract_bairro(self):
        return self._find('.//ns:DadosPrestador/ns:Endereco/ns:Bairro')
    
    def _extract_telefone(self):
        return None
    
    def _extract_email(self):
        return None


if __name__ == "__main__":
    dtoFile = File(
        file_path=Path('static/notas_fiscais/delmiro/NFSe - 150.xml'),
        file_extension='xml'
    )
    
    
    extractor = DelmiroFileToPrestadorExtractor(dtoFile)
    print(extractor.get_all_extracted_info())
    
    
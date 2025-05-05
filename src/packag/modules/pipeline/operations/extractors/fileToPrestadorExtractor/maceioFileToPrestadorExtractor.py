from pathlib import Path
import re
import xml.etree.ElementTree as ET
from packag.modules.pipeline.operations.extractors.fileToPrestadorExtractor import FileToPrestadorExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type

logger = get_logger('operations')

class MaceioFileToPrestadorExtractor(FileToPrestadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
        self.xml_content = self.extract_data()
        self.namespaces = {
            'ns2': 'http://www.giss.com.br/tipos-v2_04.xsd',
            'ns3': 'http://www.w3.org/2000/09/xmldsig#'
        }

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
            element = root.find(xpath, self.namespaces)
            return element.text if element is not None else None
        except Exception as e:
            logger.error(f"Error finding element with xpath {xpath}: {e}")
            return None
    
    def _extract_cpf(self):
        return None
    
    def _extract_cnpj(self):
        return self._find('.//ns2:Prestador/ns2:CpfCnpj/ns2:Cnpj')

    def _extract_inscricao_municipal(self):
        return self._find('.//ns2:PrestadorServico/ns2:InscricaoMunicipal')

    def _extract_razao_social(self):
        return self._find('.//ns2:PrestadorServico/ns2:RazaoSocial')

    def _extract_endereco(self):
        return self._find('.//ns2:PrestadorServico/ns2:Endereco/ns2:Endereco')

    def _extract_municipio(self):
        codigo_municipio = self._find('.//ns2:PrestadorServico/ns2:Endereco/ns2:CodigoMunicipio')
        # You might want to add a mapping from code to municipality name
        return codigo_municipio

    def _extract_uf(self):
        return self._find('.//ns2:PrestadorServico/ns2:Endereco/ns2:Uf')
    
    def _extract_cep(self):
        return self._find('.//ns2:PrestadorServico/ns2:Endereco/ns2:Cep')
    
    def _extract_numero(self):
        return self._find('.//ns2:PrestadorServico/ns2:Endereco/ns2:Numero')
    
    def _extract_bairro(self):
        return self._find('.//ns2:PrestadorServico/ns2:Endereco/ns2:Bairro')
    
    def _extract_telefone(self):
        return self._find('.//ns2:PrestadorServico/ns2:Contato/ns2:Telefone')
    
    def _extract_email(self):
        return self._find('.//ns2:PrestadorServico/ns2:Contato/ns2:Email')


if __name__ == "__main__":
    dtoFile = File(
        file_path=Path('static/notas_fiscais/maceio/342.xml'),
        file_extension='xml'
    )
    extractor = MaceioFileToPrestadorExtractor(dtoFile)
    print(extractor.get_all_extracted_info())
    
    
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor import FileToTomadorExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type

logger = get_logger('operations')

class DelmiroFileToTomadorExtractor(FileToTomadorExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        
        self.file_path = file.file_path
        self.root = self.extract_data()
        self.xml_content = self.extract_data()
        
        self.namespaces = {'ns': 'http://www.agili.com.br/nfse_v_1.00.xsd'}
    
    def extract_data(self):
        try:
            tree = ET.parse(self.file_path)
            return tree.getroot()
        except Exception as e:
            logger.error(f"Error parsing XML: {e}")
            raise OperationError(...)

    def _find(self, xpath):
        try:
            element = self.root.find(xpath, self.namespaces)
            return element.text if element is not None else None
        except Exception as e:
            logger.error(f"Error finding element with xpath {xpath}: {e}")
            return None

    def _extract_cpf(self):
        cpf = self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:IdentificacaoTomador/ns:CpfCnpj/ns:Cpf')
        print(f"[DEBUG] CPF: {cpf}")
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
        return self._find('.//ns:DeclaracaoPrestacaoServico/ns:DadosTomador/ns:Contato/ns:Email')


if __name__ == "__main__":
    dtoFile = File(
        file_path=Path('static/notas_fiscais/delmiro/NFSe - 150.xml'),
        file_extension='xml'
    )
    extractor = DelmiroFileToTomadorExtractor(dtoFile)
    print(extractor.get_all_extracted_info())
    
    
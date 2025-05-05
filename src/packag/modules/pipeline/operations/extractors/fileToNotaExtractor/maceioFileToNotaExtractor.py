from packag.modules.pipeline.operations.extractors.fileToNotaExtractor import FileToNotaExtractor
import xml.etree.ElementTree as ET

from packag.models.dtoFile import File

from pathlib import Path

from typing import Type

class MaceioFileToNotaExtractor(FileToNotaExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.xml_content = file.file_path.read_text()
        self.ns = {
            'ns2': 'http://www.giss.com.br/tipos-v2_04.xsd',
            'ns3': 'http://www.w3.org/2000/09/xmldsig#'
        }
        if self.xml_content:
            self.root = ET.fromstring(self.xml_content)
        else:
            self.root = None

    def _find(self, path):
        if self.root is None:
            return None
        el = self.root.find(path, self.ns)
        return el.text if el is not None else None

    def _extract_numero_nfs(self):
        return self._find('.//ns2:InfNfse/ns2:Numero')

    def _extract_codigo_autenticidade(self):
        return self._find('.//ns2:InfNfse/ns2:CodigoVerificacao')

    def _extract_data_competencia(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Competencia')

    def _extract_valor_liquido(self):
        return self._find('.//ns2:InfNfse/ns2:ValoresNfse/ns2:ValorLiquidoNfse')

    def _extract_valor_total(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorServicos')

    def _extract_valor_deducoes(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorDeducoes')

    def _extract_valor_pis(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorPis')

    def _extract_valor_cofins(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorCofins')

    def _extract_valor_inss(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorInss')

    def _extract_valor_irrf(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorIr')

    def _extract_valor_csll(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:ValorCsll')

    def _extract_valor_issqn(self):
        return self._find('.//ns2:InfNfse/ns2:ValoresNfse/ns2:ValorIss')

    def _extract_base_calculo(self):
        return self._find('.//ns2:InfNfse/ns2:ValoresNfse/ns2:BaseCalculo')

    def _extract_aliquota(self):
        return self._find('.//ns2:InfNfse/ns2:ValoresNfse/ns2:Aliquota')

    def _extract_issqn_a_reter(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:IssRetido')

    def _extract_estado(self):
        return self._find('.//ns2:InfNfse/ns2:PrestadorServico/ns2:Endereco/ns2:Uf')

    def _extract_codigo_tributacao(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:CodigoTributacaoMunicipio')

    def _extract_discriminacao_servico(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Discriminacao')

    def _extract_opt_simples_nacional(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:OptanteSimplesNacional')

    def _extract_serie(self):
        # Not present in provided XML, return None
        return None

    def _extract_nfse_substituida(self):
        return self._find('.//ns2:InfNfse/ns2:NfseSubstituida')

    def _extract_valor_outras_retencoes(self):
        return self._find('.//ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/ns2:Valores/ns2:OutrasRetencoes')

    def _extract_data_emissao(self):
        return self._find('.//ns2:InfNfse/ns2:DataEmissao')

    def _extract_atv_economica(self):
        return self._find('.//ns2:ItemListaServico')

    def _extract_municipio(self):
        return self._find('.//ns2:InfNfse/ns2:PrestadorServico/ns2:Endereco/ns2:CodigoMunicipio')

if __name__ == '__main__':
    dtoFile = File(
        file_path=Path('static/notas_fiscais/maceio/342.xml'),
        file_extension='xml'
    )
    maceio_file_to_nota_extractor = MaceioFileToNotaExtractor(dtoFile)
    print(maceio_file_to_nota_extractor.run(dtoFile))
    
    
    
    
    
    
    
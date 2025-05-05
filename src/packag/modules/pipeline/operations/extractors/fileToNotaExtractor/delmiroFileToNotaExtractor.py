from packag.modules.pipeline.operations.extractors.fileToNotaExtractor import FileToNotaExtractor
import xml.etree.ElementTree as ET
from packag.models.business import dtoNota

from packag.models.dtoFile import File

from pathlib import Path

from typing import Type


class DelmiroFileToNotaExtractor(FileToNotaExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.xml_content = file.file_path.read_text()
        self.ns = {
            '': 'http://www.agili.com.br/nfse_v_1.00.xsd'
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
        return self._find('.//Numero')

    def _extract_codigo_autenticidade(self):
        return self._find('.//CodigoAutenticidade')

    def _extract_data_competencia(self):
        # In Delmiro's XML, we use DataEmissao as competencia
        return self._find('.//DataEmissao')

    def _extract_valor_liquido(self):
        return self._find('.//ValorLiquido')

    def _extract_valor_total(self):
        return self._find('.//ValorServicos')

    def _extract_valor_deducoes(self):
        return self._find('.//ValorDescontos')

    def _extract_valor_pis(self):
        return self._find('.//ValorPis')

    def _extract_valor_cofins(self):
        return self._find('.//ValorCofins')

    def _extract_valor_inss(self):
        return self._find('.//ValorInss')

    def _extract_valor_irrf(self):
        return self._find('.//ValorIrrf')

    def _extract_valor_csll(self):
        return self._find('.//ValorCsll')

    def _extract_valor_issqn(self):
        return self._find('.//ValorISSQNRecolher')

    def _extract_base_calculo(self):
        return self._find('.//ValorBaseCalculoISSQN')

    def _extract_aliquota(self):
        return self._find('.//AliquotaISSQN')

    def _extract_issqn_a_reter(self):
        return self._find('.//ISSQNRetido')

    def _extract_estado(self):
        return self._find('.//IdentificacaoOrgaoGerador/Municipio/Uf')

    def _extract_codigo_tributacao(self):
        return self._find('.//CodigoAtividadeEconomica')

    def _extract_discriminacao_servico(self):
        return self._find('.//ListaServico/DadosServico/Discriminacao')

    def _extract_opt_simples_nacional(self):
        return self._find('.//OptanteSimplesNacional')

    def _extract_serie(self):
        # Not present in Delmiro's XML
        return None

    def _extract_nfse_substituida(self):
        # Not present in Delmiro's XML
        return None

    def _extract_valor_outras_retencoes(self):
        return self._find('.//ValorOutrasRetencoes')

    def _extract_data_emissao(self):
        return self._find('.//DataEmissao')

    def _extract_atv_economica(self):
        return self._find('.//CodigoAtividadeEconomica')

    def _extract_municipio(self):
        return self._find('.//IdentificacaoOrgaoGerador/Municipio/CodigoMunicipioIBGE')


if __name__ == '__main__':
    dtoFile = File(
        file_path=Path('static/notas_fiscais/delmiro/NFSe - 1779(1).xml'),
        file_extension='xml'
    )
    delmiro_file_to_nota_extractor = DelmiroFileToNotaExtractor(dtoFile)
    print(delmiro_file_to_nota_extractor.run(dtoFile))
    
    
    
    
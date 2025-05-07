import pytest
from pathlib import Path
from packag.models.dtoFile import File
from packag.modules.pipeline.operations.extractors.fileToNotaExtractor.delmiroFileToNotaExtractor import DelmiroFileToNotaExtractor
from packag.models.business import dtoNota


def normalize_lines(s):
    return '\n'.join(line.strip() for line in s.splitlines())

NOTAS = [
    (
        "287.xml",
        {
            'numero_nfs': '287',
            'codigo_autenticidade': '9747a45ae57a0b827e8818e97591a30a',
            'data_competencia': '2024-06-01T12:53:18', 
            'valor_liquido': '3800.00',  # <ValorLiquido>
            'valor_total': '4000.00',  # <ValorServicos>
            'valor_deducoes': '0.00',  # <ValorDescontos>
            'valor_pis': '0.00',  # <ValorPis>
            'valor_cofins': '0.00',  # <ValorCofins>
            'valor_inss': '0.00',  # <ValorInss>
            'valor_irrf': '0.00',  # <ValorIrrf>
            'valor_csll': '0.00',  # <ValorCsll>
            'valor_issqn': '200.00',  # <ValorISSQNCalculado>
            'base_calculo': '4000.00',  # <ValorBaseCalculoISSQN>
            'aliquota': '5.00',  # <AliquotaISSQN>
            'issqn_a_reter': '1',  # <ISSQNRetido>
            'estado': 'AL',  # <Uf> (from IdentificacaoOrgaoGerador / Municipio)
            'codigo_tributacao': '8.02',  # <CodigoAtividadeEconomica>
            'discriminacao_servico': 'CT 01136/24\nAE 375275\nItem 0001',  # <Discriminacao>
            'opt_simples_nacional': '1',  # <OptanteSimplesNacional>
            'serie': None,  # Not present in this XML
            'nfse_substituida': None,  # Not present in this XML
            'valor_outras_retencoes': '0.00',  # <ValorOutrasRetencoes>
            'data_emissao': '2024-06-01T12:53:18',  # <DataEmissao>
            'atv_economica': '8.02',  # <CodigoAtividadeEconomica>
            'municipio': '2702405',  # <CodigoMunicipioIBGE>
        }
    ),
    (
        "324.xml",
        {
            'numero_nfs': '324',  # <Numero>
            'codigo_autenticidade': '7b3d7cfaa95b0891b137c8d0ece952d1',  # <CodigoAutenticidade>
            'data_competencia': '2024-08-19T18:47:37',  # (not present in XML)
            'valor_liquido': '760.00',  # <ValorLiquido>
            'valor_total': '800.00',  # <ValorServicos>
            'valor_deducoes': '0.00',  # <ValorDescontos>
            'valor_pis': '0.00',  # <ValorPis>
            'valor_cofins': '0.00',  # <ValorCofins>
            'valor_inss': '0.00',  # <ValorInss>
            'valor_irrf': '0.00',  # <ValorIrrf>
            'valor_csll': '0.00',  # <ValorCsll>
            'valor_issqn': '40.00',  # <ValorISSQNCalculado>
            'base_calculo': '800.00',  # <ValorBaseCalculoISSQN>
            'aliquota': '5.00',  # <AliquotaISSQN>
            'issqn_a_reter': '1',  # <ISSQNRetido>
            'estado': 'AL',  # <IdentificacaoOrgaoGerador><Municipio><Uf>
            'codigo_tributacao': '8.02',  # <CodigoAtividadeEconomica>
            'discriminacao_servico': 'CT 04032/24\nAE 381854\nItem 0001',  # <Discriminacao>
            'opt_simples_nacional': '1',  # <OptanteSimplesNacional>
            'serie': None,  # (not present in XML)
            'nfse_substituida': None,  # (not present in XML)
            'valor_outras_retencoes': '0.00',  # <ValorOutrasRetencoes>
            'data_emissao': '2024-08-19T18:47:37',  # <DataEmissao>
            'atv_economica': '8.02',  # <CodigoAtividadeEconomica>
            'municipio': '2702405',  # <CodigoMunicipioIBGE>
        }
    ),
    (
        "352.xml",
        {
            'numero_nfs': '352',  # <Numero>
            'codigo_autenticidade': 'b8f7e34f742891b368f65bead5c4cbd8',  # <CodigoAutenticidade>
            'data_competencia': '2024-10-01T18:47:24',  # Not present in XML
            'valor_liquido': '2280.00',  # <ValorLiquido>
            'valor_total': '2400.00',  # <ValorServicos>
            'valor_deducoes': '0.00',  # <ValorDescontos>
            'valor_pis': '0.00',  # <ValorPis>
            'valor_cofins': '0.00',  # <ValorCofins>
            'valor_inss': '0.00',  # <ValorInss>
            'valor_irrf': '0.00',  # <ValorIrrf>
            'valor_csll': '0.00',  # <ValorCsll>
            'valor_issqn': '120.00',  # <ValorISSQNCalculado>
            'base_calculo': '2400.00',  # <ValorBaseCalculoISSQN>
            'aliquota': '5.00',  # <AliquotaISSQN>
            'issqn_a_reter': '1',  # <ISSQNRetido>
            'estado': 'AL',  # <IdentificacaoOrgaoGerador> → <Municipio> → <Uf>
            'codigo_tributacao': '17.01',  # <CodigoAtividadeEconomica>
            'discriminacao_servico': 'Contrato 03814/24 AE 381501 item 0001',  # <Discriminacao>
            'opt_simples_nacional': '1',  # <OptanteSimplesNacional>
            'serie': None,  # Not in XML
            'nfse_substituida': None,  # Not in XML
            'valor_outras_retencoes': '0.00',  # <ValorOutrasRetencoes>
            'data_emissao': '2024-10-01T18:47:24',  # <DataEmissao>
            'atv_economica': '17.01',  # <CodigoAtividadeEconomica>
            'municipio': '2702405',  # <CodigoMunicipioIBGE> inside <IdentificacaoOrgaoGerador>
        }
    ),
]


# Map expected keys to extractor method names
FIELD_TO_METHOD = {
    'numero_nfs': '_extract_numero_nfs',
    'codigo_autenticidade': '_extract_codigo_autenticidade',
    'data_competencia': '_extract_data_competencia',
    'valor_liquido': '_extract_valor_liquido',
    'valor_total': '_extract_valor_total',
    'valor_deducoes': '_extract_valor_deducoes',
    'valor_pis': '_extract_valor_pis',
    'valor_cofins': '_extract_valor_cofins',
    'valor_inss': '_extract_valor_inss',
    'valor_irrf': '_extract_valor_irrf',
    'valor_csll': '_extract_valor_csll',
    'valor_issqn': '_extract_valor_issqn',
    'base_calculo': '_extract_base_calculo',
    'aliquota': '_extract_aliquota',
    'issqn_a_reter': '_extract_issqn_a_reter',
    'estado': '_extract_estado',
    'codigo_tributacao': '_extract_codigo_tributacao',
    'discriminacao_servico': '_extract_discriminacao_servico',
    'opt_simples_nacional': '_extract_opt_simples_nacional',
    'serie': '_extract_serie',
    'nfse_substituida': '_extract_nfse_substituida',
    'valor_outras_retencoes': '_extract_valor_outras_retencoes',
    'data_emissao': '_extract_data_emissao',
    'atv_economica': '_extract_atv_economica',
    'municipio': '_extract_municipio',
}

###### TESTING IF EACH ABSTRACT METHOD OF EXTRACTION IS RETURNING THE CORRECT VALUE ######
@pytest.mark.parametrize("xml_filename,expected", NOTAS)
def test_if_all_extractor_methods_are_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/delmiro/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = DelmiroFileToNotaExtractor(dto_file)
    # iterating over the expected fields and values
    for field, exp_value in expected.items():
        # getting the method name from the field
        method_name = FIELD_TO_METHOD[field]
        # getting the method from the extractor
        method = getattr(extractor, method_name)
        result = method()
        # normalizing the result and the expected value
        normalized_result = normalize_lines(result) if result else None
        normalized_expected = normalize_lines(exp_value) if exp_value else None
        # asserting the result and the expected value
        assert normalized_result == normalized_expected, f"Field '{field}' failed for {xml_filename}: expected {normalized_expected!r}, got {normalized_result!r}"


###### TESTTING IF THE METHOD GET_ALL_EXTRACTED_INFO IS RETURNING THE CORRECT VALUE ######
@pytest.mark.parametrize("xml_filename,expected", NOTAS)
def test_if_method_get_all_extracted_info_is_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/delmiro/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = DelmiroFileToNotaExtractor(dto_file)
    # getting all the extracted info
    extracted_info = extractor.get_all_extracted_info()
    # normalizing each field of the extracted info
    normalized_extracted_info = {
        key: normalize_lines(value) if value else None
        for key, value in extracted_info.items()
    }
    # normalizing the expected value
    normalized_expected = {
        key: normalize_lines(value) if value else None
        for key, value in expected.items()
    }
    # asserting the extracted info and the expected value
    assert normalized_extracted_info == normalized_expected, f"Extracted info failed for {xml_filename}: expected {normalized_expected!r}, got {normalized_extracted_info!r}"
    

###### TESTING IF THE METHOD VALIDATE_OUTPUT IS RETURNING A DTO NOTA EXTRACTED INFO ######
@pytest.mark.parametrize("xml_filename,expected", NOTAS)
def test_if_run_is_returning_a_dto_nota_extracted_info(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/delmiro/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = DelmiroFileToNotaExtractor(dto_file)
    result_dto_nota = extractor.run(dto_file)
    assert isinstance(result_dto_nota, dtoNota.NotaExtractedInfo)




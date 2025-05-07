import pytest
from pathlib import Path
from packag.models.dtoFile import File
from packag.modules.pipeline.operations.extractors.fileToNotaExtractor.maceioFileToNotaExtractor import MaceioFileToNotaExtractor
from packag.models.business import dtoNota

from reportlab.pdfgen import canvas

def normalize_lines(s):
            return '\n'.join(line.strip() for line in s.splitlines())
        
NOTAS = [
    (
        "21.xml",
        {
            'numero_nfs': '21',
            'codigo_autenticidade': 'BIJSGSPYW',
            'data_competencia': '2025-05-04-03:00',
            'valor_liquido': '2744.00',
            'valor_total': '2800.00',
            'valor_deducoes': '0.00',
            'valor_pis': '0.00',
            'valor_cofins': '0.00',
            'valor_inss': '0.00',
            'valor_irrf': '0.00',
            'valor_csll': '0.00',
            'valor_issqn': '56.00',
            'base_calculo': '2800.00',
            'aliquota': '2.00',
            'issqn_a_reter': '1',
            'estado': 'AL',
            'codigo_tributacao': '8.02',
            'discriminacao_servico': 'Contrato 00523/25 AE 394610 item 0001',
            'opt_simples_nacional': '1',
            'serie': None,
            'nfse_substituida': None,
            'valor_outras_retencoes': '0.00',
            'data_emissao': '2025-05-04T18:30:20.630-03:00',
            'atv_economica': '8.02',
            'municipio': '2704302',
        }
    ),
    (
        "160.xml",
        {
            'numero_nfs': '160',
            'codigo_autenticidade': 'LU9MVVYGZ',
            'data_competencia': '2024-01-11-03:00',
            'valor_liquido': '15631.00',
            'valor_total': '15950.00',
            'valor_deducoes': '0.00',
            'valor_pis': '0.00',
            'valor_cofins': '0.00',
            'valor_inss': '0.00',
            'valor_irrf': '0.00',
            'valor_csll': '0.00',
            'valor_issqn': '319.00',
            'base_calculo': '15950.00',
            'aliquota': '2.00',
            'issqn_a_reter': '1',
            'estado': 'AL',
            'codigo_tributacao': '6190699',
            'discriminacao_servico': '''Referente a ordem de Fornecimento N°: 371050.\n     Solicitação N°: 17512\n     Descrição do Serviço:\n     Serviço de instalação de 20 câmeras de segurança (com passagem de cabeamento; instalação de rack e power balun; instalação e configuração de HD e DVR), conforme a proposta comercial N° 47880-01-2024\n     Dados bancários:\n     Caixa Econômica federal\n     Daniela Marques Tenório Gomes - JLG TELECOM\n     Ag:2404\n     Op:003\n     C/C: 00004220-6''',
            'opt_simples_nacional': '1',
            'serie': None,
            'nfse_substituida': None,
            'valor_outras_retencoes': '0.00',
            'data_emissao': '2024-01-11T13:09:38.496-03:00',
            'atv_economica': '31.01',
            'municipio': '2704302',
        }
    ),
    (
        "405.xml",
        {
            'numero_nfs': '405',
            'codigo_autenticidade': 'HYJODWYFB',
            'data_competencia': '2025-05-05-03:00',
            'valor_liquido': '1878.34',
            'valor_total': '1920.00',
            'valor_deducoes': '0.00',
            'valor_pis': '0.00',
            'valor_cofins': '0.00',
            'valor_inss': '0.00',
            'valor_irrf': '0.00',
            'valor_csll': '0.00',
            'valor_issqn': '41.66',
            'base_calculo': '1920.00',
            'aliquota': '2.17',
            'issqn_a_reter': '1',
            'estado': 'AL',
            'codigo_tributacao': '17.01',
            'discriminacao_servico': 'Contrato 00509/25 AE 394524 item 0001, 0002, 0003 e 0004',
            'opt_simples_nacional': '1',
            'serie': None,
            'nfse_substituida': None,
            'valor_outras_retencoes': '0.00',
            'data_emissao': '2025-05-05T11:30:46.887-03:00',
            'atv_economica': '17.01',
            'municipio': '2704302',
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
    
    # file path of the xml maceio nota fiscal file
    file_path = Path(f'static/notas_fiscais/maceio/{xml_filename}')
    
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    
    # building the extractor with the dto file
    extractor = MaceioFileToNotaExtractor(dto_file)
    
    # iterating over the expected fields and values
    for field, exp_value in expected.items():
        
        # getting the method name from the field
        method_name = FIELD_TO_METHOD[field]
        
        # getting the method from the extractor
        method = getattr(extractor, method_name)
        result = method()
        
        # normalizing the result and the expected value
        normalized_result = normalize_lines(result) if result else None
        normalized_expected = normalize_lines(exp_value) if result else None
        
        # asserting the result and the expected value
        assert normalized_result == normalized_expected, f"Field '{field}' failed for {xml_filename}: expected {normalized_expected!r}, got {normalized_result!r}"


###### TESTTING IF THE METHOD GET_ALL_EXTRACTED_INFO IS RETURNING THE CORRECT VALUE ######
@pytest.mark.parametrize("xml_filename,expected", NOTAS)
def test_if_method_get_all_extracted_info_is_returning_the_correct_value(xml_filename, expected):
    
    # file path of the xml maceio nota fiscal file
    file_path = Path(f'static/notas_fiscais/maceio/{xml_filename}')
    
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    
    # building the extractor with the dto file
    extractor = MaceioFileToNotaExtractor(dto_file)
    
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
    # file path of the xml maceio nota fiscal file
    file_path = Path(f'static/notas_fiscais/maceio/{xml_filename}')
    
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    
    # building the extractor with the dto file
    extractor = MaceioFileToNotaExtractor(dto_file)
    
    result_dto_nota = extractor.run(dto_file)
    
    assert isinstance(result_dto_nota, dtoNota.NotaExtractedInfo)
    




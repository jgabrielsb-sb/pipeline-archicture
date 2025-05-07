import pytest
from pathlib import Path
from packag.models.dtoFile import File
from packag.modules.pipeline.operations.extractors.fileToNotaExtractor.penedoFileToNotaExtractor import PenedoFileToNotaExtractor
from packag.models.business import dtoNota
from unittest.mock import MagicMock
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError
)

from reportlab.pdfgen import canvas


def normalize_lines(s):
    return '\n'.join(line.strip() for line in s.splitlines())



NOTAS = [
    (
        "590.pdf",
        {
            "numero_nfs": "00000590",
            "codigo_autenticidade": "G1SS-8SA6W",
            "data_competencia": "ABR/2024",
            "valor_liquido": "1.078,00",
            "valor_total": "1.100,00",
            "valor_deducoes": "0,00",
            "valor_pis": "0,00",
            "valor_cofins": "0,00",
            "valor_inss": "0,00",
            "valor_irrf": "0,00",
            "valor_csll": "0,00",
            "valor_issqn": "22,00",
            "base_calculo": "1.100,00",
            "aliquota": "2,00",
            "issqn_a_reter": "1",
            "estado": "AL",
            "codigo_tributacao": "7020400",
            "discriminacao_servico": "1.CONTRATO 306//24 - AE: 372160-0001 #QTD:1 - V.UND.:R$1.100,00 - TOTAL.:R$1.100,00",
            "opt_simples_nacional": "1",
            "serie": None,
            "nfse_substituida": None,
            "valor_outras_retencoes": "0,00",
            "data_emissao": "01/04/2024 16:38:26",
            "atv_economica": "1701",
            "municipio": "Penedo"
        }

    ),
    (
        "646.pdf",
        {
            "numero_nfs": "00000646",
            "codigo_autenticidade": "LS3P-GSAVM",
            "data_competencia": "MAR/2025",
            "valor_liquido": "2.508,80",
            "valor_total": "2.560,00",
            "valor_deducoes": "0,00",
            "valor_pis": "0,00",
            "valor_cofins": "0,00",
            "valor_inss": "0,00",
            "valor_irrf": "0,00",
            "valor_csll": "0,00",
            "valor_issqn": "51,20",
            "base_calculo": "2.560,00",
            "aliquota": "2,00",
            "issqn_a_reter": "1",
            "estado": "AL",
            "codigo_tributacao": "7020400",
            "discriminacao_servico": "1. CONTRATO 00050/25 AE 391411 ITEM 0001 #QTD:1 - V.UND.:R$2.560,00 - TOTAL.:R$2.560,00",
            "opt_simples_nacional": "1",
            "serie": None,
            "nfse_substituida": None,
            "valor_outras_retencoes": "0,00",
            "data_emissao": "10/03/2025 10:34:42",
            "atv_economica": "1701",
            "municipio": "Penedo"
        }


    ),
    (
        "647.pdf",
        {
            "numero_nfs": "00000647",
            "codigo_autenticidade": "49NR-5DQ16",
            "data_competencia": "ABR/2025",
            "valor_liquido": "7.448,00",
            "valor_total": "7.600,00",
            "valor_deducoes": "0,00",
            "valor_pis": "0,00",
            "valor_cofins": "0,00",
            "valor_inss": "0,00",
            "valor_irrf": "0,00",
            "valor_csll": "0,00",
            "valor_issqn": "152,00",
            "base_calculo": "7.600,00",
            "aliquota": "2,00",
            "issqn_a_reter": "1",
            "estado": "AL",
            "codigo_tributacao": "7020400",
            "discriminacao_servico": "1.CONTRATO00230/25 AE 392710 ITEM 0001. #QTD:1 - V.UND.:R$7.600,00 - TOTAL.:R$7.600,00",
            "opt_simples_nacional": "1",
            "serie": None,
            "nfse_substituida": None,
            "valor_outras_retencoes": "0,00",
            "data_emissao": "02/04/2025 17:01:35",
            "atv_economica": "1701",
            "municipio": "Penedo"
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

@pytest.fixture
def create_temporary_pdf_file(tmp_path) -> Path:
    file_path = tmp_path / 'test_file.pdf'

    # Create a PDF and write "Hello, World!" on it
    c = canvas.Canvas(str(file_path))
    c.drawString(100, 750, "Hello, World!")
    c.save()

    return file_path

###### TESTING IF EACH ABSTRACT METHOD OF EXTRACTION IS RETURNING THE CORRECT VALUE ######
@pytest.mark.parametrize("xml_filename,expected", NOTAS)
def test_if_all_extractor_methods_are_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/penedo/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = PenedoFileToNotaExtractor(dto_file)
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
        print(f'field: {method_name}, result: {result}, expected: {exp_value}')
        print(f'normalized_result: {normalized_result}, normalized_expected: {normalized_expected}')
        assert normalized_result == normalized_expected, f"Field '{field}' failed for {xml_filename}: expected {normalized_expected!r}, got {normalized_result!r}"


###### TESTTING IF THE METHOD GET_ALL_EXTRACTED_INFO IS RETURNING THE CORRECT VALUE ######
@pytest.mark.parametrize("xml_filename,expected", NOTAS)
def test_if_method_get_all_extracted_info_is_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/penedo/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = PenedoFileToNotaExtractor(dto_file)
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
    file_path = Path(f'static/notas_fiscais/penedo/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = PenedoFileToNotaExtractor(dto_file)
    result_dto_nota = extractor.run(dto_file)
    assert isinstance(result_dto_nota, dtoNota.NotaExtractedInfo)
    
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES FILENOTFOUNDERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_filenotfounderror():
    
    extractor = PenedoFileToNotaExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=FileNotFoundError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()
        
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES PERMISSIONERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_permissionerror():
    extractor = PenedoFileToNotaExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=PermissionError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()    
        
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES VALUEERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_valueerror():
    extractor = PenedoFileToNotaExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=ValueError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()
        
###### TESTING IF THE EXTRACTING METHODS RETURN NONE WHEN DOESNT MATCH #####
def test_if_the_extracting_methods_return_none_when_doesnt_match(
    create_temporary_pdf_file: Path
):
    dto_file = File(file_path=create_temporary_pdf_file, file_extension='pdf')
   
    # building the extractor with the dto file
    extractor = PenedoFileToNotaExtractor(dto_file)
    
    extracted_info = extractor.get_all_extracted_info()
    
    for field, value in extracted_info.items():
        assert value is None, f"Field '{field}' should be None"
    
    
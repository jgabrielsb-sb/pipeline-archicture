import pytest
from pathlib import Path
from packag.models.dtoFile import File
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor.penedoFileToTomadorExtractor import (
    PenedoFileToTomadorExtractor
)
from packag.models.business import dtoTomador
from unittest.mock import MagicMock
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError
)

from reportlab.pdfgen import canvas


def normalize_lines(s):
    return '\n'.join(line.strip() for line in s.splitlines())


TOMADORES = [
    (
        "590.pdf",
        {
            "cnpj": "12.517.413/0003-99",
            "cpf": None,
            "inscricao_municipal": "6619",
            "razao_social": "SERVICO DE APOIO AS M E P EMPRESAS DE ALAGOAS SEBRAE AL",
            "endereco": "PRC JACOME CALHEIROS, 64 CENTRO HISTORICO",
            "numero": None,
            "bairro": None,
            "municipio": "Penedo",
            "uf": "AL",
            "cep": "57200000",
            "telefone": None,
            "email": None
        }
    ),
    (
        "646.pdf",
        {
            "cnpj": "12.517.413/0003-99",
            "cpf": None,
            "inscricao_municipal": "6619",
            "razao_social": "SERVICO DE APOIO AS M E P EMPRESAS DE ALAGOAS SEBRAE AL",
            "endereco": "PRC JACOME CALHEIROS, 64 CENTRO HISTORICO",
            "numero": None,
            "bairro": None,
            "municipio": "Penedo",
            "uf": "AL",
            "cep": "57200000",
            "telefone": None,
            "email": None
        }


    ),
    (
        "647.pdf",
        {
            "cnpj": "12.517.413/0003-99",
            "cpf": None,
            "inscricao_municipal": "6619",
            "razao_social": "SERVICO DE APOIO AS M E P EMPRESAS DE ALAGOAS SEBRAE AL",
            "endereco": "PRC JACOME CALHEIROS, 64 CENTRO HISTORICO",
            "numero": None,
            "bairro": None,
            "municipio": "Penedo",
            "uf": "AL",
            "cep": "57200000",
            "telefone": None,
            "email": None
        }
    ),
]


# Map expected keys to extractor method names
FIELD_TO_METHOD = {
    'cnpj': '_extract_cnpj',
    'cpf': '_extract_cpf',
    'inscricao_municipal': '_extract_inscricao_municipal',
    'razao_social': '_extract_razao_social',
    'endereco': '_extract_endereco',
    'numero': '_extract_numero',
    'bairro': '_extract_bairro',
    'municipio': '_extract_municipio',
    'uf': '_extract_uf',
    'cep': '_extract_cep',
    'telefone': '_extract_telefone',
    'email': '_extract_email', 
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
@pytest.mark.parametrize("xml_filename,expected", TOMADORES)
def test_if_all_extractor_methods_are_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/penedo/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = PenedoFileToTomadorExtractor(dto_file)
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
@pytest.mark.parametrize("xml_filename,expected", TOMADORES)
def test_if_method_get_all_extracted_info_is_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/penedo/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = PenedoFileToTomadorExtractor(dto_file)
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
@pytest.mark.parametrize("xml_filename,expected", TOMADORES)
def test_if_run_is_returning_a_dto_tomador_extracted_info(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/penedo/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = PenedoFileToTomadorExtractor(dto_file)
    result_dto_tomador = extractor.run(dto_file)
    assert isinstance(result_dto_tomador, dtoTomador.TomadorExtractedInfo)
    
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES FILENOTFOUNDERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_filenotfounderror():
    
    extractor = PenedoFileToTomadorExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=FileNotFoundError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()
        
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES PERMISSIONERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_permissionerror():
    extractor = PenedoFileToTomadorExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=PermissionError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()    
        
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES VALUEERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_valueerror():
    extractor = PenedoFileToTomadorExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=ValueError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()
        
###### TESTING IF THE EXTRACTING METHODS RETURN NONE WHEN DOESNT MATCH #####
def test_if_the_extracting_methods_return_none_when_doesnt_match(
    create_temporary_pdf_file: Path
):
    dto_file = File(file_path=create_temporary_pdf_file, file_extension='pdf')
   
    # building the extractor with the dto file
    extractor = PenedoFileToTomadorExtractor(dto_file)
    
    extracted_info = extractor.get_all_extracted_info()
    
    for field, value in extracted_info.items():
        assert value is None, f"Field '{field}' should be None"
    
    
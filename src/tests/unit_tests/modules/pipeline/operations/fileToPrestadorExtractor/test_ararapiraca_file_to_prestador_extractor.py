import pytest
from pathlib import Path
from packag.models.dtoFile import File
from packag.modules.pipeline.operations.extractors.fileToPrestadorExtractor.arapiracaFileToPrestadorExtractor import ArapiracaFileToPrestadorExtractor
from packag.models.business import dtoPrestador
from unittest.mock import MagicMock
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError
)

from reportlab.pdfgen import canvas


def normalize_lines(s):
    return '\n'.join(line.strip() for line in s.splitlines())



PRESTADORES = [
    (
        "205.pdf",
        {
            "cnpj": "24.588.668/0001-60",
            "cpf": None,
            "inscricao_municipal": "150539",
            "razao_social": "JULIANA ALVES SCALDAFERRI LTDA",
            "endereco": "NEIDE BARBOSA ROCHA, 446, SAO LUIZ",
            "numero": None,
            "bairro": None,
            "municipio": "Arapiraca",
            "uf": "AL",
            "cep": "57301403",
            "telefone": None,
            "email": "julialves26@gmail.com"
        }
    ),
    (
        "694.pdf",
        {
            "cnpj": "09.550.814/0001-74",
            "cpf": None,
            "inscricao_municipal": "155290",
            "razao_social": "CENTRO EDUCACIONAL ANA JECEV LTDA - ME",
            "endereco": "PEDRO LIVINO, 279,LOTE 1;, JARDIM ESPERANCA",
            "numero": None,
            "bairro": None,
            "municipio": "Arapiraca",
            "uf": "AL",
            "cep": "57307520",
            "telefone": None,
            "email": "processual@synergein-al.com"
        }
    ),
    (
        "1008.pdf",
        {
            "cnpj": "15.274.089/0001-51",
            "cpf": None,
            "inscricao_municipal": "112898",
            "razao_social": "IMAGEM CONSULTORIA E ASSESSORIA S/S LTDA",
            "endereco": "ERASMO PINHEIRO DA SILVA, 136,NULL, BOA VISTA",
            "numero": None,
            "bairro": None,
            "municipio": "Arapiraca",
            "uf": "AL",
            "cep": "57303284",
            "telefone": None,
            "email": "elismacedo_al@hotmail.com"
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
@pytest.mark.parametrize("xml_filename,expected", PRESTADORES)
def test_if_all_extractor_methods_are_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/arapiraca/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = ArapiracaFileToPrestadorExtractor(dto_file)
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
@pytest.mark.parametrize("xml_filename,expected", PRESTADORES)
def test_if_method_get_all_extracted_info_is_returning_the_correct_value(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/arapiraca/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = ArapiracaFileToPrestadorExtractor(dto_file)
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
@pytest.mark.parametrize("xml_filename,expected", PRESTADORES)
def test_if_run_is_returning_a_dto_nota_extracted_info(xml_filename, expected):
    # file path of the xml penedo nota fiscal file
    file_path = Path(f'static/notas_fiscais/arapiraca/{xml_filename}')
    # building the dto file with the file path and the file extension
    dto_file = File(file_path=file_path, file_extension='xml')
    # building the extractor with the dto file
    extractor = ArapiracaFileToPrestadorExtractor(dto_file)
    result_dto_prestador = extractor.run(dto_file)
    assert isinstance(result_dto_prestador, dtoPrestador.PrestadorExtractedInfo)
    
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES FILENOTFOUNDERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_filenotfounderror():
    
    extractor = ArapiracaFileToPrestadorExtractor(MagicMock(
        file_path=Path('static/notas_fiscais/arapiraca/000.pdf'),
        file_extension='pdf'
    ))
    extractor.extract_text_from_pdf = MagicMock(side_effect=FileNotFoundError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()
        
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES PERMISSIONERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_permissionerror():
    extractor = ArapiracaFileToPrestadorExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=PermissionError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()    
        
###### TESTING IF EXTRACT_DATA RAISE EXTRACT METHOD ERROR  WHEN EXTRACT_TEXT_FROM_PDF RAISES VALUEERROR ######
def test_if_extract_data_raise_extract_method_error_when_extract_text_from_pdf_raises_valueerror():
    extractor = ArapiracaFileToPrestadorExtractor(MagicMock())
    extractor.extract_text_from_pdf = MagicMock(side_effect=ValueError)
    
    with pytest.raises(ExtractMethodError):
        extractor.extract_data()
        
###### TESTING IF THE EXTRACTING METHODS RETURN NONE WHEN DOESNT MATCH #####
def test_if_the_extracting_methods_return_none_when_doesnt_match(
    create_temporary_pdf_file: Path
):
    dto_file = File(file_path=create_temporary_pdf_file, file_extension='pdf')
   
    # building the extractor with the dto file
    extractor = ArapiracaFileToPrestadorExtractor(dto_file)
    
    extracted_info = extractor.get_all_extracted_info()
    
    for field, value in extracted_info.items():
        assert value is None, f"Field '{field}' should be None"
        
        
    
    
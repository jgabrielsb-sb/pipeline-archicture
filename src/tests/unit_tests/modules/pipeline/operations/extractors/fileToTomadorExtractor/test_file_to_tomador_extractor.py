import pytest


from unittest.mock import MagicMock
from packag.modules.pipeline.operations.extractors.fileToTomadorExtractor import FileToTomadorExtractor
from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    ExtractMethodError, 
    OperationError,
    GetAllExtractedInfoError,
)
from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage,
)
from packag.models.business import dtoTomador

from packag.models import dtoFile

    
class DummyFileToTomadorExtractor(FileToTomadorExtractor):
    def _extract_cpf(self): 
        return 'dummy data'
    
    def _extract_cnpj(self): 
        return 'dummy data'
    
    def _extract_inscricao_municipal(self): 
        return 'dummy data'
    
    def _extract_razao_social(self): 
        return 'dummy data'
    
    def _extract_endereco(self): 
        return 'dummy data'
    
    def _extract_municipio(self): 
        return 'dummy data'
    
    def _extract_uf(self): 
        return 'dummy data'
    
    def _extract_cep(self): 
        return 'dummy data'
    
    def _extract_numero(self): 
        return 'dummy data'
    
    def _extract_bairro(self): 
        return 'dummy data'
    
    def _extract_telefone(self): 
        return 'dummy data'
    
    def _extract_email(self): 
        return 'dummy data'
    

###### TEST IF VALIDATE_INPUT RAISES VALIDATION ERROR IF INPUT IS NOT A DTOFILE ######
def test_if_validate_input_raises_validation_error_if_input_is_not_a_dtofile():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    with pytest.raises(ValidationError):
        dummy_file_to_tomador_extractor.validate_input(input_data=1)
        
###### IF VALIDATE_INPUT THE INPUT WHEN VALID ######
def test_if_validate_input_returns_the_input_when_valid():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    assert dummy_file_to_tomador_extractor.validate_input(input_data=dtoFile.File(file_path='test', file_extension='xml')) == dtoFile.File(file_path='test', file_extension='xml')
        
def test_if_get_extract_methods_returns_a_dictionary_with_the_correct_methods():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()

    assert dummy_file_to_tomador_extractor.get_extract_methods() == {
            'cpf': dummy_file_to_tomador_extractor._extract_cpf,
            'cnpj': dummy_file_to_tomador_extractor._extract_cnpj,
            'inscricao_municipal': dummy_file_to_tomador_extractor._extract_inscricao_municipal,
            'razao_social': dummy_file_to_tomador_extractor._extract_razao_social,
            'endereco': dummy_file_to_tomador_extractor._extract_endereco,
            'municipio': dummy_file_to_tomador_extractor._extract_municipio,
            'uf': dummy_file_to_tomador_extractor._extract_uf,
            'cep': dummy_file_to_tomador_extractor._extract_cep,
            'numero': dummy_file_to_tomador_extractor._extract_numero,
            'bairro': dummy_file_to_tomador_extractor._extract_bairro,
            'telefone': dummy_file_to_tomador_extractor._extract_telefone,
            'email': dummy_file_to_tomador_extractor._extract_email,
        }
    
def test_if_run_extract_method_raises_extract_method_error_if_method_raises_an_exception():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    def test_method():
        raise Exception('test exception')
    
    with pytest.raises(ExtractMethodError) as e:
        dummy_file_to_tomador_extractor.run_extract_method(method=test_method)
        
    assert str(e.value) == 'Error on extract method test_method -\ntest exception'
    
def test_if_get_all_extracted_info_raises_get_all_extracted_info_error_if_an_exception_is_raised_in_any_of_the_methods():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    def test_method():
        raise Exception('test exception')
    
    dummy_file_to_tomador_extractor.get_extract_methods = MagicMock(return_value={'test_method': test_method})
    
    with pytest.raises(GetAllExtractedInfoError) as e:
        dummy_file_to_tomador_extractor.get_all_extracted_info()
        
    assert str(e.value) == 'Error on the following extracting methods:\nError on extract method test_method -\ntest exception'
    
def test_if_get_all_extracted_info_returns_a_dict_with_the_correct_methods():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    def test_method():
        return 'dummy data'
    
    dummy_file_to_tomador_extractor.get_extract_methods = MagicMock(return_value={'test_method': test_method})
    
    assert dummy_file_to_tomador_extractor.get_all_extracted_info() == {'test_method': 'dummy data'}
    
def test_if_get_all_extracted_info_raises_get_all_extracted_info_if_more_than_one_method_raise_exceptions():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    def test_method():
        raise Exception('test exception')
    
    def test_method_2():
        raise Exception('test exception 2')
    
    dummy_file_to_tomador_extractor.get_extract_methods = MagicMock(return_value={'test_method': test_method, 'test_method_2': test_method_2})
    
    with pytest.raises(GetAllExtractedInfoError) as e:
        dummy_file_to_tomador_extractor.get_all_extracted_info()
        
    assert str(e.value) == 'Error on the following extracting methods:\nError on extract method test_method -\ntest exception\nError on extract method test_method_2 -\ntest exception 2'
    
def test_if_validate_output_raises_validation_error_if_output_is_not_a_dict():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    with pytest.raises(ValidationError):
        dummy_file_to_tomador_extractor.validate_output(output_data=1)
        
def test_if_validate_output_raises_validation_error_if_pydantic_validation_error_is_raised():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    output_data = {
        'cpf': 'dummy data',
    }
    
    with pytest.raises(ValidationError) as e:
        dummy_file_to_tomador_extractor.validate_output(output_data=output_data)
        
def test_if_validate_output_returns_a_dto_nota_extracted_info_object():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    output_data = {
            'cpf': 'test',
            'cnpj': 'test',
            'inscricao_municipal': 'test',
            'razao_social': 'test',
            
            'endereco': 'test',
            'municipio': 'test',
            'uf': 'test',
            'cep': 'test',
            
            'numero': 'test',
            'bairro': 'test',
            'telefone': 'test',
            'email': 'test',
        } 
    
    assert dummy_file_to_tomador_extractor.validate_output(output_data=output_data) == dtoTomador.TomadorExtractedInfo(**output_data)
    
def test_if_run_raises_operation_error_if_input_data_raises_validation_error():
    extractor = DummyFileToTomadorExtractor()

    # Patch validate_input on the instance
    extractor.validate_input = MagicMock(side_effect=ValidationError(
        message=ValidationErrorMessage(
            function_name='test',
            input_name='test',
            received_type='test',
            expected_type='test'
        )
    ))

    file = dtoFile.File(file_path='test', file_extension='xml')

    with pytest.raises(OperationError):
        extractor.run(input_data=file)
    
def test_if_run_returns_a_dto_tomador_object():
    dummy_file_to_tomador_extractor = DummyFileToTomadorExtractor()
    
    dummy_file_to_tomador_extractor.validate_input = MagicMock(return_value=dtoFile.File(file_path='test', file_extension='xml'))
    
    dummy_file_to_tomador_extractor.get_all_extracted_info = MagicMock(return_value={'test_method': 'dummy data'})
    
    dummy_file_to_tomador_extractor.validate_output = MagicMock(return_value=dtoTomador.TomadorExtractedInfo(cpf='test', cnpj='test', inscricao_municipal='test', razao_social='test', endereco='test', municipio='test', uf='test', cep='test', numero='test', bairro='test', telefone='test', email='test'))
    
    assert dummy_file_to_tomador_extractor.run(input_data=dtoFile.File(file_path='test', file_extension='xml')) == dtoTomador.TomadorExtractedInfo(cpf='test', cnpj='test', inscricao_municipal='test', razao_social='test', endereco='test', municipio='test', uf='test', cep='test', numero='test', bairro='test', telefone='test', email='test')
        






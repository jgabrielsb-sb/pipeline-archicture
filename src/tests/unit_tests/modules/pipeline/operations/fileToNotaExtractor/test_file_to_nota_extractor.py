import pytest


from unittest.mock import MagicMock
from packag.modules.pipeline.operations.extractors.fileToNotaExtractor import FileToNotaExtractor
from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    ExtractMethodError, 
    OperationError,
    GetAllExtractedInfoError,
)
from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage,
)
from packag.models.business import dtoNota

from packag.models import dtoFile


class DummyFileToNotaExtractor(FileToNotaExtractor):
    def _extract_numero_nfs(self): 
        return 'dummy data'
    
    def _extract_codigo_autenticidade(self): 
        return 'dummy data'
    
    def _extract_data_competencia(self): 
        return 'dummy data'
    
    def _extract_valor_liquido(self): 
        return 'dummy data'
    
    def _extract_valor_total(self): 
        return 'dummy data'
    
    def _extract_valor_deducoes(self): 
        return 'dummy data'
    
    def _extract_valor_pis(self): 
        return 'dummy data'
    
    def _extract_valor_cofins(self): 
        return 'dummy data'
    
    def _extract_valor_inss(self): 
        return 'dummy data'
    
    def _extract_valor_irrf(self): 
        return 'dummy data'
    
    def _extract_valor_csll(self): 
        return 'dummy data'
    
    def _extract_valor_issqn(self): 
        return 'dummy data'
    
    def _extract_base_calculo(self): 
        return 'dummy data'
    
    def _extract_aliquota(self): 
        return 'dummy data'
    
    def _extract_issqn_a_reter(self): 
        return 'dummy data'
    
    def _extract_issqn_a_reter(self): 
        return 'dummy data'
    
    def _extract_estado(self): 
        return 'dummy data'
    
    def _extract_codigo_tributacao(self): 
        return 'dummy data'
    
    def _extract_discriminacao_servico(self):
        return 'dummy data'
    
    def _extract_opt_simples_nacional(self):
        return 'dummy data'
    
    def _extract_serie(self):
        return 'dummy data'
    
    def _extract_nfse_substituida(self):
        return 'dummy data'
    
    def _extract_valor_outras_retencoes(self):
        return 'dummy data'
    
    def _extract_data_emissao(self):
        return 'dummy data'
    
    def _extract_atv_economica(self):
        return 'dummy data'
    
    def _extract_municipio(self):
        return 'dummy data'

###### TEST IF VALIDATE_INPUT RAISES VALIDATION ERROR IF INPUT IS NOT A DTOFILE ######
def test_if_validate_input_raises_validation_error_if_input_is_not_a_dtofile():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    with pytest.raises(ValidationError):
        dummy_file_to_nota_extractor.validate_input(input_data=1)
        
def test_if_get_extract_methods_returns_a_dictionary_with_the_correct_methods():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    assert dummy_file_to_nota_extractor.get_extract_methods() == {
            'numero_nfs': dummy_file_to_nota_extractor._extract_numero_nfs,
            'codigo_autenticidade': dummy_file_to_nota_extractor._extract_codigo_autenticidade,
            'data_competencia': dummy_file_to_nota_extractor._extract_data_competencia,
            'valor_liquido': dummy_file_to_nota_extractor._extract_valor_liquido,
            'valor_total': dummy_file_to_nota_extractor._extract_valor_total,
            'valor_deducoes': dummy_file_to_nota_extractor._extract_valor_deducoes,
            'valor_pis': dummy_file_to_nota_extractor._extract_valor_pis,
            'valor_cofins': dummy_file_to_nota_extractor._extract_valor_cofins,
            'valor_inss': dummy_file_to_nota_extractor._extract_valor_inss,
            'valor_irrf': dummy_file_to_nota_extractor._extract_valor_irrf,
            'valor_csll': dummy_file_to_nota_extractor._extract_valor_csll,
            'valor_issqn': dummy_file_to_nota_extractor._extract_valor_issqn,
            'base_calculo': dummy_file_to_nota_extractor._extract_base_calculo,
            'aliquota': dummy_file_to_nota_extractor._extract_aliquota,
            'issqn_a_reter': dummy_file_to_nota_extractor._extract_issqn_a_reter,
            'estado': dummy_file_to_nota_extractor._extract_estado,
            'codigo_tributacao': dummy_file_to_nota_extractor._extract_codigo_tributacao,
            'discriminacao_servico': dummy_file_to_nota_extractor._extract_discriminacao_servico,
            'opt_simples_nacional': dummy_file_to_nota_extractor._extract_opt_simples_nacional,
            'serie': dummy_file_to_nota_extractor._extract_serie,
            'nfse_substituida': dummy_file_to_nota_extractor._extract_nfse_substituida,
            'valor_outras_retencoes': dummy_file_to_nota_extractor._extract_valor_outras_retencoes,
            'data_emissao': dummy_file_to_nota_extractor._extract_data_emissao,
            'atv_economica': dummy_file_to_nota_extractor._extract_atv_economica,
            'municipio': dummy_file_to_nota_extractor._extract_municipio,
        }
    
def test_if_run_extract_method_raises_extract_method_error_if_method_raises_an_exception():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    def test_method():
        raise Exception('test exception')
    
    with pytest.raises(ExtractMethodError) as e:
        dummy_file_to_nota_extractor.run_extract_method(method=test_method)
        
    assert str(e.value) == 'Error on extract method test_method -\ntest exception'
    
def test_if_get_all_extracted_info_raises_get_all_extracted_info_error_if_an_exception_is_raised_in_any_of_the_methods():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    def test_method():
        raise Exception('test exception')
    
    dummy_file_to_nota_extractor.get_extract_methods = MagicMock(return_value={'test_method': test_method})
    
    with pytest.raises(GetAllExtractedInfoError) as e:
        dummy_file_to_nota_extractor.get_all_extracted_info()
        
    assert str(e.value) == 'Error on the following extracting methods:\nError on extract method test_method -\ntest exception'
    
def test_if_get_all_extracted_info_raises_get_all_extracted_info_if_more_than_one_method_raise_exceptions():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    def test_method():
        raise Exception('test exception')
    
    def test_method_2():
        raise Exception('test exception 2')
    
    dummy_file_to_nota_extractor.get_extract_methods = MagicMock(return_value={'test_method': test_method, 'test_method_2': test_method_2})
    
    with pytest.raises(GetAllExtractedInfoError) as e:
        dummy_file_to_nota_extractor.get_all_extracted_info()
        
    assert str(e.value) == 'Error on the following extracting methods:\nError on extract method test_method -\ntest exception\nError on extract method test_method_2 -\ntest exception 2'
    
def test_if_validate_output_raises_validation_error_if_output_is_not_a_dict():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    with pytest.raises(ValidationError):
        dummy_file_to_nota_extractor.validate_output(output_data=1)
        
def test_if_validate_output_raises_validation_error_if_pydantic_validation_error_is_raised():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    output_data = {
        'numero_nfs': 'dummy data',
    }
    
    with pytest.raises(ValidationError) as e:
        dummy_file_to_nota_extractor.validate_output(output_data=output_data)
        
def test_if_validate_output_returns_a_dto_nota_extracted_info_object():
    dummy_file_to_nota_extractor = DummyFileToNotaExtractor()
    
    output_data = {
            'numero_nfs': 'test',
            'codigo_autenticidade': 'test',
            'data_competencia': 'test',
            'valor_liquido': 'test',
            'valor_total': 'test',
            'valor_deducoes': 'test',
            'valor_pis': 'test',
            'valor_cofins': 'test',
            'valor_inss': 'test',
            'valor_irrf': 'test',
            'valor_csll': 'test',
            'valor_issqn': 'test',
            'base_calculo': 'test',
            'aliquota': 'test',
            'issqn_a_reter': 'test',
            'estado': 'test',
            'codigo_tributacao': 'test',
            'discriminacao_servico': 'test',
            'opt_simples_nacional': 'test',
            'serie': 'test',
            'nfse_substituida': 'test',
            'valor_outras_retencoes': 'test',
            'data_emissao': 'test',
            'atv_economica': 'test',
            'municipio': 'test',
        } 
    
    assert dummy_file_to_nota_extractor.validate_output(output_data=output_data) == dtoNota.NotaExtractedInfo(**output_data)
    
def test_if_run_raises_operation_error_if_input_data_raises_validation_error():
    extractor = DummyFileToNotaExtractor()

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






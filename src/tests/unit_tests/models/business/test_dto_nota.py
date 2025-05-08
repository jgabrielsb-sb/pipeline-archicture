from pydantic import ValidationError
from packag.models.business.enum import (
    EstadoEnum,
    MunicipioEnum
)
from packag.models.business import (
    dtoNota,
)

import pytest

from datetime import date

from tests.unit_tests.models.test_dto_base import BasePydanticModelTest

class TestNotaExtractedInfo(BasePydanticModelTest):
    """
    This class is used to test the NotaExtractedInfo model.
    It inherits from BasePydanticModelTest, which provides the basic functionality for testing Pydantic models.
    If it pass, it means that the model is working as expected:
        * the optional fields are not raising errors when not provided
        * the required fields are raising errors when not provided
        * the fields are of the correct type
    """
    
    def get_model(self):
        return dtoNota.NotaExtractedInfo
    
    def get_required_fields_info(self):
        REQUIRED_COLUMNS_INFO = {
            'numero_nfs': str ,
            'codigo_autenticidade': str,
            
            'data_competencia': str,
            
            'valor_liquido': str,
            'valor_total': str,
            'valor_deducoes': str,
            'valor_pis': str,
            'valor_cofins': str,
            'valor_inss': str,
            'valor_irrf': str,
            'valor_csll': str,
            'valor_issqn': str,
            'base_calculo': str,
            'aliquota': str,
            'issqn_a_reter': str,
            'estado': str,
            
            'codigo_tributacao': str,
            'discriminacao_servico': str,
            'opt_simples_nacional': str,
            
            'atv_economica': str,
            'municipio': str
        }
        
        return REQUIRED_COLUMNS_INFO
    
    def get_optional_fields_info(self):
        OPTIONAL_COLUMNS_INFO = {
            'serie': str,   
            'nfse_substituida': str, 
            'valor_outras_retencoes': str,
            'data_emissao': str,
        }
        
        return OPTIONAL_COLUMNS_INFO

class TestNotaFormattedInfo(BasePydanticModelTest):
    """
    This class is used to test the NotaFormattedInfo model.
    It inherits from BasePydanticModelTest, which provides the basic functionality for testing Pydantic models.
    If it pass, it means that the model is working as expected:
        * the optional fields are not raising errors when not provided
        * the required fields are raising errors when not provided
        * the fields are of the correct type
    """ 
    
    def get_model(self):
        return dtoNota.NotaFormattedInfo
    
    def get_required_fields_info(self):
        REQUIRED_COLUMNS_INFO = {
            'numero_nfs': str,
            'codigo_autenticidade': str,
            
            'data_competencia': str,
            
            'valor_liquido': str,
            'valor_total': str,
            'valor_deducoes': str,
            'valor_pis': str,
            'valor_cofins': str,
            'valor_inss': str,
            'valor_irrf': str,
            'valor_csll': str,
            'valor_issqn': str,
            'base_calculo': str,
            'aliquota': str,
            'issqn_a_reter': str,
            
            'estado': str,
            
            'codigo_tributacao': str,
            'discriminacao_servico': str,
            'opt_simples_nacional': str,
            'atv_economica': str,
            'atv_economica_normalized': str,
            'municipio': str
        }
        
        return REQUIRED_COLUMNS_INFO
    def get_optional_fields_info(self):
        OPTIONAL_COLUMNS_INFO = {
            'serie': str,   
            'nfse_substituida': str, 
            'valor_outras_retencoes': str,
            'data_emissao': str,
        }
    
        return OPTIONAL_COLUMNS_INFO
    
    def build_valid_data_with_all_fields(self):
        return {
            'numero_nfs': '1',
            'codigo_autenticidade': 'AAKS78901234',
            'data_competencia': '2021-01-01',
            'valor_liquido': '100',
            'valor_total': '100',
            'valor_deducoes': '100',
            'valor_pis': '100',
            'valor_cofins': '100',
            'valor_inss': '100',
            'valor_irrf': '100',
            'valor_csll': '100',
            'valor_issqn': '100',
            'base_calculo': '100',
            'aliquota': '100',
            'issqn_a_reter': '100',
            'estado': 'AL',
            'codigo_tributacao': '12345678901234',
            'discriminacao_servico': 'Teste',
            'opt_simples_nacional': '1',
            'atv_economica': '12.34567.8901.234',
            'atv_economica_normalized': '12345678901234',
            'municipio': 'Maceió'
        }
    def test_create_element_that_the_fields_that_accept_only_numbers_are_not_numbers_raises_error(self):
        """
        Test if the fields that are strings but should accept only numbers 
        raise error if not numbers.
        """
        self.validate()
        only_numbers_fields = [
            'codigo_tributacao',
            'atv_economica_normalized',
            'numero_nfs',
            'opt_simples_nacional'
        ]
        
        valid_data_with_all_fields = self.build_valid_data_with_all_fields()
        Model_Class = self.get_model()
        
        for field in only_numbers_fields:
            copy_of_valid_data_with_all_fields = valid_data_with_all_fields.copy()
            copy_of_valid_data_with_all_fields[field] = 'A12345678901234'
            
            with pytest.raises(ValueError):
                Model_Class(**copy_of_valid_data_with_all_fields)
            
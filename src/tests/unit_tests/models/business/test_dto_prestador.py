from pydantic import ValidationError
from packag.models.business.enum import (
    EstadoEnum,
    MunicipioEnum
)
from packag.models.business import (
    dtoPrestador,
)

import pytest

from tests.unit_tests.models.test_dto_base import BasePydanticModelTest

class TestPrestadorExtractedInfo(BasePydanticModelTest):
    """
    This class is used to test the PrestadorExtractedInfo model.
    It inherits from BasePydanticModelTest, which provides the basic functionality for testing Pydantic models.
    If it pass, it means that the model is working as expected:
        * the optional fields are not raising errors when not provided
        * the required fields are raising errors when not provided
        * the fields are of the correct type
    """
    
    def get_model(self):
        return dtoPrestador.PrestadorExtractedInfo
    
    def get_required_fields_info(self):
        REQUIRED_COLUMNS_INFO = {
            'inscricao_municipal': str,
            'razao_social': str,
    
            'endereco': str,
            'municipio': str,
            'uf': str,
            'cep': str,
        }
        
        return REQUIRED_COLUMNS_INFO
    
    def get_optional_fields_info(self):
        OPTIONAL_COLUMNS_INFO = {
            'cnpj': str,
            'cpf': str,
            'numero': str,
            'bairro': str,
            'telefone': str,
            'email': str
        }
        
        return OPTIONAL_COLUMNS_INFO
    
    def test_create_without_cpf_and_cnpj_raises_error(self):
        """
        As defined in the model, the prestador must have at 
        least one of the following fields: 
        -> cnpj or cpf.
        Then, if the model is not provided with any of these fields, 
        it should raise a ValueError.
        """
        self.validate()
        
        valid_data_with_all_fields = self.build_valid_data_with_all_fields()
        
        valid_data_without_cnpj_and_cpf = valid_data_with_all_fields.copy()
        
        for field in ['cnpj', 'cpf']:
            valid_data_without_cnpj_and_cpf.pop(field)

        Model_Class = self.get_model()
        with pytest.raises(ValueError):
            Model_Class(**valid_data_without_cnpj_and_cpf)
            
class TestPrestadorFormattedInfo(BasePydanticModelTest):
    """
    This class is used to test the PrestadorFormattedInfo model.
    It inherits from BasePydanticModelTest, which provides the basic functionality for testing Pydantic models.
    If it pass, it means that the model is working as expected:
        * the optional fields are not raising errors when not provided
        * the required fields are raising errors when not provided
        * the fields are of the correct type
    """
    
    def get_model(self):
        return dtoPrestador.PrestadorFormattedInfo
    
    def get_required_fields_info(self):
        REQUIRED_COLUMNS_INFO = {
            'inscricao_municipal': str,
            'razao_social': str,
    
            'endereco': str,
            'municipio': MunicipioEnum,
            'uf': EstadoEnum,
            'cep': str,
        }
        
        return REQUIRED_COLUMNS_INFO
    
    def get_optional_fields_info(self):
        OPTIONAL_COLUMNS_INFO = {
            'cnpj': str,
            'cpf': str,
            'numero': int,
            'bairro': str,
            'telefone': str,
            'email': str
        }
        
        return OPTIONAL_COLUMNS_INFO
    
    def build_valid_data_with_all_fields(self):
        return {
            'cnpj': '12345678901234',
            'cpf': '12345678901',
            'inscricao_municipal': '12345678901234',
            'razao_social': 'Teste',
            'endereco': 'Teste',
            'municipio': MunicipioEnum.MACEIO,
            'uf': EstadoEnum.AL,
            'cep': '12345678901234',
            'numero': 123,
            'bairro': 'Teste',
            'telefone': '12345678901234',
            'email': 'teste@teste.com'
        }
    
    def test_create_without_cpf_and_cnpj_raises_error(self):
        """
        As defined in the model, the prestador must have at 
        least one of the following fields: 
        -> cnpj or cpf.
        Then, if the model is not provided with any of these fields, 
        it should raise a ValueError.
        """
        self.validate()
        
        valid_data_with_all_fields = self.build_valid_data_with_all_fields()
        
        valid_data_without_cnpj_and_cpf = valid_data_with_all_fields.copy()
        
        for field in ['cnpj', 'cpf']:
            valid_data_without_cnpj_and_cpf.pop(field)

        Model_Class = self.get_model()
        with pytest.raises(ValueError):
            Model_Class(**valid_data_without_cnpj_and_cpf)
            
    def test_create_element_that_the_fields_that_accept_only_numbers_are_not_numbers_raises_error(self):
        """
        Test if the fields that are strings but should accept only numbers 
        raise error if not numbers.
        """
        self.validate()
        only_numbers_fields = [
            'cnpj',
            'cpf',
            'inscricao_municipal',
            'cep',
            'numero',
            'telefone'
        ]
        
        valid_data_with_all_fields = self.build_valid_data_with_all_fields()
        Model_Class = self.get_model()
        
        for field in only_numbers_fields:
            copy_of_valid_data_with_all_fields = valid_data_with_all_fields.copy()
            copy_of_valid_data_with_all_fields[field] = 'A12345678901234'
            
            with pytest.raises(ValueError):
                Model_Class(**copy_of_valid_data_with_all_fields)
        
        
        
                
                
            
        
        
        
        
        
        
        
    
            
            
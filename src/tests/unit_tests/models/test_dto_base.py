from pydantic import ValidationError
import pytest
from abc import ABC, abstractmethod
from pydantic import BaseModel

from datetime import date

from packag.models.business.enum import (
    EstadoEnum,
    MunicipioEnum
)

DUMMY_TEST_DATA = {
    str: 'teste',
    int: 1,
    float: 1.0,
    EstadoEnum: EstadoEnum.AL,
    MunicipioEnum: MunicipioEnum.ARAPIRACA,
    date: date(2021, 1, 1)
}


class BasePydanticModelTest(ABC):
    
    DUMMY_TEST_DATA = DUMMY_TEST_DATA
    
    @abstractmethod
    def get_model(self):
        """
        HERE, you must return the Pydantic Model Class that you want to test.
        """
        pass
    
    @abstractmethod
    def get_required_fields_info(self):
        """
        HERE, you must return a dictionary with the required fields and their types.
        Example:
            required_fields = {
                'name': str,
                'age': int,
                'email': str,
            }
        """
        pass
    
    @abstractmethod
    def get_optional_fields_info(self):
        """
        HERE, you must return a dictionary with the optional fields and their types.
        Example:
            optional_fields = {
                'address': str,
                'phone': int,
            }
        """
        pass
    
    def validate_fields_info(self, fields_info: dict):
        """
        Given fields_info, this function will:
        1. Validate if its a dictionary
            Raise TypeError if not
        2. Validate if all the keys are strings
            Raise TypeError if not
        3. Validate if all the values are types
            Raise TypeError if not
        4. Validate if all the values are in DUMMY_TEST_DATA
            Raise ValueError if not
          
        If all the validations pass, the function will return the fields_info dictionary.
        """
        if not isinstance(fields_info, dict):
            raise TypeError("fields_info must be a dictionary containing the fields as keys and their types as values")
            
        for field, field_type in fields_info.items():
            if not isinstance(field, str):
                raise TypeError("All the keys of fields_info must be strings")
            
            if field_type not in self.DUMMY_TEST_DATA:
                raise ValueError(f"You must define the dummy data for: {field_type}")
            
        return fields_info
    
    def validate_if_every_field_of_the_model_has_been_defined(self):
        optional_fields_info = self.get_optional_fields_info()
        required_fields_info = self.get_required_fields_info()
        
        
        all_fields = {**required_fields_info, **optional_fields_info}
        
        model_fields = self.get_model().model_fields.keys()
        
        missing_fields = []
        
        for field in model_fields:
            if field not in all_fields:
                missing_fields.append(field)
                
        if missing_fields:
            raise ValueError(f"The fields {missing_fields} are not defined in the fields_info. You must add them as a required or optional field.")
        
    def validate_if_every_defined_field_is_present_in_the_model(self):
        
        optional_fields_info = self.get_optional_fields_info()
        required_fields_info = self.get_required_fields_info()
        
        all_fields = {**required_fields_info, **optional_fields_info}
        
        model_fields = self.get_model().model_fields.keys()
        
        missing_fields = []
        
        for field in all_fields:
            if field not in model_fields:
                missing_fields.append(field)
                
        if missing_fields:
            raise ValueError(f"The fields {missing_fields} are defined in the fields_info, but not in the model. You must add it to the model or remove it from the fields_info.")
            
    def validate(self):
        list_of_fields_to_validate = [
            self.get_required_fields_info(), 
            self.get_optional_fields_info()
            ]
        
        try:
            for list_of_fields in list_of_fields_to_validate:
                self.validate_fields_info(list_of_fields)
                
            self.validate_if_every_field_of_the_model_has_been_defined()
            self.validate_if_every_defined_field_is_present_in_the_model()
        except Exception as e:
            print('Error validating fields info: ', e)
            
    
    def build_valid_data_with_only_required_fields(self):
        """
        Given that YOU defined the required fields, this function will build a dictionary with 
        only the required fields and their types.
        """
        required_fields_info = self.get_required_fields_info()

        valid_data_with_only_required_fields = {}
        
        for field, type in required_fields_info.items():
            data_to_replace = self.DUMMY_TEST_DATA[type]
            valid_data_with_only_required_fields[field] = data_to_replace
            
        return valid_data_with_only_required_fields
    
    def build_valid_data_with_all_fields(self):
        required_fields_info = self.get_required_fields_info()
        optional_fields_info = self.get_optional_fields_info()
        
        all_fields = {**required_fields_info, **optional_fields_info}
        
        valid_data_with_all_fields = {}
        
        for field, type in all_fields.items():
            data_to_replace = self.DUMMY_TEST_DATA[type]
            valid_data_with_all_fields[field] = data_to_replace
            
        return valid_data_with_all_fields
                       
    def test_create_with_all_fields_does_not_raise_error(self):
        """
        Test creation with all fields.
        """
        self.validate()
        
        valid_data_with_all_fields = self.build_valid_data_with_all_fields()
        
        Model_Class = self.get_model()
        model = Model_Class(**valid_data_with_all_fields)
        
        for field, value in valid_data_with_all_fields.items():
            assert getattr(model, field) == value
            
    def test_create_without_a_required_field(self):
        """Test creation without a required field."""
        self.validate()
        required_fields = self.build_valid_data_with_only_required_fields()
        valid_data_with_all_fields = self.build_valid_data_with_all_fields()
        
        Model_Class = self.get_model()
        
        # creating a model instance with all fields
        model = Model_Class(**valid_data_with_all_fields)
        
        # dumping the model with all fields to a dictionary
        data_model = model.model_dump()
        
        # removing all fields that are required and checking if the model raises a ValidationError
        for required_field in required_fields.keys():
            data_copy = data_model.copy()
            data_copy.pop(required_field)
            
            # asserting that the model raises a ValidationError
            with pytest.raises(ValidationError):
                print('--------------------------------')
                print('MODEL {__name__} WILL ALL FIELDS: ', data_model)
                print('REMOVE FIELD: ', required_field)
                print('MODEL {__name__} WITHOUT FIELD: ', data_copy)
                print('--------------------------------')
                Model_Class.model_validate(data_copy)
            
            
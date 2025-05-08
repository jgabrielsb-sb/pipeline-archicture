import pytest

from packag.modules.pipeline.tasks import FormatDataTask

from packag.modules.pipeline.utils.exceptions import ValidationError

from unittest.mock import MagicMock

from pydantic import BaseModel

from packag.modules.pipeline.utils.exceptions import TaskError

from packag.modules.pipeline.operation import Operation

from packag.models import dtoFile

from pathlib import Path

class TestFormatDataTask:
    #
    def test_if_private_validate_operation_cls_raise_type_error_when_operation_cls_is_not_an_operation(self):
        with pytest.raises(TypeError):
            FormatDataTask(operation_cls=None)._validate_operation_cls(operation_cls=None)
            
  
    def test_if_private_validate_input_raise_type_error_when_input_is_not_a_dict(self):
        with pytest.raises(TypeError):
            FormatDataTask(operation_cls=None)._validate_input(input_data=None)
        
    
    def test_if_private_validate_input_raise_type_error_when_it_is_not_a_dict_and_is_not_none(self):
        with pytest.raises(TypeError):
            FormatDataTask(operation_cls=None)._validate_input(input_data=str)
        
    
    def test_if_private_validate_input_return_the_input_when_it_is_a_dict(self):
        
        dummy_dict = {
            'key1': 'value1',
            'key2': 'value2'
        }
        
        input_data = dummy_dict
        assert FormatDataTask(operation_cls=None)._validate_input(input_data=input_data) == input_data

    #
    def test_if_private_validate_output_raise_type_error_when_output_is_not_a_dict(self):
        with pytest.raises(TypeError):
            FormatDataTask(operation_cls=None)._validate_output(output_data=None)
            
    def test_if_private_validate_output_raise_type_error_when_output_is_not_a_dict_and_is_not_none(self):
        with pytest.raises(TypeError):
            FormatDataTask(operation_cls=None)._validate_output(output_data=str)
            
    def test_if_private_validate_output_return_the_output_when_it_is_a_dict(self):
        
        dummy_dict = {
            'key1': 'value1',
            'key2': 'value2'
        }
        
        output_data = dummy_dict
        assert FormatDataTask(operation_cls=None)._validate_output(output_data=output_data) == output_data
            
    def test_if_private_validate_operation_cls_raise_type_error_when_operation_cls_is_not_an_operation_instance(self):
        with pytest.raises(TypeError):
            operation = str
            FormatDataTask(operation_cls=operation)._validate_operation_cls(operation_cls=operation)
            
    #
    def test_if_validate_operation_cls_return_the_operation_when_it_is_valid(self):
        class MockOperation(MagicMock, Operation):
            def run(self, input_data=None):
                return None
            
        operation = MockOperation()
        assert FormatDataTask(operation_cls=operation).validate_operation_cls(operation_cls=operation) == operation
            
    def test_if_validate_operation_cls_raise_validation_error_when_operation_cls_is_not_an_operation_instance(self):
        with pytest.raises(ValidationError):
            FormatDataTask(operation_cls=None).validate_operation_cls(operation_cls=None)
    
    def test_if_validate_input_raise_validation_error_when_input_is_not_a_dict(self):
        with pytest.raises(ValidationError):
            FormatDataTask(operation_cls=None).validate_input(input_data=str)
        
    def test_if_validate_output_raise_validation_error_when_output_is_not_a_dict(self):
        with pytest.raises(ValidationError):
            FormatDataTask(operation_cls=None).validate_output(output_data=None)
        
    



import pytest
from unittest.mock import MagicMock
from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    MissingColumnsError,
    OperationError
)

from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage,
    MissingColumnsErrorMessage,
    OperationErrorMessage,
)

from packag.modules.pipeline.operations.formatters.baseFormatter import BaseFormatter

class DummyFormatter(BaseFormatter):
    def _perform_operation(self, input_data: dict) -> dict:
        return input_data
    
@pytest.fixture
def mock_validation_error_message():
    return ValidationErrorMessage(
        function_name='test_function',
        input_name='test_input',
        received_type='test_received_type',
        expected_type='test_expected_type'
    )
    
@pytest.fixture
def mock_missing_columns_error_message():
    return MissingColumnsErrorMessage(
        function_name='test_function',
        input_name='test_input',
        missing_columns=['test_missing_column_1', 'test_missing_column_2'],
    )
    
@pytest.fixture
def mock_operation_error_message():
    return OperationErrorMessage(
        operation_name='test_operation',
        original_exception=ValueError('Test')
    )

#### TEST IF BASE FORMATTER RAISES VALIDATION ERROR WHEN COLUMNS IS NOT A LIST ####
def test_if_base_formatter_raises_validation_error_when_columns_is_not_a_list():
    with pytest.raises(ValidationError):
        DummyFormatter(columns=1)
            
#### TEST IF BASE FORMATTER RAISES VALIDATION ERROR WHEN COLUMNS IS NOT A LIST OF STRINGS ####
def test_if_base_formatter_raises_validation_error_when_columns_is_not_a_list_of_strings():
    with pytest.raises(ValidationError):
        DummyFormatter(columns=['column_1', 1])
        
#### TEST IF VALIDATE INPUT DATA TYPE RAISES VALIDATION ERROR WHEN INPUT DATA IS NOT A DICTIONARY ####
def test_if_validate_input_data_raises_validation_error_when_input_data_is_not_a_dictionary():
    with pytest.raises(ValidationError):
        DummyFormatter(columns=['column_1', 'column_2']).validate_input_data_type(input_data=1)
             
#### TEST IF VALIDATE INPUT DATA COLUMNS RAISES MISSING COLUMNS ERROR WHEN INPUT DATA IS MISSING COLUMNS ####
def test_if_validate_input_data_columns_raises_missing_columns_error_when_input_data_is_missing_columns():
    with pytest.raises(MissingColumnsError):
        DummyFormatter(columns=['column_1', 'column_2']).validate_input_data_columns(input_data={'column_1': 'value_1'})
        
#### TEST IF VALIDATE INPUT DATA COLUMNS RETURNS INPUT DATA WHEN INPUT DATA IS VALID ####
def test_if_validate_input_data_columns_returns_input_data_when_input_data_is_valid():
    assert DummyFormatter(columns=['column_1', 'column_2']).validate_input_data_columns(input_data={'column_1': 'value_1', 'column_2': 'value_2'}) == {'column_1': 'value_1', 'column_2': 'value_2'}
        
def test_if_validate_output_data_raises_validation_error_when_output_data_is_not_a_dictionary():
    with pytest.raises(ValidationError):
        DummyFormatter(columns=['column_1', 'column_2']).validate_output_data(output_data=1)
        
#### TEST IF RUN RAISES OPERATION ERROR WHEN VALIDATE INPUT DATA TYPE RAISES VALIDATION ERROR ####
def test_if_run_raises_operation_error_when_validate_input_data_type_raises_validation_error(
    mock_validation_error_message: ValidationErrorMessage
):
    DummyFormatter.validate_input_data_type.side_effect = ValidationError(
        mock_validation_error_message
        )
    
    dummy_formatter = DummyFormatter(columns=['column_1', 'column_2'])
    
    with pytest.raises(OperationError):
        dummy_formatter.run(input_data=1)
        
#### TEST IF RUN RAISES OPERATION ERROR WHEN VALIDATE INPUT DATA COLUMNS RAISES MISSING COLUMNS ERROR ####
def test_if_run_raises_operation_error_when_validate_input_data_columns_raises_missing_columns_error(
    mock_missing_columns_error_message: MissingColumnsErrorMessage
):
    DummyFormatter.validate_input_data_columns.side_effect = MissingColumnsError(
        mock_missing_columns_error_message
    )
    dummy_formatter = DummyFormatter(columns=['column_1', 'column_2'])
    
    with pytest.raises(OperationError):
        dummy_formatter.run(input_data={'column_1': 'value_1'})
        
#### TEST IF RUN RAISES OPERATION ERROR WHEN PERFORM OPERATION RAISES OPERATION ERROR ####
def test_if_run_raises_operation_error_when_perform_operation_raises_operation_error(
    mock_operation_error_message: OperationErrorMessage
):
    DummyFormatter._perform_operation.side_effect = OperationError(
        mock_operation_error_message
        )
    
    dummy_formatter = DummyFormatter(columns=['column_1', 'column_2'])
    
    with pytest.raises(OperationError):
        dummy_formatter.run(input_data={'column_1': 'value_1'})
        
#### TEST IF RUN RAISES OPERATION ERROR WHEN VALIDATE OUTPUT DATA TYPE RAISES VALIDATION ERROR ####
def test_if_run_raises_operation_error_when_validate_output_data_type_raises_validation_error(
    mock_validation_error_message: ValidationErrorMessage
):
    DummyFormatter.validate_output_data.side_effect = ValidationError(mock_validation_error_message)
    dummy_formatter = DummyFormatter(columns=['column_1', 'column_2'])
    
    with pytest.raises(OperationError):
        dummy_formatter.run(input_data={'column_1': 'value_1'})
        
#### TEST IF RUN RETURNS OUTPUT DATA WHEN EVERYTHING IS VALID ####
def test_if_run_returns_output_data_when_everything_is_valid():
    dummy_formatter = DummyFormatter(columns=['column_1', 'column_2'])
    
    assert dummy_formatter.run(input_data={'column_1': 'value_1', 'column_2': 'value_2'}) == {'column_1': 'value_1', 'column_2': 'value_2'}
        
        
        
        
        
        
        
        
        
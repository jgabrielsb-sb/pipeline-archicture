
from packag.modules.utils import get_logger

from ...operation import Operation

from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    MissingColumnsError,
    OperationError
)

from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage,
    MissingColumnsErrorMessage,
    OperationErrorMessage
)


from abc import abstractmethod, ABC


operation_logger = get_logger('operations')

class BaseFormatter(Operation, ABC):
    """
    Base class for all formatters.
    
    A formatter is an operation that receives, on initialization, a list of columns   
    that will be formatted.
    
    On the run method, it must receive an input_data that is a dictionary with the columns as keys and the values to be 
    formatted as values.
    
    The confront_input_data_with_columns method is used to confront the input_data with the columns received 
    on initialization.
    If the input_data does not have all the columns received on initialization, a ValidationError is raised.
    
    The _perform_operation method is used to perform the operation.
    
    
    """
    def __init__(self, columns: list[str]):
        # must be a list and must be a list of strings
        if isinstance(columns, list) and all(isinstance(column, str) for column in columns):
            self.columns = columns
        else:
            message = ValidationErrorMessage(
                function_name='__init__',
                input_name='columns',
                received_type=str(type(columns)),
                expected_type=str(list[str])
            )
            
            operation_logger.error(message.get_message())
            
            raise ValidationError(message)
        
        
    def validate_input_data_type(self, input_data: dict) -> dict:
        """
        For Formatters, the input_data must be a dictionary with string values.
        Then, you don't need to implement the validation of the input_data when inheriting from this class.
        """
        if not isinstance(input_data, dict):
            pass  
        else:
            return input_data

        message = ValidationErrorMessage(
            function_name='validate_input_data',
            input_name='input_data',
            received_type=str(type(input_data)),
            expected_type=str(dict[str, str])
        )
        operation_logger.error(message.get_message())
        raise ValidationError(message)

        
    def validate_output_data(self, output_data: dict) -> dict:
        """
        For Formatters, the output_data must be a dictionary with string values.
        Then, you don't need to implement the validation of the output_data when inheriting from this class.
        """
        if not isinstance(output_data, dict):
            pass  
        else:
            return output_data

        message = ValidationErrorMessage(
            function_name='validate_output_data',
            input_name='output_data',
            received_type=str(type(output_data)),
            expected_type=str(dict)
        )
        operation_logger.error(message.get_message())
        raise ValidationError(message)
    
    def validate_input_data_columns(self, input_data: dict) -> dict:
        """
        Confront the input_data with the columns received on initialization.
        If the input_data does not have all the columns received on initialization, a ValidationError is raised.
        """
        if not all(column in input_data.keys() for column in self.columns):
            missing_columns = list(set(self.columns) - set(input_data.keys()))
            
            message = MissingColumnsErrorMessage(
                function_name='validate_input_data_columns',
                input_name='input_data',
                missing_columns=missing_columns,
            )
            
            operation_logger.error(message.get_message())
            
            raise MissingColumnsError(message)
        
        return input_data
    
    @abstractmethod
    def _perform_operation(self, input_data: dict[str, str]) -> dict[str, str]: # pragma: no cover
        pass
        
    
    def run(self, input_data: dict[str, str]) -> dict[str, str]:
        try:
            input_data = self.validate_input_data_type(input_data)
            input_data = self.validate_input_data_columns(input_data)
            
            output_data = self._perform_operation(input_data)
            
            output_data = self.validate_output_data(output_data)
            
            return output_data
            
        except (
            ValidationError,
            MissingColumnsError,
            OperationError,
        ) as e:
            message = OperationErrorMessage(
                operation_name=self.__class__.__name__,
                original_exception=e,
            )
            
            operation_logger.error(message.get_message())
            
            raise OperationError(message)
        
        
    
   

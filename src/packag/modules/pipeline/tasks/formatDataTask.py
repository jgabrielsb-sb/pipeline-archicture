from packag.modules.pipeline.task import Task

from ..operation import Operation

from typing import Type

from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    OperationError,
    TaskError,
    TaskErrorMessage
)

from packag.modules.utils import get_logger

logger = get_logger('tasks')

class FormatDataTask(Task):
    """
    Format data from a file.
    
    This task expects to receive a dict object as a input;
    Then, it uses the operation instance, which has to be an instance of Operation, to format the data.
    The output is a dict object.
    """
    
    def _validate_operation_cls(self, operation_cls: Operation):
        if not isinstance(operation_cls, Operation):
            raise TypeError(f"Expected an Operation instance, got {type(operation_cls)} instead")

        return operation_cls
    
    def _validate_input(self, input_data: dict):
        if not isinstance(input_data, dict):
            raise TypeError(f"Expected a {type(dict)} type, got {type(input_data)} instead")
        return input_data
    
    def _validate_output(self, output_data: dict):
        if not isinstance(output_data, dict):
            raise TypeError(f"Expected a {type(dict)} type, got {type(output_data)} instead")
        
        return output_data
    
    def run(self, input_data: dict) -> dict:
        """
        Run the task by:
            * Validating the input data.
            * Using the operation instance to execute the task by running the operation run method
            * Validating the output data.
            * Returning the output data if it is valid.
        """
        try:
            operation = self.validate_operation_cls(self.operation_cls)
            input_data = self.validate_input(input_data)
            
            output_data = operation.run(input_data)
            
            output_data = self.validate_output(output_data)
            return output_data
        
        except (ValidationError, OperationError) as e:
            message = TaskErrorMessage(
                task_name=self.__class__.__name__,
                original_exception=e
            )
            
            logger.error(message.get_message())
            
            raise TaskError(message=message)
    
    
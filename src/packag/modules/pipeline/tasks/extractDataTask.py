from packag.modules.pipeline.task import Task

from ..operation import Operation

from packag.models import dtoFile

from typing import Type

import pydantic

from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    OperationError,
    TaskError,
    TaskErrorMessage
)

from packag.modules.utils import get_logger

logger = get_logger('tasks')

class ExtractDataTask(Task):
    """
    Extract data from a file.
    
    This task expects to receive a File.File Object as a input;
    Then, it uses the operation instance, which has to be an instance of Operation, to extract the data from the file.
    The output is a dtoData object.
    """
    
    def _validate_operation_cls(self, operation_cls: Operation):
        if not isinstance(operation_cls, Operation):
            raise TypeError(f"Expected an Operation instance, got {type(operation_cls)} instead")

        return operation_cls
    
    def _validate_input(self, input_data: dtoFile.File):
        if not isinstance(input_data, dtoFile.File):
            raise TypeError(f"Expected a {type(dtoFile.File)} type, got {type(input_data)} instead")
        return input_data
    
    def _validate_output(self, output_data: pydantic.BaseModel):
        if not isinstance(output_data, pydantic.BaseModel):
            raise TypeError(f"Expected a pydantic.BaseModel type, got {type(output_data)} instead")
        
        return output_data
    
    def run(self, input_data: dtoFile.File) -> pydantic.BaseModel:
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
    
    
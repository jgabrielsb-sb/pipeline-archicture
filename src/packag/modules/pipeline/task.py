from abc import ABC, abstractmethod
from typing import Any, Type

from packag.modules.pipeline.utils.exceptions import (
    TaskError, 
    ValidationError,
    OperationError
)

from packag.modules.pipeline.operation import Operation

from packag.modules.utils.logger import get_logger
from packag.modules.utils import (
    ValidationErrorMessage, 
    TaskErrorMessage
)

logger = get_logger('task_logger')

"""
What is a Task?

A task is a unit of work that can be executed by a pipeline.
    * A task have a run method that compiles the execution of the task.
    * A task must define what it expects as input and what it expects as output.
    * A task must receive on init the class of the operation that will be executed (the operation class contains the business logic of the task).
    
Then, to create a new generic task, you must:
    * Inherit from Task class.
    * Implement the init me
    * Implement the validate_input method by raising a TaskError if the input is not valid.
    * Implement the validate_output method by raising a TaskError if the output is not valid.
"""


class Task(ABC):
    """
    Abstract base class for all tasks.
    """
    
    def __init__(self, operation_cls: Type[Operation]):
        self.operation_cls = operation_cls
        
    @abstractmethod
    def _validate_operation_cls(self, operation_cls: Type[Any]): # pragma: no cover
        """
        Validate the class of the operation that will be executed.
        Define, for each task, what is the type of the operation that will be executed.
        It must:
            * Raise a ValidationError if the class is not what is expected.
            * Return the class if it is valid.
        """
        pass
    
    @abstractmethod
    def _validate_input(self, input_data): # pragma: no cover
        """
        Subclass must implement this method.
        Validate the input data of the task.
        It must:
            * Raise a ValidationError if the input is not valid.
            * Return the input data if it is valid.
        """
        pass
    
    @abstractmethod
    def _validate_output(self, output_data): # pragma: no cover
        """
        Subclass must implement this method.
        Validate the output data of the task.
        It must:
            * Raise a ValidationError if the output is not valid.
            * Return the output data if it is valid.
        """
        pass
    
    def validate_operation_cls(self, operation_cls: Type[Operation]):
        try:
            return self._validate_operation_cls(operation_cls)
        except TypeError as e:
            
            message = ValidationErrorMessage(
                function_name='validate_operation_cls',
                input_name='operation_cls',
                received_type=str(type(operation_cls)),
            )
            
            logger.error(message.get_message())
            
            raise ValidationError(message=message) 
        
    def validate_input(self, input_data):
        try:
            return self._validate_input(input_data)
        except TypeError as e:
            message = ValidationErrorMessage(
                function_name='validate_input',
                input_name='input_data',
                received_type=str(type(input_data))
            )
            
            logger.error(message.get_message())
            
            raise ValidationError(message=message) 
    
    def validate_output(self, output_data):
        try:
            result = self._validate_output(output_data)
            return result
        except TypeError as e:
            message = ValidationErrorMessage(
                function_name='validate_output',
                input_name='output_data',
                received_type=str(type(output_data)),
            )
            
            logger.error(message.get_message())
            
            raise ValidationError(message=message)
    
    
    def run(self, input_data):
        """
        Run the task by:
            * Validating the input data.
            * Using the operation class to execute the task by running the operation run method (the class is already validated)
            * Validating the output data.
            * Returning the output data if it is valid.
        """
        try:
            operation_cls = self.validate_operation_cls(self.operation_cls)
            input_data = self.validate_input(input_data)
            
            instance = operation_cls()
            output_data = instance.run(input_data)
            
            output_data = self.validate_output(output_data)
            return output_data
        
        except (ValidationError, OperationError) as e:
            
            message = TaskErrorMessage(
                task_name=self.__class__.__name__,
                original_exception=e
            )
            
            logger.error(message.get_message())
            
            raise TaskError(message=message)
        
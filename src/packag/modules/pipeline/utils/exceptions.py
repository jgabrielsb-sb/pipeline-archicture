"""
We should think about exceptions as a way to concantenate,
to compile error logic from units of work.
"""

from packag.modules.utils.messages import (
    ValidationErrorMessages, 
    TaskErrorMessage,
    OperationErrorMessage,
)

class PipelineError(Exception):
    """
    Raised when a pipeline execution fails.

    Example message:
        "Error running pipeline MyPipeline: Something went wrong."
    """
    def __init__(self, message, pipeline_name, original_exception=None):
        self.message = message
        self.pipeline_name = pipeline_name
        self.original_exception = original_exception
        
        full_message = f"Error running pipeline '{pipeline_name}': {message}"
        super().__init__(full_message)


class TaskError(Exception):
    """
    Raised when a task execution fails.

    Example message:
        "[Task: MyTask] Something went wrong."
    """
    def __init__(self, message: TaskErrorMessage, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        
        super().__init__(message.get_message())


class OperationError(Exception):
    """
    Raised when an operation execution fails.

    Example message:
        "[Operation: MyOperation] Something went wrong."
    """
    def __init__(self, message: OperationErrorMessage, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        
        super().__init__(message.get_message())


class ValidationError(Exception):
    """
    Raised when an input validation fails.

    Example message:
        "Error validating 'field_name': must be a positive integer."
    """
    def __init__(self, message: ValidationErrorMessages):
        self.message = message
        
        if not isinstance(message, ValidationErrorMessages):
            raise ValueError("message must be an instance of ValidationErrorMessages")
        
        self.message = message.get_message()
        super().__init__(self.message)

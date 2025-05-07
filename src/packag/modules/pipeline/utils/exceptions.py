"""
We should think about exceptions as a way to concantenate,
to compile error logic from units of work.
"""

from packag.modules.pipeline.utils.messages import *


class PipelineError(Exception):
    """
    Raised when a pipeline execution fails.

    Example message:
        "Error running pipeline MyPipeline: Something went wrong."
    """
    def __init__(self, message: PipelineErrorMessage):
        self.message = message
        
        
        if not isinstance(message, PipelineErrorMessage):
            raise TypeError("message must be an instance of PipelineErrorMessage")
        
        super().__init__(message.get_message())


class TaskError(Exception):
    """
    Raised when a task execution fails.

    Example message:
        "[Task: MyTask] Something went wrong."
    """
    def __init__(self, message: TaskErrorMessage):
        self.message = message
        
        
        if not isinstance(message, TaskErrorMessage):
            raise TypeError("message must be an instance of TaskErrorMessage")
        
        
        super().__init__(message.get_message())


class OperationError(Exception):
    """
    Raised when an operation execution fails.

    Example message:
        "[Operation: MyOperation] Something went wrong."
    """
    def __init__(self, message: OperationErrorMessage):
        self.message = message
        
        if not isinstance(message, OperationErrorMessage):
            raise TypeError("message must be an instance of OperationErrorMessage")
        
        super().__init__(message.get_message())


class ValidationError(Exception):
    """
    Raised when an input validation fails.

    Example message:
        "Error validating 'field_name': must be a positive integer."
    """
    def __init__(self, message: ValidationErrorMessage):
        self.message = message
        
        if not isinstance(message, ValidationErrorMessage):
            raise TypeError("message must be an instance of ValidationErrorMessage")
        
        super().__init__(message.get_message())
        
        
class ExtractMethodError(Exception):
    """
    Exception raised when an extract method fails.
    """
    def __init__(self, message: ExtractMethodErrorMessage):
        self.message = message
        
        if not isinstance(message, ExtractMethodErrorMessage):
            raise TypeError("message must be an instance of ExtractMethodErrorMessage")
        
        super().__init__(message.get_message())
        
class GetAllExtractedInfoError(Exception):
    """
    Exception raised when an error occurs while getting all extracted info.
    """
    def __init__(self, message: GetAllExtractedInfoErrorMessage):
        self.message = message
        
        if not isinstance(message, GetAllExtractedInfoErrorMessage):
            raise TypeError("message must be an instance of GetAllExtractedInfoErrorMessage")
        
        super().__init__(message.get_message())
        



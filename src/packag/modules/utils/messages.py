class PipelineErrorMessage:
    def __init__(self, pipeline_name: str, original_exception: Exception):
        self.pipeline_name = pipeline_name
        self.original_exception = original_exception
        
        if not isinstance(pipeline_name, str):
            raise ValueError("pipeline_name must be a string")
        
        if not isinstance(original_exception, Exception):
            raise ValueError("original_exception must be an instance of Exception")
        
    def get_message(self):
        return f"""Error running pipeline {self.pipeline_name} -
        {self.original_exception}
        """
        

class TaskErrorMessage:
    def __init__(self, task_name: str, original_exception: Exception):
        self.task_name = task_name
        self.original_exception = original_exception
        
        if not isinstance(task_name, str):
            raise ValueError("task_name must be a string")
        
        if not isinstance(original_exception, Exception):
            raise ValueError("original_exception must be an instance of Exception")
        
    def get_message(self):
        return f"""Error running task {self.task_name} -
        {self.original_exception}
        """
        
class OperationErrorMessage:
    def __init__(self, operation_name: str, original_exception: Exception):
        self.operation_name = operation_name
        self.original_exception = original_exception
        
        if not isinstance(operation_name, str):
            raise ValueError("operation_name must be a string")
        
        if not isinstance(original_exception, Exception):
            raise ValueError("original_exception must be an instance of Exception")
        
    def get_message(self):
        return f"""Error running operation {self.operation_name} -
        {self.original_exception}
        """
        
class ValidationErrorMessage:
    def __init__(self, 
                 function_name: str, 
                 input_name: str, 
                 received_type: str, 
                 expected_type: str=None
                 ):
        self.function_name = function_name
        self.input_name = input_name
        self.received_type = received_type
        self.expected_type = expected_type
        
        if not isinstance(function_name, str):
            raise ValueError("function_name must be a string")
        
        if not isinstance(input_name, str):
            raise ValueError("input_name must be a string")
        
        if not isinstance(received_type, str):
            raise ValueError("received_type must be a string")
        
        if expected_type: 
            if not isinstance(expected_type, str):
                raise ValueError("expected_type must be a string")
        
    def get_message(self):
        if self.expected_type:
            return f""" Error validating {self.input_name} on function {self.function_name} - the received type is not allowed: {self.received_type} 
            Expected type: {self.expected_type}
            """
        else:
            return f""" Error validating {self.input_name} on function {self.function_name} - the received type is not allowed: {self.received_type} 
            """
        
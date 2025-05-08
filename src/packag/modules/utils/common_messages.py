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

class ExtractMethodErrorMessage:
    def __init__(self, method_name: str, original_exception: Exception):
        self.method_name = method_name
        self.original_exception = original_exception
        
        if not isinstance(method_name, str):
            raise ValueError("method_name must be a string")
        
        if not isinstance(original_exception, Exception):
            raise ValueError("original_exception must be an instance of Exception")
        
    def get_message(self):
        return f"Error on extract method {self.method_name} -\n{self.original_exception}"

class GetAllExtractedInfoErrorMessage:
    def __init__(self, exceptions: list[Exception]):
        if not isinstance(exceptions, list):
            raise ValueError("exceptions must be a list")
        
        for exception in exceptions:
            try:
                exception.get_message()
            except:
                raise ValueError("exceptions must have a get_message method. You should pass a list of ExtractMethodError")
        
        self.exceptions = exceptions
        
    def get_message(self):
        error_messages = '\n'.join([e.get_message() for e in self.exceptions])
        return f"Error on the following extracting methods:\n{error_messages}"

class MissingColumnsErrorMessage:
    def __init__(self, 
                 function_name: str, 
                 input_name: str,
                 missing_columns: list[str],
                 ):
        for argument in [function_name, input_name]:
            if not isinstance(argument, str):
                raise ValueError("function_name and input_name must be strings")
        
        if not isinstance(missing_columns, list):
            raise ValueError("missing_columns must be a list")
        
        if not all(isinstance(column, str) for column in missing_columns):
            raise ValueError("missing_columns must be a list of strings")
        
        self.function_name = function_name
        self.input_name = input_name
        self.missing_columns = missing_columns
        
    def get_message(self):
        return f"MissingColumnsError on function {self.function_name}: The following columns are missing: {str(self.missing_columns)} on the input {self.input_name}" 
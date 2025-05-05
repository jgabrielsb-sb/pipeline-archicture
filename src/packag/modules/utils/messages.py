class PipelineErrorMessage:
    def __init__(self, pipeline_name, original_exception):
        self.pipeline_name = pipeline_name
        self.original_exception = original_exception
        
    def get_message(self):
        return f"""Error running pipeline {self.pipeline_name} -
        {self.original_exception}
        """
        

class TaskErrorMessage:
    def __init__(self, task_name, original_exception):
        self.task_name = task_name
        self.original_exception = original_exception
        
    def get_message(self):
        return f"""Error running task {self.task_name} -
        {self.original_exception}
        """
        
class OperationErrorMessage:
    def __init__(self, operation_name, original_exception):
        self.operation_name = operation_name
        self.original_exception = original_exception
        
    def get_message(self):
        return f"""Error running operation {self.operation_name} -
        {self.original_exception}
        """
        
class ValidationErrorMessages:
    def __init__(self, function_name, input_name, received_type, expected_type=None):
        self.function_name = function_name
        self.input_name = input_name
        self.received_type = received_type
        self.expected_type = expected_type
        
    def get_message(self):
        if self.expected_type:
            return f""" Error validating {self.input_name} on function {self.function_name} - the received type is not allowed: {self.received_type} 
            Expected type: {self.expected_type}
            """
        else:
            return f""" Error validating {self.input_name} on function {self.function_name} - the received type is not allowed: {self.received_type} 
            """
        
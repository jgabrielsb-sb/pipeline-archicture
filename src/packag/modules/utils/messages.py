class ValidationErrorMessages:
    def __init__(self, function_name, input_name, received_type):
        self.function_name = function_name
        self.input_name = input_name
        self.received_type = received_type
        
    def get_message(self):
        return f""" Error validating {self.input_name} on function {self.function_name} - the received type is not allowed: {self.received_type} 
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
        
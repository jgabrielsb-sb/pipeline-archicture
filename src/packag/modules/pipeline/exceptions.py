class PipelineError(Exception):
    def __init__(self, message, pipeline_name, original_exception=None):
        self.message = message
        self.pipeline_name = pipeline_name
        self.original_exception = original_exception
        
        full_message = f"[Pipeline: {pipeline_name}] {message}"
        super().__init__(full_message, pipeline_name, original_exception)

class TaskError(PipelineError):
    def __init__(self, message, task_name, original_exception=None):
        self.message = message
        self.task_name = task_name
        self.original_exception = original_exception
        
        full_message = f"[Task: {task_name}] {message}"
        super().__init__(full_message, task_name, original_exception)
        

class OperationError(PipelineError):
    def __init__(self, message, operation_name, original_exception=None):
        self.message = message
        self.operation_name = operation_name
        self.original_exception = original_exception
        
        full_message = f"[Operation: {operation_name}] {message}"
        super().__init__(full_message, operation_name, original_exception)


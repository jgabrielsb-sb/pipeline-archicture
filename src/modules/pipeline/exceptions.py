class PipelineError(Exception):
    def __init__(self, message, pipeline_name, original_exception=None):
        self.pipeline_name = pipeline_name
        self.original_exception = original_exception
        
        full_message = f"[Pipeline: {pipeline_name}] {message}"
        super().__init__(full_message)

class TaskError(PipelineError):
    def __init__(self, message, task_name, original_exception=None):
        self.task_name = task_name
        self.original_exception = original_exception
        
        full_message = f"[Task: {task_name}] {message}"
        super().__init__(full_message)
        

class OperationError(PipelineError):
    def __init__(self, message, operation_name, original_exception=None):
        self.operation_name = operation_name
        self.original_exception = original_exception
        
        full_message = f"[Operation: {operation_name}] {message}"
        super().__init__(full_message)


from packag.modules.pipeline.utils.exceptions import *
import pytest


#### TEST IF PIPELINE ERROR RAISES VALIDATION ERROR WHEN MESSAGE IS NOT A INSTANCE OF PIPELINE ERROR MESSAGE ######
def test_if_pipeline_error_raises_validation_error_when_message_is_not_a_instance_of_pipeline_error_message():
    with pytest.raises(TypeError):
        PipelineError(message='message')
        
def test_if_pipeline_error_is_created():
    pipeline_error = PipelineError(
        message=PipelineErrorMessage(
            pipeline_name='pipeline_name', 
            original_exception=Exception('original_exception')
            )
        )

#### TEST IF TASK ERROR RAISES VALIDATION ERROR WHEN MESSAGE IS NOT A INSTANCE OF TASK ERROR MESSAGE ######
def test_if_task_error_raises_validation_error_when_message_is_not_a_instance_of_task_error_message():
    with pytest.raises(TypeError):
        TaskError(message='message')
        
def test_if_task_error_is_created():
    task_error = TaskError(
        message=TaskErrorMessage(
            task_name='task_name', 
            original_exception=Exception('original_exception')
            )
        )   
    
#### TEST IF OPERATION ERROR RAISES VALIDATION ERROR WHEN MESSAGE IS NOT A INSTANCE OF OPERATION ERROR MESSAGE ######
def test_if_operation_error_raises_validation_error_when_message_is_not_a_instance_of_operation_error_message():
    with pytest.raises(TypeError):
        OperationError(message='message')
        
def test_if_operation_error_is_created():
    operation_error = OperationError(
        message=OperationErrorMessage(
            operation_name='operation_name', 
            original_exception=Exception('original_exception')
            )
        )
    
#### TEST IF VALIDATION ERROR RAISES VALIDATION ERROR WHEN MESSAGE IS NOT A INSTANCE OF VALIDATION ERROR MESSAGE ######
def test_if_validation_error_raises_validation_error_when_message_is_not_a_instance_of_validation_error_message():
    with pytest.raises(TypeError):
        ValidationError(message='message')
        
def test_if_validation_error_is_created():
    validation_error = ValidationError(
        message=ValidationErrorMessage(
            function_name='function_name', 
            input_name='input_name', 
            received_type=str(str), 
            expected_type=str(int)
            )
        )
    

        
        
        
        
        
        
        
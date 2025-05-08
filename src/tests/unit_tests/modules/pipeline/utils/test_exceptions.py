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
    
#### TEST IF EXTRACT METHOD ERROR RAISES VALIDATION ERROR WHEN MESSAGE IS NOT A INSTANCE OF EXTRACT METHOD ERROR MESSAGE ######
def test_if_extract_method_error_raises_validation_error_when_message_is_not_a_instance_of_extract_method_error_message():
    with pytest.raises(TypeError):
        ExtractMethodError(message='message')
        
def test_if_extract_method_error_is_created():
    extract_method_error = ExtractMethodError(
        message=ExtractMethodErrorMessage(
            method_name='method_name', 
            original_exception=Exception('original_exception')
            )
        )
    
###### TEST IF GET ALL EXTRACTED INFO ERROR RAISES TYPE ERROR IF MESSAGE IS NOT A GETALLEXTRACTEDINFOERRORMESSAGE ######
def test_if_get_all_extracted_info_error_raises_type_error_if_message_is_not_a_get_all_extracted_info_error_message():
    with pytest.raises(TypeError):
        GetAllExtractedInfoError(message='message')
        
def test_if_get_all_extracted_info_error_is_created():
    get_all_extracted_info_error = GetAllExtractedInfoError(
        message=GetAllExtractedInfoErrorMessage(
            exceptions=[ExtractMethodErrorMessage(
                method_name='method_name', 
                original_exception=Exception('original_exception')
            )]
        )
    )
    
def test_if_missing_columns_error_raises_type_error_if_message_is_not_a_missing_columns_error_message():
    with pytest.raises(TypeError):
        MissingColumnsError(message='message')
        
def test_if_missing_columns_error_is_created():
    missing_columns_error = MissingColumnsError(
        message=MissingColumnsErrorMessage(
            function_name='function_name',
            input_name='input_name',
            missing_columns=['column_1', 'column_2']
        )
    )
        
        
        
        
        
        
        
        
        
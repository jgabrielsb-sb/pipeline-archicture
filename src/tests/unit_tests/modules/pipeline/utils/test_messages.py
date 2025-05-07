from packag.modules.pipeline.utils.messages import *

import pytest

def normalize_string(s: str) -> str:
    return '\n'.join(line.rstrip() for line in s.strip().splitlines())


###### TEST IF PIPELINE ERROR MESSAGE RETURNS THE CORRECT MESSAGE ######
def test_if_pipeline_error_message_returns_the_correct_message():
    pipeline_error_message = PipelineErrorMessage(
        pipeline_name='pipeline_name', 
        original_exception=Exception(
            'original_exception'
        )
    )
    assert pipeline_error_message.get_message() == f"""Error running pipeline pipeline_name -
        original_exception
        """

###### TEST IF PIPELINE ERROR MESSAGE RAISES VALUE ERROR WHEN PIPELINE NAME IS NOT A STRING ######
def test_if_pipeline_error_message_raises_value_error_when_pipeline_name_is_not_a_string():
    with pytest.raises(ValueError):
        PipelineErrorMessage(
            pipeline_name=1, 
            original_exception=Exception(
                'original_exception'
            )
        )
        
###### TEST IF PIPELINE ERROR MESSAGE RAISES VALUE ERROR WHEN ORIGINAL EXCEPTION IS NOT A INSTANCE OF EXCEPTION ######
def test_if_pipeline_error_message_raises_value_error_when_original_exception_is_not_a_instance_of_exception():
    with pytest.raises(ValueError):
        PipelineErrorMessage(
            pipeline_name='pipeline_name', 
            original_exception=1)

###### TEST IF TASK ERROR MESSAGE RETURNS THE CORRECT MESSAGE ######
def test_if_task_error_message_returns_the_correct_message():
    task_error_message = TaskErrorMessage(
        task_name='task_name', 
        original_exception=Exception(
            'original_exception'
        )
    )
    assert task_error_message.get_message() == f"""Error running task task_name -
        original_exception
        """

###### TEST IF TASK ERROR MESSAGE RAISES VALUE ERROR WHEN TASK NAME IS NOT A STRING ######
def test_if_task_error_message_raises_value_error_when_task_name_is_not_a_string():
    with pytest.raises(ValueError):
        TaskErrorMessage(
            task_name=1, 
            original_exception=Exception(
                'original_exception'
            )
        )
        
###### TEST IF TASK ERROR MESSAGE RAISES VALUE ERROR WHEN ORIGINAL EXCEPTION IS NOT A INSTANCE OF EXCEPTION ######
def test_if_task_error_message_raises_value_error_when_original_exception_is_not_a_instance_of_exception():
    with pytest.raises(ValueError):
        TaskErrorMessage(
            task_name='task_name', 
            original_exception=1
        )

###### TEST IF OPERATION ERROR MESSAGE RETURNS THE CORRECT MESSAGE ######
def test_if_operation_error_message_returns_the_correct_message():
    operation_error_message = OperationErrorMessage(
        operation_name='operation_name', 
        original_exception=Exception('original_exception')
    )
    assert operation_error_message.get_message() == f"""Error running operation operation_name -
        original_exception
        """

###### TEST IF OPERATION ERROR MESSAGE RAISES VALUE ERROR WHEN OPERATION NAME IS NOT A STRING ######
def test_if_operation_error_message_raises_value_error_when_operation_name_is_not_a_string():
    with pytest.raises(ValueError):
        OperationErrorMessage(
            operation_name=1, 
            original_exception=Exception('original_exception')
        )

###### TEST IF OPERATION ERROR MESSAGE RAISES VALUE ERROR WHEN ORIGINAL EXCEPTION IS NOT A INSTANCE OF EXCEPTION ######
def test_if_operation_error_message_raises_value_error_when_original_exception_is_not_a_instance_of_exception():
    with pytest.raises(ValueError):
        OperationErrorMessage(
            operation_name='operation_name', 
            original_exception=1
        )

###### TEST IF VALIDATION ERROR MESSAGE RETURNS THE CORRECT MESSAGE ######
def test_if_validation_error_message_returns_the_correct_message():
    validation_error_message = ValidationErrorMessage(
        function_name='function_name',
        input_name='input_name',
        received_type='int',
        expected_type='str'
    )
    assert validation_error_message.get_message() == f""" Error validating input_name on function function_name - the received type is not allowed: int 
            Expected type: str
            """

###### TEST IF VALIDATION ERROR MESSAGE RAISES VALUE ERROR WHEN FUNCTION NAME IS NOT A STRING ######
def test_if_validation_error_message_raises_value_error_when_function_name_is_not_a_string():
    with pytest.raises(ValueError):
        ValidationErrorMessage(
            function_name=1,
            input_name='input_name',
            received_type='int',
            expected_type='str'
        )

###### TEST IF VALIDATION ERROR MESSAGE RAISES VALUE ERROR WHEN INPUT NAME IS NOT A STRING ######
def test_if_validation_error_message_raises_value_error_when_input_name_is_not_a_string():
    with pytest.raises(ValueError):
        ValidationErrorMessage(
            function_name='function_name',
            input_name=1,
            received_type='int',
            expected_type='str'
        )

###### TEST IF VALIDATION ERROR MESSAGE RAISES VALUE ERROR WHEN RECEIVED TYPE IS NOT A STRING ######
def test_if_validation_error_message_raises_value_error_when_received_type_is_not_a_string():
    with pytest.raises(ValueError):
        ValidationErrorMessage(
            function_name='function_name',
            input_name='input_name',
            received_type=1,
            expected_type='str'
        )

###### TEST IF VALIDATION ERROR MESSAGE RAISES VALUE ERROR WHEN EXPECTED TYPE IS NOT A STRING ######
def test_if_validation_error_message_raises_value_error_when_expected_type_is_not_a_string():
    with pytest.raises(ValueError):
        ValidationErrorMessage(
            function_name='function_name',
            input_name='input_name',
            received_type='int',
            expected_type=1
        )
        
###### TEST IF VALIDATION ERROR MESSAGE RAISES VALUE ERROR WHEN EXPECTED TYPE IS NOT PROVIDED ######
def test_if_validation_error_message_raises_value_error_when_expected_type_is_not_provided():
    validation_error_message = ValidationErrorMessage(
        function_name='function_name',
        input_name='input_name',
        received_type='int',
    )
    
    assert validation_error_message.get_message() == f""" Error validating input_name on function function_name - the received type is not allowed: int 
            """

###### TEST IF EXTRACT METHOD ERROR MESSAGE RETURNS THE CORRECT MESSAGE ######
def test_if_extract_method_error_message_returns_the_correct_message():
    extract_method_error_message = ExtractMethodErrorMessage(
        method_name='method_name', 
        original_exception=Exception('original_exception')
    )
    assert extract_method_error_message.get_message() == f"Error on extract method method_name -\noriginal_exception"

###### TEST IF EXTRACT METHOD ERROR MESSAGE RAISES VALUE ERROR WHEN METHOD NAME IS NOT A STRING ######
def test_if_extract_method_error_message_raises_value_error_when_method_name_is_not_a_string():
    with pytest.raises(ValueError):
        ExtractMethodErrorMessage(
            method_name=1, 
            original_exception=Exception('original_exception')
        )

###### TEST IF EXTRACT METHOD ERROR MESSAGE RAISES VALUE ERROR WHEN ORIGINAL EXCEPTION IS NOT A INSTANCE OF EXCEPTION ######
def test_if_extract_method_error_message_raises_value_error_when_original_exception_is_not_a_instance_of_exception():
    with pytest.raises(ValueError):
        ExtractMethodErrorMessage(
            method_name='method_name', 
            original_exception=1
        )
        
###### TEST IF GET ALL EXTRACTED INFO ERROR MESSAGE RAISES VALUE ERROR WHEN EXCEPTIONS IS NOT A LIST ######
def test_if_get_all_extracted_info_error_message_raises_value_error_when_exceptions_is_not_a_list():
    with pytest.raises(ValueError):
        GetAllExtractedInfoErrorMessage(
            exceptions=1
        )
        
###### TEST IF GET ALL EXTRACTED INFO ERROR MESSAGE RAISES VALUE ERROR WHEN EXCEPTIONS IS NOT A LIST OF EXCEPTIONS ######
def test_if_get_all_extracted_info_error_message_raises_value_error_when_exceptions_is_not_a_list_of_exceptions():
    with pytest.raises(ValueError):
        GetAllExtractedInfoErrorMessage(
            exceptions=[1]
        )
        
        
        
###### TEST IF GET ALL EXTRACTED INFO ERROR MESSAGE RETURNS THE CORRECT MESSAGE ######
def test_if_get_all_extracted_info_error_message_returns_the_correct_message():
    get_all_extracted_info_error_message = GetAllExtractedInfoErrorMessage(
        exceptions=[ExtractMethodErrorMessage(
            method_name='method_name', 
            original_exception=Exception('original_exception')
        )]
    )
    
    expected_message = f"Error on the following extracting methods:\nError on extract method method_name -\noriginal_exception"
        
    message = get_all_extracted_info_error_message.get_message()
        
    normalized_expected_message = normalize_string(expected_message)
    normalized_result = normalize_string(message)
    
    assert normalized_result == normalized_expected_message
    
def test_if_get_all_extracted_info_error_message_returns_the_correct_message_with_more_than_one_exception():
    get_all_extracted_info_error_message = GetAllExtractedInfoErrorMessage(
        exceptions=[
            ExtractMethodErrorMessage(
                method_name='method_name', 
                original_exception=Exception('original_exception')
            ),
            ExtractMethodErrorMessage(
                method_name='method_name_2', 
                original_exception=Exception('original_exception_2')
            )
        ]
    )
    
    expected_message = f"Error on the following extracting methods:\nError on extract method method_name -\noriginal_exception\nError on extract method method_name_2 -\noriginal_exception_2"
        
    message = get_all_extracted_info_error_message.get_message()
        
    normalized_expected_message = normalize_string(expected_message)
    normalized_result = normalize_string(message)
   
    assert normalized_result == normalized_expected_message
    
    




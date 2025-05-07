import pytest
from unittest.mock import Mock, MagicMock

from packag.modules.pipeline.operation import Operation
from packag.modules.pipeline.task import Task
from packag.modules.pipeline.utils.exceptions import (
    ValidationError,
    TaskError, 
    OperationError,
)
from packag.modules.pipeline.utils.messages import OperationErrorMessage
""" 
Should assert that:
      
* That IF validate input data raise a ValidationError, the run method of the task will raise a TaskError
    * and that the TaskError will contain the correct message: 
        -> must contain:
            * the name of the field (like input_data, output_data, etc) 
            * 'Error validating'
            * the message of the ValidationError
        
* That:
    * IF 
        * validate output data raises a ValidationError
    * THEN:
        * the run method of the task will raise a TaskError
            -> and that the TaskError will contain the correct message: 
                -> must contain:
                * the name of the task (e.g. ExtractDataTask)
                * the name of the field (like input_data, output_data, etc) 
                * 'Error validating'
            
* That IF:
    -> the operation does not raise an exception
    -> the operation returns a valid output
the task will return the output data
  
    
* That IF the operation raises an exception, the task will raise a TaskError
    * and that the TaskError will contain the correct message: 
        -> must contain:
            * the name of the task (e.g. ExtractDataTask)
            * the name of the field (like input_data, output_data, etc) 
"""

def task_error_message_with_operation_error_must_contain(task_name: str, operation_name: str):
    task_name = task_name.lower()
    operation_name = operation_name.lower()
    
    return [
        f'error running task {task_name}',
        f'error running operation {operation_name}',
    ]
def task_error_message_with_validation_error_must_contain(task_name: str, name_of_the_field: str):
    
    task_name = task_name.lower()
    name_of_the_field = name_of_the_field.lower()
    
    return [
            f'error running task {task_name}',
            f'error validating {name_of_the_field}',
            f'the received type is not allowed',
        ]

class MockOperation(Operation, MagicMock):
    def run(self, input_data=None):
        return 'hello'

class TestTask:
    
    @pytest.fixture
    def validation_error_message_must_contain(self):
        def _inner(name_of_the_function, name_of_the_field):
            return [
                'Error validating',
                'function',
                'Received type',
                str(name_of_the_function),
                str(name_of_the_field),
            ]
        return _inner
    
    @pytest.fixture
    def task_error_message_must_contain(self):
        def _inner(name_of_the_task, name_of_the_field):
            return [
                'Error validating',
                'task',
            ]
        return _inner
    
    @pytest.fixture
    def dump_task(self):
        class DumpTask(Task):
            def _validate_operation_cls(self, operation_cls):
                return operation_cls
            def _validate_input(self, input_data):
                return input_data
            def _validate_output(self, output_data):
                return output_data
        return DumpTask
    
    def test_task_with_invalid_operation_cls_raises_a_validationerror(
        self,
        dump_task,
    ):
        """
        ✅ Assert that the run method raise a TaskError if the function validate_operation_cls raises a ValidationError
        """
        
        task = dump_task
        task_instance = task(MockOperation())
        
        task_instance._validate_operation_cls = MagicMock(side_effect=TypeError())
        
        with pytest.raises(TaskError) as e:
            task_instance.run(input_data=None)
            
        error_message = str(e.value).lower()
        
        for item in task_error_message_with_validation_error_must_contain(
            task_name='DumpTask',
            name_of_the_field='operation_cls',
        ):
            assert item in error_message
            
    def test_task_with_invalid_output_data_raises_a_validationerror(
        self,
        dump_task,
    ):
        """
        ✅ Assert that the run method raise a TaskError if the function validate_output raises a ValidationError
        
        The TaskError message must include:
            - the name of the task (e.g., ExtractDataTask)
            - the name of the field that failed validation (on this case, output_data)
            - the text 'Error validating'
        """
        
        task = dump_task
        task_instance = task(MockOperation())
        
        task_instance._validate_output = MagicMock(side_effect=TypeError())
        
        with pytest.raises(TaskError) as e:
            task_instance.run(input_data=None)
            
        error_message = str(e.value).lower()
        
        for item in task_error_message_with_validation_error_must_contain(
            task_name='DumpTask',
            name_of_the_field='output_data',
        ):
            assert item in error_message
            
    def test_task_with_invalid_input_data_raises_a_validationerror(
        self,
        dump_task,
        validation_error_message_must_contain,
    ):
        """
        ✅ Assert that the run method raise a TaskError if the function validate_input raises a ValidationError
        
        The TaskError message must include:
            - the name of the task (e.g., ExtractDataTask)
            - the name of the field that failed validation (on this case, input_data)
            - the text 'Error validating'
        """
        
        task = dump_task
        task_instance = task(MockOperation())
        
        task_instance._validate_input = MagicMock(side_effect=TypeError())
        
        with pytest.raises(TaskError) as e:
            task_instance.run(input_data=None)
            
        error_message = str(e.value).lower()
        
        for item in task_error_message_with_validation_error_must_contain(
            task_name='DumpTask',
            name_of_the_field='input_data',
        ):
            assert item in error_message
            
    def test_task_without_validation_error_and_valid_operation_returns_the_output_data(
        self,
        dump_task,
    ):
        """
        ✅ Assert that the run method of the task returns the output data of the operation if:
            * the operation is valid on initialization
            * the input data is what the task expects
            * the output data is what the task expects
            * the run method of the operation does not raise an exception
        """
        
        
        operation = MockOperation()
        operation.run = MagicMock(return_value='hello')
        
        task = dump_task
        task_instance = task(operation)
        
        output_data = task_instance.run(input_data=None)
        
        assert output_data == 'hello'
        
    def test_task_with_operation_error_raises_a_taskerror(
        self,
        dump_task,
    ):
        """
        ✅ Assert that the run method of the task raises a TaskError if the operation raises an exception
        """
        
        mock_operation_cls = MagicMock()
        
        mock_operation_instance = MagicMock()
        mock_operation_instance.run.side_effect = OperationError(
            OperationErrorMessage(
                operation_name='MockOperation',
                original_exception=Exception('TEST ERROR'),
            )
        )
        
        mock_operation_cls.return_value = mock_operation_instance

        task_instance = dump_task(mock_operation_cls)
        
        with pytest.raises(TaskError) as e:
            task_instance.run(input_data=None)
        
        error_message = str(e.value).lower()
        
        for item in task_error_message_with_operation_error_must_contain(
            task_name='DumpTask',
            operation_name='MockOperation',
        ):
            assert item in error_message
        
        
            
       
   
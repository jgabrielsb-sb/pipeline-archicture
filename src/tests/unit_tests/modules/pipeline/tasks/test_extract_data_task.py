import pytest

from packag.modules.pipeline.tasks import ExtractDataTask

from packag.modules.pipeline.utils.exceptions import ValidationError

from unittest.mock import MagicMock

from pydantic import BaseModel

from packag.modules.pipeline.utils.exceptions import TaskError

from packag.modules.pipeline.operation import Operation

from packag.models import dtoFile

from pathlib import Path





class TestExtractDataTask:
    ###### TEST IF _VALIDATE_OPERATION_CLS RAISE TYPE ERROR WHEN OPERATION_CLS IS NOT AN OPERATION ######
    def test_if_private_validate_operation_cls_raise_type_error_when_operation_cls_is_not_a_operation(self):
        print("dtoFile.File in test:", dtoFile.File)
        import sys
        print("sys.modules keys (filtered):", [k for k in sys.modules.keys() if 'dtoFile' in k])
        print("Module object in sys.modules['packag.models.dtoFile']:", sys.modules['packag.models.dtoFile'])
        with pytest.raises(TypeError):
            ExtractDataTask(operation_cls=None)._validate_operation_cls(operation_cls=None)
            
    ###### TEST IF _VALIDATE_INPUT RAISE TYPE ERROR WHEN INPUT IS NOT A DTO FILE ######
    def test_if_private_validate_input_raise_type_error_when_input_is_not_a_dto_file(self):
        with pytest.raises(TypeError):
            ExtractDataTask(operation_cls=None)._validate_input(input_data=None)

    ###### TEST IF _VALIDATE_OUTPUT RAISE TYPE ERROR WHEN OUTPUT IS NOT A Pydantic Base Model ######
    def test_if_private_validate_output_raise_type_error_when_output_is_not_a_pydantic_base_model(self):
        with pytest.raises(TypeError):
            ExtractDataTask(operation_cls=None)._validate_output(output_data=None)
            
    ###### TEST IF VALIDATE_OPERATION_CLS RAISE VALIDATION ERROR WHEN OPERATION_CLS IS NOT A SUBCLASS OF OPERATION ######
    def test_if_validate_operation_cls_raise_validation_error_when_operation_cls_is_not_a_subclass_of_operation(self):
        with pytest.raises(ValidationError):
            ExtractDataTask(operation_cls=None).validate_operation_cls(operation_cls=None)
    
    ###### TEST IF VALIDATE_INPUT RAISE VALIDATION ERROR WHEN INPUT IS NOT A DTO FILE ######
    def Atest_if_validate_input_raise_validation_error_when_input_is_not_a_dto_file(self):
        with pytest.raises(ValidationError):
            ExtractDataTask(operation_cls=None).validate_input(input_data=None)
        
    ###### TEST IF VALIDATE_OUTPUT RAISE VALIDATION ERROR WHEN OUTPUT IS NOT A Pydantic Base Model ######
    def test_if_validate_output_raise_validation_error_when_output_is_not_a_pydantic_base_model(self):
        with pytest.raises(ValidationError):
            ExtractDataTask(operation_cls=None).validate_output(output_data=None)
        
    
    ####### TEST IF RUN RAISE TASK ERROR WHEN OPERATION_CLS IS NOT A SUBCLASS OF OPERATION ######
    def test_if_run_raise_task_error_when_operation_cls_is_not_a_subclass_of_operation(self):
        
        input_data = MagicMock(BaseModel)
        with pytest.raises(TaskError):
            ExtractDataTask(operation_cls=None).run(input_data=input_data)
    
    ###### TEST IF RUN RAISE TASK ERROR WHEN INPUT IS NOT A DTO FILE ######
    def Atest_if_run_raise_task_error_when_input_is_not_a_dto_file(self):
        operation_cls = MagicMock(Operation)
        operation_cls.run = MagicMock(BaseModel)
        
        input_data = dtoFile.File(file_path=Path('test.pdf'), file_extension='pdf')
        

        output_data = MagicMock(BaseModel)
        
        with pytest.raises(TaskError):
            task = ExtractDataTask(operation_cls=operation_cls)
            task.validate_input(input_data=input_data)
            
    ###### TEST IF RUN RAISE TASK ERROR WHEN OUTPUT IS NOT A Pydantic Base Model ######
    def test_if_run_raise_task_error_when_output_is_not_a_pydantic_base_model(self):
        with pytest.raises(TaskError):
            ExtractDataTask(operation_cls=None).run(input_data=None)

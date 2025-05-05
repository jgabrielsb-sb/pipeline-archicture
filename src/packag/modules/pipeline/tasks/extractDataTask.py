from packag.modules.pipeline.task import Task

from ..operation import Operation

from packag.models import dtoFile

from typing import Type

import pydantic

class ExtractDataTask(Task):
    """
    Extract data from a file.
    
    This task expects to receive a File.File Object as a input;
    Then, it uses the operation class, which has to be a subclass of Operation, to extract the data from the file.
    The output is a dtoData object.
    """
    
    def _validate_operation_cls(self, operation_cls: Type[Operation]):
        if not isinstance(operation_cls, type):
            raise TypeError(f"Expected a operation class type, got {type(operation_cls)} instead")
        
        if not issubclass(operation_cls, Operation):
            raise TypeError(f"{operation_cls} is not a subclass of Operation")

        return operation_cls
    
    def _validate_input(self, input_data: dtoFile.File):
        if not isinstance(input_data, type):
            raise TypeError(f"Expected a File type, got {type(input_data)} instead")
        
        if not isinstance(input_data, dtoFile.File):
            raise TypeError(f"Expected a File object, got {type(input_data)} instead")
        
        return input_data
    
    def _validate_output(self, output_data: Type[pydantic.BaseModel]):
        if not isinstance(output_data, type):
            raise TypeError(f"Expected a pydantic.BaseModel type, got {type(output_data)} instead")
        
        if not issubclass(output_data, pydantic.BaseModel):
            raise TypeError(f"Expected a pydantic.BaseModel type, got {type(output_data)} instead")
        
        return output_data
    
    
from packag.modules.pipeline.task import Task

from ..operation import Operation

from typing import Type



class FormatDataTask(Task):
    """
    Format data from a file.
    
    This task expects to receive a dict object as a input;
    Then, it uses the operation class, which has to be a subclass of Operation, to format the data.
    The output is a dict object.
    """
    
    def _validate_operation_cls(self, operation_cls: Type[Operation]):
        if not isinstance(operation_cls, type):
            raise TypeError(f"Expected a operation class type, got {type(operation_cls)} instead")
        
        if not issubclass(operation_cls, Operation):
            raise TypeError(f"{operation_cls} is not a subclass of Operation")

        return operation_cls
    
    def _validate_input(self, input_data: dict):
        if not isinstance(input_data, dict):
            raise TypeError(f"Expected a {type(dict)} type, got {type(input_data)} instead")
        return input_data
    
    def _validate_output(self, output_data: dict):
        if not isinstance(output_data, dict):
            raise TypeError(f"Expected a {type(dict)} type, got {type(output_data)} instead")
        
        return output_data
    
    
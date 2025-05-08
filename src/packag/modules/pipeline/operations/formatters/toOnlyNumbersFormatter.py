from .baseFormatter import BaseFormatter

from packag.modules.pipeline.utils.exceptions import (
    ValidationError
)

from packag.modules.utils import get_logger

from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage
)

from packag.modules.string_operations.functions import get_only_numbers

operation_logger = get_logger('operation_logger')

class ToOnlyNumbersFormatter(BaseFormatter):
    
    def _perform_operation(self, input_data: dict[str, str]) -> dict[str, str]:
        columns_to_format = self.columns
        
        for column in columns_to_format:
            input_data[column] = get_only_numbers(input_data[column])
                
        return input_data
    
    
        
            
        
        
        
        
        
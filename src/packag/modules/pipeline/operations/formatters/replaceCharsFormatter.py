from .baseFormatter import BaseFormatter

from packag.modules.pipeline.utils.exceptions import (
    ValidationError
)

from packag.modules.utils import get_logger

from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage
)

operation_logger = get_logger('operation_logger')

class ReplaceCharsFormatter(BaseFormatter):
    def __init__(self, columns: list[str], chars_to_replace: dict[str, str]):
        """
        Replace characters in the input data.
        
        Args:
            columns (list[str]): The columns to format.
            chars_to_replace (dict[str, str]): The characters to replace.
            
        Returns:
            dict[str, str]: The input data with the characters replaced.
            
        Examples:
            >>> replace_formatter = ReplaceCharsFormatter(columns=['state', 'city'], chars_to_replace={'RIO DE JANEIRO': 'RJ'})
            >>> result = replace_formatter.run({'state': 'RIO DE JANEIRO', 'city': 'RIO DE JANEIRO'})
            >>> result
            {'state': 'RJ', 'city': 'RJ'}
        """
        super().__init__(columns)
        
        if not isinstance(chars_to_replace, dict):
            pass  # will raise below
        elif not all(isinstance(key, str) for key in chars_to_replace.keys()):
            pass
        elif not all(isinstance(value, str) for value in chars_to_replace.values()):
            pass
        else:
            self.chars_to_replace = chars_to_replace
            return 
            
        message = ValidationErrorMessage(
            function_name='__init__',
            input_name='chars_to_replace',
            received_type=str(type(chars_to_replace)),
            expected_type=str(dict[str, str])
        )
        
        operation_logger.error(message.get_message())
        
        raise ValidationError(message)
    
    def _perform_operation(self, input_data: dict[str, str]) -> dict[str, str]:
        columns_to_format = self.columns
        
        for column in columns_to_format:
            for char_to_replace, replacement in self.chars_to_replace.items():
                input_data[column] = input_data[column].replace(char_to_replace, replacement)
                
        return input_data
    
    
        
            
        
        
        
        
        
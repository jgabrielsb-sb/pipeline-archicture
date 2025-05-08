
from packag.modules.utils import get_logger

from .baseFormatter import BaseFormatter

from packag.modules.string_operations.functions import remove_leading_zeros

class RemoveZerosFromBeginningFormatter(BaseFormatter):
    """
    Remove zeros from the beginning of the strings in the columns.
    
    Args:
        columns (list[str]): The columns to remove zeros from.
    Returns:
        dict[str, str]: The input data with the zeros removed from the beginning of the strings in the columns.
    """
    
    def _perform_operation(self, input_data: dict[str, str]) -> dict[str, str]:
        columns_to_format = self.columns
        
        for column in columns_to_format:
            input_data[column] = remove_leading_zeros(input_data[column])
            
        return input_data
        
        
        
        
from abc import ABC, abstractmethod

class Operation(ABC):
    """
    Abstract base class for all operations.
    
    An operation is a class that implements a specific task.
    It has a run method that receives an input and returns an output.
    
    The operation, thus, does not perform any validation of the input or output.
    This is done by the task that uses the operation.
    """
    
    @abstractmethod
    def run(self, input_data=None): # pragma: no cover
        """
        Run the operation.
        """
        pass
    
    
    
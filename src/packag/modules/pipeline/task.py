from abc import ABC, abstractmethod
class Task(ABC):
    """
    Abstract base class for all tasks.
    """
    
    @abstractmethod
    def run(self, previous_task_result=None):
        pass
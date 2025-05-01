"""
Pipeline Module

This module defines the Pipeline class, responsible for orchestrating tasks.
It is designed as a generic infrastructure component, agnostic to business logic.

IMPORTANT:
- This class should remain business-logic free.
- Changes to this module may affect all pipelines across the system.
- Ensure 100% test coverage and backward compatibility before modifying.

How it works:
A pipeline receives a list of tasks.
Then, by using the run method, it executes the tasks in order, passing the result of each task to the next one.
If you want to start the pipeline with some data, you can pass it to the run method as an argument.
If any task fails, the pipeline stops and raises an exception (PipelineError).
For details about Task, see the Task class.
How to use:
1. Create a pipeline class that inherits from Pipeline.
2. Implement the get_tasks method.
3. Run the pipeline with the run method.

Example:

class MyPipeline(Pipeline):
    def get_tasks(self):
        return [Task1(), Task2(), Task3()]

pipeline = MyPipeline()
pipeline.run()
"""

from abc import ABC, abstractmethod

from packag.modules.utils import get_logger

from packag.modules.pipeline.task import Task

from packag.modules.pipeline.exceptions import (
    PipelineError,
    TaskError
)
pipeline_logger = get_logger('pipeline')

class Pipeline(ABC):
    """
    Generic pipeline class that orchestrates tasks.
    """
    
    def __init__(self):
        tasks = self.get_tasks()
        
        # validates the tasks are a list of Task objects
        if not isinstance(tasks, list):
            message = 'Tasks must be a list of Task objects. Please implement the get_tasks method correctly.'
            pipeline_logger.error(message)
            raise PipelineError(message=message, pipeline_name=self.__class__.__name__)
        
        # validates the tasks are a list of Task objects
        if not all(isinstance(task, Task) for task in tasks):
            message = 'Tasks must be a list of Task objects. Please implement the get_tasks method correctly.'
            pipeline_logger.error(message)
            raise PipelineError(message=message, pipeline_name=self.__class__.__name__)
        
        self.tasks = tasks
    
    @abstractmethod
    def get_tasks(self): # pragma: no cover
        pass
    
    def run(self, input_data=None):
        """
        Runs the pipeline but starting with the input data.
        Then, it passes the result of each task to the next one.
        Args:
            input_data: The input data for the pipeline. Can be None
        Returns:
            The result of the last task.
        """
        pipeline_logger.info(f'Running pipeline: {self.__class__.__name__}')
        
        tasks = self.get_tasks()
        
        previous_task_result = input_data
        
        try:
            for task in tasks:           
                previous_task_result = task.run(previous_task_result)
                
            pipeline_logger.info(f'Pipeline: {self.__class__.__name__} completed successfully')
        except TaskError as e:
            pipeline_logger.error(f'Error on pipeline: {e}')
            raise PipelineError(message=e.message, pipeline_name=self.__class__.__name__, original_exception=e)
            
        return previous_task_result
            
           

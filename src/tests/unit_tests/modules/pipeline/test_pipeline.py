"""
What should be tested:
    - The pipeline should be able to run a list of tasks.
    - The pipeline should be able to run a list of tasks with input data.
    - The pipeline should be able to run a list of tasks and return the result of the last task.
    - The pipeline should raise an exception if any task fails.
    - The pipeline should raise an exception if the tasks are not a list.
    - The pipeline should raise an exception if the tasks are not a list of Task objects.
    
This test file should not depend on the implementation details of the Task class.
"""

import pytest

from packag.modules.pipeline import Pipeline

from packag.modules.pipeline.utils.exceptions import (
    PipelineError,
    ValidationError
)

from unittest.mock import MagicMock

from packag.modules.pipeline.task import Task

from packag.modules.pipeline.utils.exceptions import TaskError

from packag.modules.utils.messages import TaskErrorMessage
class TestPipeline:
    
    def test_pipeline_with_non_list_get_tasks_implementation_raises_an_exception(self):
        
        class PipelineWithNonListGetTasks(Pipeline):
            def get_tasks(self):
                return "not a list"
            
        with pytest.raises(ValidationError):
            PipelineWithNonListGetTasks().validate_tasks()
            
    def test_pipeline_with_a_list_of_non_task_objects_get_tasks_implementation_raises_an_exception(self):
        
        class PipelineWithNonListOfTaskObjectsGetTasks(Pipeline):
            def get_tasks(self):
                return [
                    "not a task object",
                    "not a task object"
                ]
            
        with pytest.raises(ValidationError):
            PipelineWithNonListOfTaskObjectsGetTasks().validate_tasks()
            
    def test_run_method_raises_a_pipeline_error_if_any_task_raises_a_task_error(self):
        
        mock_task = MagicMock(Task)
        
        task_error_message = TaskErrorMessage(
            task_name='MockTask',
            original_exception=Exception('TEST ERROR')
        )
        
        mock_task.run.side_effect = TaskError(task_error_message)
        
        class PipelineWithTaskThatRaisesATaskError(Pipeline):
            def get_tasks(self):
                return [
                    mock_task  # this task will raise a TaskError
                ]
            
        with pytest.raises(PipelineError):
            PipelineWithTaskThatRaisesATaskError().run()
            
    def test_run_method_returns_the_result_of_the_last_task(self):
        
        #mock_task = MockTaskWithResult()
        mock_task = MagicMock(Task)
        mock_task.run.return_value = "result of the last task"
        
        class PipelineWithTwoTasks(Pipeline):
            def get_tasks(self):
                return [
                    mock_task,
                    mock_task
                ]
                
        pipeline_result = PipelineWithTwoTasks().run()
        
        assert pipeline_result == 'result of the last task'
                
    def test_run_method_returns_the_result_of_the_last_task_when_starting_with_input_data(self):
        
        mock_task = MagicMock(Task)
        mock_task.run.return_value = "result of the last task"
        
        class PipelineWithTwoTasksAndInputData(Pipeline):
            def get_tasks(self):
                return [
                    mock_task,
                    mock_task
                ]
            
            def run(self, input_data=None):
                return super().run(input_data)
            
        pipeline_result = PipelineWithTwoTasksAndInputData().run(input_data='initial data')
        
        assert pipeline_result == 'result of the last task'
        
    
        


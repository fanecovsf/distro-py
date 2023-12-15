from django.urls import path

from scheduler.views import AvailableModules, QueueTaskView, CleanQueueView


urlpatterns = [
    path('/modules', AvailableModules.as_view(), name='available_files_view'),
    path('/queue-task', QueueTaskView.as_view(), name='queue_task_view'),
    path('/clean-queue', CleanQueueView.as_view(), name='clean_queue_view'),
]

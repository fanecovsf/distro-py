from django.urls import path

from scheduler.views import AvailableModules, QueueTask


urlpatterns = [
    path('/modules', AvailableModules.as_view(), name='available_files_view'),
    path('/queue-task', QueueTask.as_view(), name='queue_task_view'),
]

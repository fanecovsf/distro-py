from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from scheduler.utils import import_function, define_queue

import os
import datetime

from distro.settings import MODULES_PATH, DEFAULT_QUEUE, TASK_RETRIES

from rq import Retry


class AvailableModules(APIView):


    def get(self, request):
        func_list = []
        modules_path = os.path.join('/app/repo/modules/', MODULES_PATH)
        for file in os.listdir(modules_path):
            if file.endswith('.py') and '__init__' not in file:
                data = {
                    "module": file.split('.')[0]
                }

                func_list.append(data)

        return Response(func_list, status=status.HTTP_200_OK)
    

class QueueTaskView(APIView):


    def post(self, request):
        module = request.data.get('module')
        function = request.data.get('function')
        queue_data = request.data.get('queue', 'default')

        queue = define_queue(queue_data)

        func = import_function(module, function)
        
        if func:
            queue.enqueue(func, retry=Retry(max=TASK_RETRIES))
            return Response(
                data={
                    'message':f'task enqueued on {queue_data} queue.',
                    'task': f'{module}.{function}'
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(data={'message':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class ScheduleTimeTaskView(APIView):


    def post(self, request):
        module = request.data.get('module')
        function = request.data.get('function')
        seconds = request.data.get('seconds', 0)
        minutes = request.data.get('minutes', 0)
        hours = request.data.get('hours', 0)
        queue_data = request.data.get('queue', 'default')

        queue = define_queue(queue_data)

        func = import_function(module, function)

        if func:
            queue.enqueue_in(datetime.timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours)), func)
            return Response(
                data={
                    'message':f'task scheduled for {hours} Hours, {minutes} Minutes and {seconds} Seconds from now on {queue_data} queue.',
                    'task': f'{module}.{function}',
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(data={'message':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    

class CleanQueueView(APIView):


    def get(self, request):
        DEFAULT_QUEUE.empty()

        return Response(data={'message':'queue cleaned up'}, status=status.HTTP_200_OK)


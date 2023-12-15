from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from scheduler.utils import import_function


from rq.job import Job
import os

from distro.settings import MODULES_PATH, QUEUE


class AvailableModules(APIView):


    def get(self, request):
        func_list = []
        for file in os.listdir(os.path.join(MODULES_PATH, 'modules')):
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

        func = import_function(module, function)
        
        if func:
            QUEUE.enqueue(func)
            return Response(
                data={
                    'message':'task enqueued',
                    'task': f'{module}.{function}'
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(data={'message':'invalid data'}, status=status.HTTP_404_NOT_FOUND)
    

class CleanQueueView(APIView):


    def get(self, request):
        QUEUE.empty()

        return Response(data={'message':'queue cleaned up'}, status=status.HTTP_200_OK)


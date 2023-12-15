from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('scheduler', include('scheduler.urls'), name='scheduler_app'),
]

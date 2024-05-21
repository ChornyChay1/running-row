# video/urls.py

from django.urls import path
from .views import generate_video

urlpatterns = [
    path('generate_video/', generate_video, name='generate_video'),
]
from django.urls import path
from .views import upload_file, succes

urlpatterns = [
    path('upload/', upload_file, name='upload'),
    path('success/', succes, name='success'),
]

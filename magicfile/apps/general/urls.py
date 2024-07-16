from django.urls import path
from .views import create_company, list_company

urlpatterns = [
    path('company-create/', create_company, name='create_company'),
    path('company-list/', list_company, name='list_company'),
]

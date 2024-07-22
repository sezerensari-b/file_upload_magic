from django.urls import path
from .views import create_company, list_company, upload_logo, delete_logo, index, login, logout, edit_temp_company

urlpatterns = [
    path('company-create/', create_company, name='create_company'),
    path('company-list/', list_company, name='list_company'),
    path('logo-upload/', upload_logo, name='upload_logo'),
    path('logo-delete/', delete_logo, name='delete_logo'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('temp-company-edit/', edit_temp_company, name='create_temp_company'),
]

from django.urls import path

from .views import *

app_name = 'todo'

urlpatterns = [
    path('', index_view, name='index'),
    path('create/', create_view, name='create'),
    path('delete/<int:task_id>/', delete_view, name='delete'),
    path('mark_done/<int:task_id>/', mark_done_view, name='mark_done'),
]


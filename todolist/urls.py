from django.urls import path
from .views import CreateTask, ListTask, UpdateTask, DeleteTask, TaskCompleted


urlpatterns = [
    path('task_create/', CreateTask.as_view(), name='task_create'),
    path('', ListTask, name='task_list'),
    path('task_update/<int:pk>/', UpdateTask.as_view(), name='task_update'),
    path('task_delete/<int:pk>/', DeleteTask.as_view(), name='task_delete'),
    path('completed/', TaskCompleted.as_view(), name='task_completed'),
]
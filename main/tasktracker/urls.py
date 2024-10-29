from django.urls import path
from . import views

urlpatterns = [
    path('task/create/', views.task_create, name='task-create'),
    path('task/get/<slug:task_slug>/', views.task_get, name='task-get'),
    path('task/all/', views.all_tasks_get, name='task-all'),
    path('task/update/<slug:task_slug>/', views.task_update, name='task-update'),
    path('task/delete/<slug:task_slug>/', views.task_delete, name='task-delete'),
    path('task/observe/<slug:task_slug>/', views.task_observe, name='task-observe'),
    path('status/set/<slug:task_slug>/', views.status_set, name='status-set'),
]
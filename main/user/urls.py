from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.user_create, name='user-create'),
    path('get/', views.user_get, name='user-get'),
    path('update/', views.user_update, name='user-update'),
    path('delete/', views.user_delete, name='user-delete'),
]
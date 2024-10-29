from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.user_create, name='user-create'),
    path('all/', views.user_all_get, name='user-all-get'),
    path('get/<str:nickname>/', views.user_get, name='user-get'),
    path('update/<str:nickname>/', views.user_update, name='user-update'),
    path('delete/<str:nickname>/', views.user_delete, name='user-delete'),
    path('set-permission/<str:nickname>/', views.user_set_permission, name='user-set-permission'),
]
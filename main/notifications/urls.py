from django.urls import path
from . import views

urlpatterns = [
    path('mail/send/', views.email_notification, name='email-notification'),
    path('telegram/send/', views.telegram_notification, name='telegram-notification')
]
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .selectors import *
from .services import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
        request=NotificationSerializer,
        responses=None
)
@api_view(['POST'])
def email_notification(request):
    pass

@extend_schema(
        request=NotificationSerializer,
        responses=None
)
@api_view(['POST'])
def telegram_notification(request):
    pass
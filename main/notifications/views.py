from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from .selectors import *
from .services import *
from main.permissions import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
        request=NotificationSerializer,
        responses=None
)
@api_view(['POST'])
@permission_classes([IsAuthenticated & (IsPm | IsAdminUser)])
def email_notification(request):
    status_code, response = send_email(request)

    if status_code == 202:
        return Response(response, status=status.HTTP_202_ACCEPTED)
    elif status_code == 400:
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    elif status_code == 500:
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        request=NotificationSerializer,
        responses=None
)
@api_view(['POST'])
@permission_classes([IsAuthenticated & (IsPm | IsAdminUser)])
def telegram_notification(request):
    status_code, response = send_tg(request)

    if status_code == 202:
        return Response(response, status=status.HTTP_202_ACCEPTED)
    elif status_code == 400:
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    elif status_code == 500:
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
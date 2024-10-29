from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .selectors import *
from .services import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
        request=UserSerializer,
        responses=None
)
@api_view(['POST'])
def user_create(request):
    status_code, response = create_user(request)
    if status_code == 200:
        return Response(response, status=status.HTTP_201_CREATED)
    elif status_code == 400:
        return Response({'error: ':response}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error: ':response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
        request=UserSerializer,
        responses=None
)    
@api_view(['GET'])
def user_get(request):
    pass

@extend_schema(
        request=UserSerializer,
        responses=None
)
@api_view(['PUT'])
def user_update(request):
    pass

@extend_schema(
        request=UserSerializer,
        responses=None
)
@api_view(['DELETE'])
def user_delete(request):
    pass

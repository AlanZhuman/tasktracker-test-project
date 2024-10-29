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
def user_get(request, nickname):
    status_code, response = get_user(nickname)
    
    if status_code == 200:
        return Response(response)
    elif status_code == 404:
        return Response({'error': 'No user found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def user_all_get(request):
    status_code, response = get_all_users()
    
    if status_code == 200:
        return Response(response)
    elif status_code == 404:
        return Response({'error': 'No users found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        request=UserUpdateSerializer,
        responses=None
)
@api_view(['PUT'])
def user_update(request, nickname):
    status_code, response = update_user(request, nickname)
    
    if status_code == 200:
        return Response(response, status=status.HTTP_200_OK)
    elif status_code == 404:
        return Response({'error': 'No user found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        request=UserSerializer,
        responses=None
)
@api_view(['DELETE'])
def user_delete(request, nickname):
    status_code, response = delete_user(nickname)
    
    if status_code == 204:
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    elif status_code == 404:
        return Response({'error': 'No user found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

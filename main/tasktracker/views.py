from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from .selectors import *
from .services import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from main.permissions import *

@extend_schema(request=TaskSerializer, responses=None)
@api_view(['POST'])
@permission_classes([IsAuthenticated | IsCRUD])
def task_create(request):
    status_code, response = create_task(request)
    if status_code == 200:
        return Response(response, status=status.HTTP_201_CREATED)
    elif status_code == 400:
        return Response({'error: ':response}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error: ':response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=TaskSerializer, responses=None)    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_get(request, task_slug):
    status_code, response = get_task(task_slug)
    
    if status_code == 200:
        return Response(response)
    elif status_code == 404:
        return Response({'error': 'No task found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=TaskSerializer, responses=None)    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_tasks_get(request):
    status_code, response = get_all_tasks()
    
    if status_code == 200:
        return Response(response)
    elif status_code == 404:
        return Response({'error': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=TaskSerializer, responses=None)
@api_view(['PUT'])
@permission_classes([IsAuthenticated | IsCRUD])
def task_update(request, task_slug):
    status_code, response = update_task(request, task_slug)
    
    if status_code == 200:
        return Response(response, status=status.HTTP_200_OK)
    elif status_code == 404:
        return Response({'error': 'No task found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=TaskSerializer, responses=None)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsCRUD])
def task_delete(request, task_slug):
    status_code, response = delete_task(task_slug)
    
    if status_code == 204:
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    elif status_code == 404:
        return Response({'error': 'No task found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=TaskObserveSerializer, responses=None)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_observe(request, task_slug):
    status_code, response = observe_task(request, task_slug)
    
    if status_code == 200:
        return Response(response, status=status.HTTP_202_ACCEPTED)
    elif status_code == 404:
        return Response({'error': 'No task found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=StatusSerializer, responses=None)
@api_view(['POST'])
@permission_classes([IsAuthenticated | IsCRUD])
def status_set(request, task_slug):
    status_code, response = set_status(request, task_slug)
    
    if status_code == 200:
        return Response(response, status=status.HTTP_202_ACCEPTED)
    elif status_code == 404:
        return Response({'error': 'No task found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=StatusSerializer, responses=None)
@api_view(['GET'])
@permission_classes([IsAuthenticated | IsReadTask])
def status_get(request, task_slug):
    status_code, response = get_status(task_slug)
    
    if status_code == 200:
        return Response(response, status=status.HTTP_202_ACCEPTED)
    elif status_code == 404:
        return Response({'error': 'No task found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

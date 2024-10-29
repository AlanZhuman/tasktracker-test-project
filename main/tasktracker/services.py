from .models import Task
from .serializers import TaskSerializer, StatusSerializer, TaskObserveSerializer
    
def create_task(request):
    data = TaskSerializer(data=request.data)

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}

def update_task(request, slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}

    data = TaskSerializer(instance = item, data=request.data)

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}

def delete_task(slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}
    item.delete()
    return 204, {'msg':'Deleted successful'}

def observe_task(request, slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}
    
    data = TaskObserveSerializer(instance = item, data=request.data)

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}

def set_status(request, slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}

    data = StatusSerializer(instance = item, data=request.data)

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}
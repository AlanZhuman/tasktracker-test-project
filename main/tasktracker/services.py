from .models import Task
from .serializers import TaskSerializer, StatusSerializer, TaskObserveSerializer
from notifications.tasks import celery_send_mail

    
def create_task(request):
    data = TaskSerializer(data=request.data)

    if data.is_valid():
        task = data.save() 

        celery_send_mail.delay(change_type="CREATED", data={
            'task_id': task.id,
            'recipient_list': [{'name': observer.name} for observer in task.observers.all()],
            'msg': 'Задача была создана.' 
        })

        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid', 'data:': data.data, 'error_info: ':data.errors}
    return 500, {'Serializer error:': data.errors}

def update_task(request, slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}

    data = TaskSerializer(instance = item, data=request.data)

    if data.is_valid():
        task = data.save() 

        celery_send_mail.delay(change_type="UPDATED", data={
            'task_id': task.id,
            'recipient_list': [{'name': observer.name} for observer in task.observers.all()],
            'msg': 'Задача была обновлена.' 
        })
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}

def delete_task(slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}
    task_id = item.id

    celery_send_mail.delay(change_type="DELETED", data={
        'task_id': task_id,
        'recipient_list': [{'name': observer.name} for observer in item.observers.all()],
        'msg': 'Задача была удалена.'
    })

    return 204, {'msg':'Deleted successful'}

def observe_task(request, slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}
    
    isObserve = True
    
    data = TaskObserveSerializer(instance = item, data=request.data, context={'isObserve': isObserve, 'user_instance':request.user})

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}

def unobserve_task(request, slug):
    try:
        item = Task.objects.get(slug=slug)
    except Task.DoesNotExist:
        return 404, {'error': 'Task not found.'}
    
    isObserve = False
    
    data = TaskObserveSerializer(instance = item, data=request.data, context={'isObserve': isObserve, 'user_instance':request.user})

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

        task_id = item.id

        celery_send_mail.delay(change_type="STATUS_CHANGED", data={
            'task_id': task_id,
            'recipient_list': [{'name': observer.name} for observer in item.observers.all()],
            'msg': 'Задача была удалена.'
        })

        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}
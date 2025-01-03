from .models import Task, Status
from .serializers import TaskSerializer, StatusSerializer

def get_all_tasks():
    try:
        try:
            items = Task.objects.all()
        except Task.DoesNotExist:
            return 404, {'error': 'Tasks not found.'}
        serializer = TaskSerializer(items, many=True)
        return 200, serializer.data  # Возвращаем статус и данные
    except Exception as e:
        return 500, str(e)  # Возвращаем ошибку, если что-то пошло не так
    
def get_task(slug):
    try:
        try:
            item = Task.objects.get(slug=slug)
        except Task.DoesNotExist:
            return 404, {'error': 'Task not found.'}
        serializer = TaskSerializer(item)
        return 200, serializer.data  # Возвращаем статус и данные
    except Exception as e:
        return 500, str(e)  # Возвращаем ошибку, если что-то пошло не так
    
def get_status(slug):
    try:
        try:
            item = Status.objects.get(task=Task.objects.get(slug=slug))
        except Task.DoesNotExist:
            return 404, {'error': 'Status not found.'}
        serializer = StatusSerializer(item)
        return 200, serializer.data  # Возвращаем статус и данные
    except Exception as e:
        return 500, str(e)  # Возвращаем ошибку, если что-то пошло не так
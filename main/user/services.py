from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, UserRoleSetSerializer
    
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        # Создать логику для добавления executor'a в наблюдатели
        return 200, serializer.data
    elif serializer.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': serializer.errors}

def update_user(request, name):
    try:
        item = User.objects.get(name=name)
    except User.DoesNotExist:
        return 404, {'error': 'User not found.'}

    data = UserUpdateSerializer(instance = item, data=request.data)

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}

def delete_user(name):
    try:
        item = User.objects.get(name=name)
    except User.DoesNotExist:
        return 404, {'error': 'User not found.'}
    item.delete()
    return 204, {'msg':'Deleted successful'}

def set_permission_user(request, name):
    try:
        item = User.objects.get(name=name)
    except User.DoesNotExist:
        return 404, {'error': 'User not found.'}

    data = UserRoleSetSerializer(instance = item, data=request.data)

    if data.is_valid():
        data.save()
        return 200, data.data
    elif data.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': data.errors}
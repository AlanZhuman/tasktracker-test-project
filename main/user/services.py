from .models import User
from .serializers import UserSerializer
    
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        # Создать логику для добавления executor'a в наблюдатели
        return 200, serializer.data
    elif serializer.is_valid() == False:
        return 400, {'error': 'Provided data is invalid'}
    return 500, {'Serializer error:': serializer.errors}
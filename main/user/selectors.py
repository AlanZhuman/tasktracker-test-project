from .models import User
from .serializers import UserSerializer

def get_all_users():
    try:
        try:
            items = User.objects.all()
        except User.DoesNotExist:
            return 404, {'error': 'Users not found.'}
        serializer = UserSerializer(items, many=True)
        return 200, serializer.data  # Возвращаем статус и данные
    except Exception as e:
        return 500, str(e)  # Возвращаем ошибку, если что-то пошло не так
    
def get_user(name):
    try:
        try:
            item = User.objects.get(name=name)
        except User.DoesNotExist:
            return 404, {'error': 'User not found.'}
        serializer = UserSerializer(item)
        return 200, serializer.data  # Возвращаем статус и данные
    except Exception as e:
        return 500, str(e)  # Возвращаем ошибку, если что-то пошло не так
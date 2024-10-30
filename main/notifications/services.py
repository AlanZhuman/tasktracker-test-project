from .serializers import NotificationSerializer
from .models import Notification
from .tasks import celery_send_mail
import smtplib

def send_email(request):
    serializer = NotificationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        celery_send_mail.delay(None, serializer.validated_data) # Отправляем письмо в celery

        return 202, serializer.data
    elif serializer.is_valid() == False:
        return 400, {'error': 'Provided data is invalid', 'details': serializer.errors}
    return 500, {'Serializer error:': serializer.errors}

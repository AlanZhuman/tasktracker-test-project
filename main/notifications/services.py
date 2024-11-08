from .serializers import NotificationSerializer
from .tasks import celery_send_mail, celery_send_tg

def send_email(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        celery_send_mail.delay(None, serializer.validated_data) # Отправляем письмо в celery
        return 202, serializer.data
    elif serializer.is_valid() == False:
        return 400, {'error': 'Provided data is invalid', 'details': serializer.errors}
    return 500, {'Serializer error:': serializer.errors}

def send_tg(request):
    serializer = NotificationSerializer(data=request.data)

    if serializer.is_valid():
        notification = serializer.save()  # Сохраняем уведомление

        # Передаем только нужные данные в Celery (например, имена пользователей и task_id)
        task_id = notification.task.id
        data_to_send = {
            'task_id': task_id,
            'recipient_list': [{'name': user.name} for user in notification.recipient_list.all()],
            'msg': notification.msg
        }

        # Отправляем данные в Celery
        celery_send_tg.delay(None, data_to_send)

        return 202, serializer.data
    return 400, {'error': 'Provided data is invalid', 'details': serializer.errors}

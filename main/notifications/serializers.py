from rest_framework import serializers
from user.serializers import CeleryUserNameOnlySerializer
from .models import Notification
from user.models import User
from tasktracker.models import Task
from django.core.exceptions import ObjectDoesNotExist

class NotificationSerializer(serializers.ModelSerializer):
    recipient_list = CeleryUserNameOnlySerializer(many=True)
    task_id = serializers.IntegerField()

    class Meta:
        model = Notification
        fields = ('recipient_list', 'task_id', 'msg')

    def create(self, validated_data):
        recipient_data = validated_data.pop('recipient_list', [])
        mail = Notification.objects.create(**validated_data)
        
        # Получаем задачу по task_id и назначаем её mail
        task_instance = Task.objects.get(id=validated_data['task_id'])
        mail.task = task_instance
        mail.save()  # Сохраняем mail, чтобы можно было добавлять в ManyToManyField
        
        # Добавляем пользователей в список получателей
        for user_data in recipient_data:
            user_name = user_data['name']
            try:
                user = User.objects.get(name=user_name)
                mail.recipient_list.add(user)
            except ObjectDoesNotExist:
                continue  # Игнорируем пользователей, которые не найдены
        return mail
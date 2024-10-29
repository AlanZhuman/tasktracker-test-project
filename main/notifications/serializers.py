from rest_framework import serializers
from .models import Notification
from user.models import User
from tasktracker.models import Task

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
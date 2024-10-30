from django.db import models
from tasktracker.models import Task
from user.models import User

class Notification(models.Model):
    task = models.ForeignKey(Task, related_name='notification', on_delete=models.CASCADE)
    msg = models.TextField(null=True, blank=True)
    recipient_list = models.ManyToManyField(User, related_name='recipient')
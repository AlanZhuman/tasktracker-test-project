from django.db import models
from tasktracker.models import Task
from user.models import User

class Notification(models.Model):
    class Events(models.TextChoices):
        CREATED = 'CREATED', 'CREATED'
        UPDATED = 'UPDATED', 'UPDATED'
        DELETED = 'DELETED', 'DELETED'
        REMIND = 'REMIND', 'REMIND'

    task = models.OneToOneField(Task, related_name='notification', on_delete=models.CASCADE)
    msg = models.TextField(null=True, blank=True)
    event_type = models.CharField(choices=Events.choices, max_length=10)
    recipient_list = models.ManyToManyField(User, related_name='recipient')
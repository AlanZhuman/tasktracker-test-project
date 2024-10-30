from django.db import models
from user.models import User
from django.template.defaultfilters import slugify

class Task(models.Model):
    class Statuses(models.TextChoices):
        PLANNED = "PLANNED", 'PLANNED'
        ACTIVE = "ACTIVE", "ACTIVE"
        ON_CHECK = "ON_CHECK", "ON_CHECK"
        DONE = "DONE", "DONE"
        FAILED = "FAILED", 'FAILED'
        EXPIRED = 'EXPIRED', 'EXPIRED'
    
    name = models.CharField(max_length=200, default=None)
    slug = models.SlugField(unique=True, default=None)
    description = models.TextField(blank=True)
    executor = models.ManyToManyField(User, related_name='tasks_as_executor')
    observers = models.ManyToManyField(User, related_name='tasks_as_observer')
    status = models.CharField(choices=Statuses.choices, max_length=15, default=Statuses.PLANNED)
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    time_deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Task: {self.name}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Task, self).save(*args, **kwargs)
    
class Status(models.Model):
    class Statuses(models.TextChoices):
        PLANNED = "PLANNED", 'PLANNED'
        ACTIVE = "ACTIVE", "ACTIVE"
        ON_CHECK = "ON_CHECK", "ON_CHECK"
        DONE = "DONE", "DONE"
        FAILED = "FAILED", 'FAILED'
        EXPIRED = 'EXPIRED', 'EXPIRED'

    previous_status = models.CharField(choices=Statuses.choices, max_length=15, blank=True, null=True)
    set_status = models.CharField(choices=Statuses.choices, max_length=15, default=Statuses.PLANNED, blank=True, null=True)
    task = models.OneToOneField(Task, related_name='status_log', on_delete=models.CASCADE)
    edit_author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Related {self.task}"
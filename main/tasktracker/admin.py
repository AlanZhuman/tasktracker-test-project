from django.contrib import admin
from .models import Task, Status

myModels = [Task, Status]
admin.site.register(myModels)


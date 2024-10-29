from django.contrib import admin
from .models import User, Task, Status

myModels = [User, Task, Status]
admin.site.register(myModels)


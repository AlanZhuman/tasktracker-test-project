from django.contrib import admin
from .models import Notification

myModels = [Notification]
admin.site.register(myModels)

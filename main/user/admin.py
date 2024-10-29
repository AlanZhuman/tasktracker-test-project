from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'telegram')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    list_display = ('name', 'email', 'display_groups')
    list_filter = ('groups',)  # Фильтр по группам

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    display_groups.short_description = 'Groups'

    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(User, UserAdmin)

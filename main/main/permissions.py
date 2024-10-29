from rest_framework import permissions

class IsCUD(permissions.BasePermission):
    """
    CUD Permission check for users
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='CUD-user').exists()
    
class IsRead(permissions.BasePermission):
    """
    Read Permission check for users
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='R-user').exists()
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.observers.all()
    
class IsPm(permissions.BasePermission):
    """
    Pm Permission check for users
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Pm-user').exists()
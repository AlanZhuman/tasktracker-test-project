from rest_framework import permissions

class IsCRUD(permissions.BasePermission):
    """
    CRUD Permission check for users
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='CRUD-user').exists()
    
class IsReadTask(permissions.BasePermission):
    """
    Read Permission check for users and Task model
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='R-user').exists()
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.observers.all()
    
    
    
class IsSameUser(permissions.BasePermission):
    '''
    Permission to check is request.user the same with "User" model instance
    '''
    def has_object_permission(self, request, view, obj):
        return request.user == obj
    
class IsPm(permissions.BasePermission):
    """
    Pm Permission check for users
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Pm-user').exists()
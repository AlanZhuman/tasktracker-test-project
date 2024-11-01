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
        return request.user in obj.observers.all() or request.user in obj.executor.all()
    
    
    
class IsSameUser(permissions.BasePermission):
    '''
    Permission to check if request.user is the same as the "User" model instance
    '''
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff == True
    
class IsPm(permissions.BasePermission):
    """
    Pm Permission check for users
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Pm-user').exists()
from rest_framework import permissions
from .models import *


class PermitAdminAccess(permissions.BasePermission):
    edit_methods = ('PUT','POST','DELETE')
    
    def has_permission(self, request, view):
       
        return request.user.is_superuser
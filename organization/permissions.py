from rest_framework.permissions import BasePermission
from .models import Employee

class EmployeePermissionsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user,"organization_owner")



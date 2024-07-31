from rest_framework.permissions import BasePermission

from todo.models import TaskAssignee


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class HasTaskPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        task_assignee = TaskAssignee.objects.filter(task=obj,
                                                    user=request.user).first()
        if task_assignee:
            if request.method in (
            'GET', 'HEAD', 'OPTIONS') and task_assignee.can_read:
                return True
            if request.method in (
            'PUT', 'PATCH', 'DELETE') and task_assignee.can_update:
                return True
        return False

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task, TaskAssignee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskAssigneeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TaskAssignee
        fields = ['user', 'can_read', 'can_update']


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    assignees = TaskAssigneeSerializer(source='taskassignee_set', many=True,
                                       read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'updated_at',
                  'owner', 'assignees']


class AssigneeAddSerializer(serializers.Serializer):
    username = serializers.CharField()
    can_read = serializers.BooleanField(
        default=False,
    )
    can_update = serializers.BooleanField(
        default=False,
    )


class AssigneeRemoveSerializer(serializers.Serializer):
    username = serializers.CharField()

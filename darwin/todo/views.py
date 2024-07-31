from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo.models import Task
from todo.permissions import IsOwner, HasTaskPermission
from todo.serializers import TaskSerializer, AssigneeAddSerializer, \
    AssigneeRemoveSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasTaskPermission | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user) | Task.objects.filter(
            assignees=user)

    @action(detail=True, methods=['post'])
    def add_assignee(self, request, pk):
        task = self.get_object()
        serializer = AssigneeAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        can_read = serializer.validated_data['can_read']
        can_update = serializer.validated_data['can_update']
        task.add_assignee(username, can_read, can_update)
        return Response({'status': 'assignee added',
                         'assignee': serializer.data},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_assignee(self, request, pk):
        task = self.get_object()
        serializer = AssigneeRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        task.remove_assignee(username)
        return Response({'status': 'assignee removed',
                         'assignee': serializer.data},
                        status=status.HTTP_200_OK)

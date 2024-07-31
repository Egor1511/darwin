from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Title",
    )
    description = models.TextField(
        verbose_name="Description",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )
    owner = models.ForeignKey(
        User,
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name="Owner",
    )
    assignees = models.ManyToManyField(
        User,
        through='TaskAssignee',
        related_name='assigned_tasks',
        through_fields=('task', 'user'),
        verbose_name="Assignees",
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title

    def add_assignee(self, username, can_read=False, can_update=False):
        user = User.objects.get(username=username)
        TaskAssignee.objects.create(task=self, user=user, can_read=can_read,
                                    can_update=can_update)

    def remove_assignee(self, username):
        user = User.objects.get(username=username)
        TaskAssignee.objects.filter(task=self, user=user).delete()


class TaskAssignee(models.Model):
    user = models.ForeignKey(
        User,
        related_name='taskassignee_set',
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    task = models.ForeignKey(
        Task,
        related_name='taskassignee_set',
        on_delete=models.CASCADE,
        verbose_name="Task",
    )
    can_update = models.BooleanField(
        default=False,
    )
    can_read = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ('task', 'user')
        verbose_name = "Task assignee"
        verbose_name_plural = "Task assignees"
        unique_together = ('user', 'task')

    def __str__(self):
        return f'{self.task[:50]} - {self.user}'

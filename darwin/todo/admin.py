from django.contrib import admin

from .models import Task, TaskAssignee


class TaskAssigneeInline(admin.TabularInline):
    model = TaskAssignee
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'owner__username')
    inlines = [TaskAssigneeInline]


@admin.register(TaskAssignee)
class TaskAssigneeAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'can_read', 'can_update')
    search_fields = ('task__title', 'user__username')

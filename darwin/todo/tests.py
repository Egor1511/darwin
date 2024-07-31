import os

import django
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from todo.models import Task, TaskAssignee

os.environ['DJANGO_SETTINGS_MODULE'] = 'darwin.settings'
django.setup()


class AccountTests(APITestCase):
    def test_create_account(self):
        url = reverse('rest_register')
        data = {
            "username": "newuser",
            "password1": "yourpassword",
            "password2": "yourpassword",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_login(self):
        self.test_create_account()
        url = reverse('rest_login')
        data = {
            'username': 'newuser',
            'password': 'yourpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)


class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='newuser11',
                                             password='yourpassword')
        self.assignee = User.objects.create_user(username='newuser22',
                                                 password='yourpassword')
        response = self.client.post(reverse('rest_login'),
                                    {'username': 'newuser11',
                                     'password': 'yourpassword'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.task = Task.objects.create(title='Test Task',
                                        description='Test Description',
                                        owner=self.user)

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.get(id=response.data['id']).title,
                         'New Task')

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_add_assignee(self):
        url = reverse('task-add-assignee', args=[self.task.id])
        data = {
            'username': 'newuser22',
            'can_read': True,
            'can_update': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TaskAssignee.objects.filter(task=self.task,
                                                    user=self.assignee).exists())

    def test_remove_assignee(self):
        TaskAssignee.objects.create(task=self.task, user=self.assignee,
                                    can_read=True, can_update=False)
        url = reverse('task-remove-assignee', args=[self.task.id])
        data = {
            'username': 'newuser22'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TaskAssignee.objects.filter(task=self.task,
                                                     user=self.assignee).exists())


class AssigneeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(username='owner',
                                              password='password123')
        self.assignee = User.objects.create_user(username='assignee',
                                                 password='password123')
        response = self.client.post(reverse('rest_login'),
                                    {'username': 'assignee',
                                     'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.task = Task.objects.create(title='Test Task',
                                        description='Test Description',
                                        owner=self.owner)
        TaskAssignee.objects.create(task=self.task, user=self.assignee,
                                    can_read=True, can_update=True)

    def test_get_assigned_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_assigned_task(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task by Assignee',
            'description': 'Updated Description by Assignee'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task by Assignee')

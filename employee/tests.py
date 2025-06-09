from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from datetime import date, timedelta

# Create your tests here.
class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(
            title='Test Task',
            description='Some description.',
            assigned_to=self.user,
            due_date=date.today() + timedelta(days=3),
        )

    def test_task_created(self):
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(self.task.assigned_to.username, 'testuser')
    
    def test_task_default_status(self):
        self.assertEqual(self.task.status, 'pending')
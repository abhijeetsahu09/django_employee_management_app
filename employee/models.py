from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from client.models import Client

# Create your models here.
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_joined = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('active', "Active"),
        ('on_leave', 'On Leave'),
        ('resigned', 'Resigned'),
    ])
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True,
                                        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return f"{self.user} - {self.designation}"
    
 
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')
    upload = models.FileField(
        upload_to='task_uploads/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'zip', 'jpg', 'png'])]
    )

    def __str__(self):
        return f"{self.title} -> {self.assigned_to.username}"
    
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.check_in.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-check_in']


LEAVE_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS, default='pending')
    manager_comment = models.TextField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

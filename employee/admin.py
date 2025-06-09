from django.contrib import admin
from .models import EmployeeProfile, Task

# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(Task)
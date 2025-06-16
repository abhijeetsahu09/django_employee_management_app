from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from employee.models import EmployeeProfile, Task, Attendance, LeaveRequest
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('task_list')
        
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In!")
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('task_list')
        else:
            messages.error(request, "There was an error logging you in!, Please try again....")
            return redirect('home')
    else:
        return render(request, 'home.html')

# def login_user(request):
#     pass 

def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out.....")
    return redirect('home')

def is_admin_or_hr(user):
    return user.is_superuser or user.groups.filter(name="HR").exists()

@login_required
@user_passes_test(is_admin_or_hr)
def hr_dashboard(request):
    total_employees = EmployeeProfile.objects.count()
    total_tasks = Task.objects.count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    today_attendance = Attendance.objects.filter(check_in__date=timezone.now().date()).count()

    return render(request, 'employee/hr_dashboard.html', {
        'total_employees': total_employees,
        'total_tasks': total_tasks,
        'pending_leaves': pending_leaves,
        'today_attendance': today_attendance
    })
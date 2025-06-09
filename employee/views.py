from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task, EmployeeProfile, Attendance, LeaveRequest
from .forms import TaskForm, EmployeeCreationForm, EmployeeUpdateForm, AttendanceReportForm, LeaveRequestForm, LeaveApprovalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import openpyxl
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required
def employee_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can view the employee list.")
        return redirect('task_list')

    employees = EmployeeProfile.objects.select_related('user')
    return render(request, 'employee/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    try:
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to view employee details.")
            return redirect('employee_list')
        employee = get_object_or_404(EmployeeProfile, pk=pk)
        return render(request, 'employee/employee_detail.html', {'employee': employee})
    except Exception as e:
        messages.error(request, f"An error occured: {str(e)}")
        return redirect('employee_list')

@login_required
def add_employee(request):
    try:
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to add employees.")
            return redirect('task_list')

        form = EmployeeCreationForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Employee added successfully!")
                return redirect('task_list')

        return render(request, 'employee/add_employee.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('task_list')
    
@login_required
def update_employee(request, pk):
    try:
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to update employees.")
            return redirect('employee_list')
        employee = get_object_or_404(EmployeeProfile, pk=pk)
        form = EmployeeUpdateForm(request.POST or None, request.FILES or None, instance=employee)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Employee updated successfully.")
                return redirect('employee_list')
        return render(request, 'employee/update_employee.html', {'form': form, 'employee': employee})
    except Exception as e:
        messages.error(request, f"An error occured: {str(e)}")
        return redirect('employee_list')

@login_required
def task_list(request):
    try:
        if request.user.is_superuser:
            tasks = Task.objects.all()
            employees = User.objects.filter(is_superuser=False)

            assigned_to = request.GET.get('assigned_to')
            status = request.GET.get('status')

            if assigned_to:
                tasks = tasks.filter(assigned_to_id=assigned_to)
            if status:
                tasks = tasks.filter(status=status)
            context =  {
                'tasks': tasks,
                'employees': employees,
            }
        else:
            tasks = Task.objects.filter(assigned_to=request.user)
            context = {
                'tasks': tasks,
                'employees': User.objects.none(),
            }
        return render(request, 'employee/task_list.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def create_task(request):
    try:
        if not request.user.is_superuser:
            return redirect('task_list')
        
        form = TaskForm(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        return render(request, 'employee/task_form.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('task_list')

@login_required
def update_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)

        if request.user != task.assigned_to and not request.user.is_superuser:
            return redirect('task_list')
        
        form = TaskForm(request.POST or None, request.FILES or None, instance=task, user=request.user)
        if form.is_valid():
            if not request.user.is_superuser:
                form.instance.assigned_to = task.assigned_to
            form.save()
            return redirect('task_list')
        return render(request, 'employee/task_form.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('task_list')
    

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized")
        return redirect('home')

    total_employees = EmployeeProfile.objects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()

    return render(request, 'employee/dashboard.html', {
        'total_employees': total_employees,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
    })
 
@login_required
def delete_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        if request.user != task.assigned_to and not request.user.is_superuser:
            messages.error(request, "You are not authorized to delete this task.")
            return redirect('task_list')
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('task_list')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('task_list')

@login_required
def delete_employee(request, pk):
    try:
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to delete employees.")
            return redirect('employee_list')
        employee = get_object_or_404(EmployeeProfile, pk=pk)
        employee.user.delete()  # This will also delete EmployeeProfile due to OneToOneField
        messages.success(request, "Employee deleted successfully.")
        return redirect('employee_list')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('employee_list')


@login_required
def check_in(request):
    existing = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
    if existing:
        messages.warning(request, "You are already checked in!")
    else:
        Attendance.objects.create(user=request.user)
        messages.success(request, "Checked in successfully.")
    return redirect('attendance_list')

@login_required
def check_out(request):
    existing = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
    if existing:
        existing.check_out = timezone.now()
        existing.save()
        messages.success(request, "Checked out successfully.")
    else:
        messages.warning(request, "No active check-in found.")
    return redirect('attendance_list')

@login_required
def attendance_list(request):
    records = Attendance.objects.all()
    employees = User.objects.filter(is_superuser=False)
    if request.user.is_superuser:
        employee_id = request.GET.get('employee')
        if employee_id:
            records = records.filter(user_id=employee_id)
    else:
        records = records.filter(user=request.user)
        employees = None
    return render(request, 'employee/attendance_list.html', {
        'records': records,
        'employees': employees,
    })

@login_required
def export_attendance_excel(request):
    if not request.user.is_superuser:
        return redirect('attendance_list')

    form = AttendanceReportForm(request.GET)
    employee_id = request.GET.get('employee')
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        data = Attendance.objects.filter(check_in__date__range=(start, end))
        if employee_id:
            data = data.filter(user_id=employee_id)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Attendance"

        ws.append(['Name', 'Check-In', 'Check-Out'])

        for record in data:
            ws.append([
                record.user.get_full_name(),
                record.check_in.strftime("%Y-%m-%d %H:%M"),
                record.check_out.strftime("%Y-%m-%d %H:%M") if record.check_out else "N/A"
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.xlsx"'
        wb.save(response)
        return response
    else:
        return redirect('attendance_list')
    
@login_required
def export_attendance_pdf(request):
    if not request.user.is_superuser:
        return redirect('attendance_list')

    form = AttendanceReportForm(request.GET)
    employee_id = request.GET.get('employee')
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        data = Attendance.objects.filter(check_in__date__range=(start, end))
        if employee_id:
            data = data.filter(user_id=employee_id) 

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        p.drawString(200, 800, "Attendance Report")

        y = 770
        p.setFont("Helvetica", 10)
        for record in data:
            p.drawString(50, y, f"{record.user.get_full_name()} | {record.check_in} - {record.check_out or 'N/A'}")
            y -= 20
            if y < 50:
                p.showPage()
                y = 770

        p.showPage()
        p.save()
        return response
    else:
        return redirect('attendance_list')

@login_required
def request_leave(request):
    form = LeaveRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        leave = form.save(commit=False)
        leave.user = request.user
        leave.save()

        messages.success(request, "Leave requested successfully.")
        return redirect('leave_list')
    return render(request, 'employee/request_leave.html', {'form': form})

@login_required
def leave_list(request):
    if request.user.is_superuser:
        leaves = LeaveRequest.objects.select_related('user').order_by('-requested_at')
    else:
        leaves = LeaveRequest.objects.filter(user=request.user).order_by('-requested_at')
    return render(request, 'employee/leave_list.html', {'leaves': leaves})


@login_required
def review_leave(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized")
        return redirect('leave_list')

    leave = get_object_or_404(LeaveRequest, pk=pk)
    approval_form = LeaveApprovalForm(request.POST or None, instance=leave)
    email_sent = False

    if request.method == 'POST' and approval_form.is_valid():
        leave = approval_form.save(commit=False)
        leave.responded_at = timezone.now()
        leave.save()

        # Manual email fields
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if 'change_status' in request.POST:
            messages.success(request, "Leave status updated successfully.")
            return redirect('leave_list')
        elif 'change_status_and_email' in request.POST:
            from_email = request.POST.get('from_email')
            to_email = request.POST.get('to_email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            if from_email and to_email and subject and message:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[to_email],
                    fail_silently=False
                )
                email_sent = True
                messages.success(request, "Leave status updated and email sent successfully.")
            else:
                messages.warning(request, "Email not sent. Please fill all email fields.")
            return redirect('leave_list')

    return render(request, 'employee/review_leave.html', {
        'form': approval_form,
        'leave': leave,
        'email_sent': email_sent
    })
from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/update/', views.update_task, name='update_task'),
    path('add/', views.add_employee, name='add_employee'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/update/', views.update_employee, name='update_employee'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('employee/<int:pk>/delete/', views.delete_employee, name='delete_employee'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/checkin/', views.check_in, name='check_in'),
    path('attendance/checkout/', views.check_out, name='check_out'),
    path('attendance/export/pdf/', views.export_attendance_pdf, name='export_attendance_pdf'),
    path('attendance/export/excel/', views.export_attendance_excel, name='export_attendance_excel'),
    path('leave/request/', views.request_leave, name='request_leave'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/review/<int:pk>/', views.review_leave, name='review_leave'),
]

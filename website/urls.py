from django.urls import path  # new
from . import views  # new

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('add/', views.add_client, name='add_client'),
    path('<int:pk>/', views.client_detail, name='client_detail'),
    path('<int:pk>/edit/', views.update_client, name='update_client'),
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
]
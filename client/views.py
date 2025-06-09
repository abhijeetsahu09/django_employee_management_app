from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client
from .forms import ClientForm
import os
from django.db.models import Sum

@login_required
def client_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access client data.")
        return redirect('home')
    clients = Client.objects.all()
    return render(request, 'client/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access client data.")
        return redirect('home')
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})

@login_required
def add_client(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access client data.")
        return redirect('home')
    form = ClientForm(request.POST or None, request.FILES or None)  # <-- Add request.FILES
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, 'client/client_form.html', {'form': form})

@login_required
def update_client(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access client data.")
        return redirect('home')
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, request.FILES or None, instance=client) 
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, 'client/client_form.html', {'form': form, 'client': client})

@login_required
def delete_client(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access client data.")
        return redirect('home')
    client = get_object_or_404(Client, pk=pk)
    if client.logo and os.path.isfile(client.logo.path):
        os.remove(client.logo.path)
    client.delete()
    messages.success(request, "Client deleted successfully.")
    return redirect('client_list')

@login_required
def client_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access client dashboard.")
        return redirect('home')
    all_clients = Client.objects.all()
    active_clients = Client.objects.filter(status='active')
    old_clients = Client.objects.filter(status='old')
    total_pending_amount = Client.objects.aggregate(total=Sum('pending_amount'))['total'] or 0
    total_paid_amount = Client.objects.aggregate(total=Sum('paid_amount'))['total'] or 0
    return render(request, 'client/client_dashboard.html', {
        'all_clients': all_clients,
        'active_clients': active_clients,
        'old_clients': old_clients,
        'total_pending_amount': total_pending_amount,
        'total_paid_amount': total_paid_amount,
    })
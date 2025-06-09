from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'company', 'address', 'paid_amount', 'pending_amount','status', 'work_completed', 'notes', 'logo']
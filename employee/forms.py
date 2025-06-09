from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile, Task, Attendance, LeaveRequest


class EmployeeCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    profile_picture = forms.ImageField(required=False)
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: DD-MM-YYYY"
    )

    class Meta:
        model = EmployeeProfile
        fields = ['designation', 'department', 'date_joined', 'status', 'profile_picture']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        profile = super(EmployeeCreationForm, self).save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile
    
class EmployeeUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the current password.")
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: DD-MM-YYYY"
    )

    class Meta:
        model = EmployeeProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'designation', 'department', 'date_joined', 'status', 'profile_picture']

    def __init__(self, *args, **kwargs):
        # Expecting instance to be an EmployeeProfile
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            profile.save()
        return profile
    
class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: DD-MM-YYYY"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'upload', 'client']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['assigned_to'].disabled = True
            self.fields['due_date'].disabled = True
            self.fields['client'].disabled = True

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = []

class AttendanceReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class LeaveRequestForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: DD-MM-YYYY"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: DD-MM-YYYY"
    )
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'manager_comment']

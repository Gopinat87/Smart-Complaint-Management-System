from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Complaint, ComplaintUpdate


class RegisterForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class ComplaintForm(forms.ModelForm):
    class Meta:
        model  = Complaint
        fields = ['category', 'title', 'description', 'location', 'priority', 'attachment']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief title of your complaint'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Describe the issue in detail…'}),
            'location':    forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Block / Room / Area (optional)'}),
            'category':    forms.Select(attrs={'class': 'form-input'}),
            'priority':    forms.Select(attrs={'class': 'form-input'}),
            'attachment':  forms.FileInput(attrs={'class': 'form-input'}),
        }


class UpdateStatusForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Add a note about this status change…'}),
        required=False
    )

    class Meta:
        model  = Complaint
        fields = ['status', 'priority']
        widgets = {
            'status':   forms.Select(attrs={'class': 'form-input'}),
            'priority': forms.Select(attrs={'class': 'form-input'}),
        }

from django import forms
from .models import Task,Registration


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_name', 'description', 'priority', 'assignee', 'completion_status')
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assignee': forms.TextInput(attrs={'class': 'form-control'}),
            'completion_status': forms.CheckboxInput(),
        }
from django.contrib.auth.models  import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username=forms.CharField(error_messages='',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=('username','email')    
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']        
        

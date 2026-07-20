from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username' : 'Username',
            'email' : 'Email',
            'password1': 'Password',
            'password2' : 'Confirm Password',
        }

        for field,placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({
                'placeholder' : placeholder,
                'class' : 'form-control',
            })
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Username',
            'password': 'Password',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({
                'placeholder': placeholder,
                'class': 'form-control',
            })
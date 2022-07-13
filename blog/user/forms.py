from django import forms
from django.contrib import messages
from django.template.context_processors import request

from .models import User


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'phone_number', 'date_of_birth', 'sex']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["email"] in User.objects.all().values_list('email', flat=True):
            raise forms.ValidationError('User with this email already exists')
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd["password2"]


class AuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
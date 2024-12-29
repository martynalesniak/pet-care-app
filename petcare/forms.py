# petcare/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Załóżmy, że masz własny model User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = User  # Używamy własnego modelu użytkownika
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

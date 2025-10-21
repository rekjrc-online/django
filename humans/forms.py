from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Human

class HumanRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = Human
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

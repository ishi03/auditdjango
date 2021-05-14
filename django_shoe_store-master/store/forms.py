
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ShippingAddress

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
class Aform(forms.ModelForm):
    class Meta:
        model=ShippingAddress
        fields=['customer','address','city','state','zipcode']
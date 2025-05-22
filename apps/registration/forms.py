from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from apps.property.models import Property, PropertyImage


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['category', 'title', 'image', 'thumbnail', 'description',  'price']

class PropertyImageForm(ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image','thumbnail']


# In registration/forms.py
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']  # Add more fields as required
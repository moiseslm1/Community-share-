from django import forms
from .models import JobListing, Service, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobListing, Service, ServiceRequest 

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company', 'location', 'description', 'salary']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'address', 'zip_code', 'phone_number']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
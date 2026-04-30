from django import forms
from .models import JobListing, Service, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company', 'location', 'description', 'salary']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'zip_code']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]
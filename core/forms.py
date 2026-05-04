from django import forms
from .models import JobListing, Service, ServiceRequest, UserProfile, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company', 'location', 'description', 'salary']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'address', 'zip_code', 'phone_number']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'category', 'zip_code']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['job_title', 'date_of_birth', 'city', 'zipcode', 'biography']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 4}),
        }

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    
    class Meta:
        model = UserProfile
        fields = ['job_title', 'date_of_birth', 'city', 'zipcode', 'biography']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 4}),
        }

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Service, ServiceRequest, UserProfile, UserJobHistory
from .forms import ServiceForm, ServiceRequestForm, SignUpForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import json
import random
import requests as http_requests

CATEGORIES = {
    'assembly': {
        'name': 'Assembly',
        'icon': 'fa-solid fa-screwdriver-wrench',
        'description': 'Furniture, shelves, desks',
        'details': 'Need help assembling furniture or mounting shelves? Our community can help with furniture assembly, desk setup, and more.'
    },
    'mounting': {
        'name': 'Mounting',
        'icon': 'fa-solid fa-tv',
        'description': 'TVs, frames, shelves',
        'details': 'Get help mounting TVs, hanging picture frames, and installing shelves safely in your home.'
    },
    'cleaning': {
        'name': 'Cleaning',
        'icon': 'fa-solid fa-broom',
        'description': 'Home & Apartment',
        'details': 'Need professional or community help cleaning your home? From deep cleaning to regular maintenance.'
    },
    'outdoor-maintenance': {
        'name': 'Outdoor Maintenance',
        'icon': 'fa-solid fa-leaf',
        'description': 'Gardens, Lawn care',
        'details': 'Keep your outdoor space beautiful with help from community members experienced in gardening and lawn care.'
    },
    'repairs': {
        'name': 'Repairs',
        'icon': 'fa-solid fa-hammer',
        'description': 'Fixes & small jobs',
        'details': 'Get help with home repairs, appliance fixes, and other maintenance tasks.'
    },
    'moving': {
        'name': 'Moving',
        'icon': 'fa-solid fa-truck',
        'description': 'Heavy lifting & transport',
        'details': 'Moving to a new place? Get help with heavy lifting, packing, and transportation.'
    },
    'cooking': {
        'name': 'Cooking',
        'icon': 'fa-solid fa-utensils',
        'description': 'Home Cooked Meals',
        'details': 'Need meal preparation services? Community members can help with cooking, meal prep, and catering.'
    },
}


def home(request):
    return render(request, "home.html")


def feed(request):
    category = request.GET.get('category', '').strip()
    services = Service.objects.all()
    requests_qs = ServiceRequest.objects.all()

    if category:
        services = services.filter(category=category)
        requests_qs = requests_qs.filter(category=category)

    services_with_coords    = [s for s in services if s.latitude and s.longitude]
    services_without_coords = [s for s in services if not s.latitude or not s.longitude]

    map_pins = json.dumps([
        {
            'name': s.title,
            'category': s.get_category_display(),
            'zip': s.zip_code,
            'phone': s.phone_number,
            'coords': [
                s.longitude + random.uniform(-0.003, 0.003),
                s.latitude  + random.uniform(-0.003, 0.003),
            ],
        }
        for s in services_with_coords
    ])

    return render(request, 'feed.html', {
        'services': services,
        'services_with_coords': services_with_coords,
        'services_without_coords': services_without_coords,
        'requests': requests_qs,
        'map_pins': map_pins,
    })


def guidelines(request):
    return render(request, "guidelines.html")


@login_required
def request_service(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.posted_by = request.user
            service_request.save()
            return redirect('feed')
    else:
        form = ServiceRequestForm()
    return render(request, 'request.html', {'form': form})


def offer(request):
    return render(request, "offer.html")


def events(request):
    return render(request, "events.html")


def results(request):
    query    = request.GET.get('q', '').strip()
    zip_code = request.GET.get('zip', '').strip()
    category = request.GET.get('category', '').strip()

    services    = Service.objects.none()
    requests_qs = ServiceRequest.objects.none()
    searched    = False

    if query or zip_code or category:
        searched = True
        services = Service.objects.all()
        requests_qs = ServiceRequest.objects.all()

        if query:
            services = services.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
            requests_qs = requests_qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        if zip_code:
            services = services.filter(zip_code=zip_code)
            requests_qs = requests_qs.filter(zip_code=zip_code)
        if category:
            services = services.filter(category=category)
            requests_qs = requests_qs.filter(category=category)

    services_with_coords    = [s for s in services if s.latitude and s.longitude]
    services_without_coords = [s for s in services if not s.latitude or not s.longitude]

    map_pins = json.dumps([
        {
            'name': s.title,
            'category': s.get_category_display(),
            'zip': s.zip_code,
            'phone': s.phone_number,
            'coords': [
                s.longitude + random.uniform(-0.003, 0.003),
                s.latitude  + random.uniform(-0.003, 0.003),
            ],
        }
        for s in services_with_coords
    ])

    return render(request, 'results.html', {
        'services': services,
        'services_with_coords': services_with_coords,
        'services_without_coords': services_without_coords,
        'requests': requests_qs,
        'query': query,
        'zip_code': zip_code,
        'searched': searched,
        'map_pins': map_pins,
    })


def category(request, category_slug):
    cat = CATEGORIES.get(category_slug)
    services = Service.objects.filter(category=category_slug)
    return render(request, 'category.html', {'category': cat, 'slug': category_slug, 'services': services})


@login_required
def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.posted_by = request.user

            address = (form.cleaned_data.get('address') or '') + ', ' + form.cleaned_data.get('zip_code') + ', USA'
            try:
                geo = http_requests.get(
                    'https://nominatim.openstreetmap.org/search',
                    params={'q': address, 'format': 'json', 'limit': 1},
                    headers={'User-Agent': 'LightningQuest/1.0'},
                    timeout=5
                ).json()
                if geo:
                    service.latitude  = float(geo[0]['lat'])
                    service.longitude = float(geo[0]['lon'])
            except Exception:
                pass

            service.save()
            return redirect('home')
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required
def profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'Profile.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def job_history(request):
    from datetime import datetime, timedelta
    
    # Get jobs from the last year
    one_year_ago = datetime.now().date() - timedelta(days=365)
    jobs = UserJobHistory.objects.filter(
        user=request.user,
        start_date__gte=one_year_ago
    ).order_by('-start_date')
    
    # Calculate statistics
    current_jobs = jobs.filter(is_current=True).count()
    completed_jobs = jobs.filter(end_date__isnull=False).count()
    
    return render(request, 'job_history.html', {
        'jobs': jobs,
        'one_year_ago': one_year_ago,
        'current_jobs': current_jobs,
        'completed_jobs': completed_jobs,
    })
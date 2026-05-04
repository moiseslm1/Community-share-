from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Service, ServiceRequest, UserProfile, UserJobHistory, Post
from .forms import ServiceForm, ServiceRequestForm, SignUpForm, UserProfileForm, PostForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import json
import random
import requests as http_requests
from .models import Service, ServiceRequest, UserProfile, UserJobHistory, Post, Booking
from django.contrib import messages

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
    posts = Post.objects.order_by("-created_at")
    return render(request, "events.html", {"posts": posts})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("events")
    else:
        form = PostForm()


    return render(request, "create_post.html", {"form": form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)


    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)


    return redirect("events")


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)


    # only allow the owner to delete
    if post.user != request.user:
        return redirect("events")


    if request.method == "POST":
        post.delete()


    return redirect("events")


def results(request):
    query    = request.GET.get('q', '').strip()
    zip_code = request.GET.get('zip', '').strip()
    category = request.GET.get('category', '').strip()


    services = Service.objects.none()
    searched = False


    if query or zip_code or category:
        searched = True
        services = Service.objects.all()


        if query:
            services = services.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        if zip_code:
            services = services.filter(zip_code=zip_code)
        if category:
            services = services.filter(category=category)


    return render(request, 'results.html', {
        'services': services,
        'query': query,
        'zip_code': zip_code,
        'searched': searched,
    })


def category(request, category_slug):
    cat = CATEGORIES.get(category_slug)
    return render(request, 'category.html', {'category': cat, 'slug': category_slug})


@login_required
def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)


        if form.is_valid():
            service = form.save(commit=False)
            service.posted_by = request.user
            service.save()
            return redirect("home")
    else:
        form = ServiceForm()


    return render(request, "create_service.html", {"form": form})

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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Update user first and last name
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

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

def job_listing_view(request):
    return render(request, 'job_listing.html')

def account_view(request):
    return render(request, 'account.html')

@login_required
def incoming_requests(request):
    """
    Shows a service provider all ServiceRequests that match ANY of the
    categories of services THEY have posted — i.e. their "inbox" of jobs.
    Also shows which ones they have already accepted (Booking exists).
    """
    # Find which categories the logged-in user offers
    my_categories = (
        Service.objects
        .filter(posted_by=request.user)
        .values_list('category', flat=True)
        .distinct()
    )
 
    # All open requests in those categories (excluding their own)
    open_requests = (
        ServiceRequest.objects
        .filter(category__in=my_categories)
        .exclude(posted_by=request.user)
        .order_by('-created_at')
    )
 
    # Which request IDs has this provider already accepted?
    accepted_ids = set(
        Booking.objects
        .filter(user=request.user)
        .values_list('service_request_id', flat=True)
    )
 
    return render(request, 'incoming_requests.html', {
        'open_requests': open_requests,
        'accepted_ids': accepted_ids,
        'my_categories': list(my_categories),
    })
 
 
@login_required
def accept_request(request, request_id):
    """
    Provider accepts a ServiceRequest → creates a Booking.
    Idempotent: a second accept just redirects without creating a duplicate.
    """
    service_request = get_object_or_404(ServiceRequest, id=request_id)
 
    # Don't let someone accept their own request
    if service_request.posted_by == request.user:
        messages.error(request, "You can't accept your own request.")
        return redirect('incoming_requests')
 
    already = Booking.objects.filter(
        user=request.user,
        service_request=service_request,
    ).exists()
 
    if not already:
        Booking.objects.create(
            user=request.user,
            service_request=service_request,
        )
        messages.success(
            request,
            f"You accepted \"{service_request.title}\" — "
            f"reach out to {service_request.posted_by.username} to coordinate!"
        )
    else:
        messages.info(request, "You already accepted this request.")
 
    return redirect('incoming_requests')
 
 
@login_required
def decline_request(request, request_id):
    """
    Provider removes their acceptance (un-accepts) if they change their mind.
    """
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    Booking.objects.filter(
        user=request.user,
        service_request=service_request,
    ).delete()
    messages.info(request, f"You un-accepted \"{service_request.title}\".")
    return redirect('incoming_requests')

from django.shortcuts import render, redirect
from .forms import JobListingForm

# Category data
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
    return render (request, "home.html")

def feed(request):
    return render(request, "feed.html")

def guidelines(request):
    return render(request, "guidelines.html")

def request(request):
    return render(request, "request.html")

def offer(request):
    return render(request, "offer.html")
    
def events(request):
    return render(request, "events.html")

def category(request, category_slug):
    category = CATEGORIES.get(category_slug)
    if not category:
        return redirect('home')
    return render(request, 'category.html', {'category': category, 'slug': category_slug})

def results(request):
    return render(request, 'results.html')

def create_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JobListingForm()

    return render(request, 'offer.html', {'form': form})
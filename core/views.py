from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Service
from .forms import JobListingForm

# ... CATEGORIES dict stays the same ...

def home(request):
    return render(request, "home.html")

def feed(request):
    return render(request, "feed.html")

def guidelines(request):
    return render(request, "guidelines.html")

def request_service(request):        # ← renamed
    return render(request, "request.html")

def offer(request):
    return render(request, "offer.html")

def events(request):
    return render(request, "events.html")

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
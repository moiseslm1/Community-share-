from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Service, Post
from .forms import ServiceForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, PostForm
from django.contrib.auth import login

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
    return render(request, "feed.html")

def guidelines(request):
    return render(request, "guidelines.html")

def request_service(request):        # ← renamed
    return render(request, "request.html")

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
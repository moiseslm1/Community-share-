from django.shortcuts import render, redirect
from .forms import JobListingForm

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

def create_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JobListingForm()

    return render(request, 'offer.html', {'form': form})
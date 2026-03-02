from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def feed(request):
    return render(request, "feed.html")

def guidelines(request):
    return render(request, "guidelines.html")

def request(request):
    return render(request, "request.html")

def offer(request):
    return render(request, "offer.html")

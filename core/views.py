from django.http import HttpResponse

def home(request):
  return HttpResponse("Welcome to Community Share! Choose: Request Help or Offer Service")

def feed(request):
  return HttpResponse("This is the feed page.")

# Create your views here.

from django.contrib import admin
from .models import JobListing, Service, Booking, Review, ServiceRequest

admin.site.register(JobListing)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(ServiceRequest)
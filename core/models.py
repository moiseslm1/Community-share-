from django.db import models
from django.contrib.auth.models import User

class JobListing(models.Model):
    title       = models.CharField(max_length=200)
    company     = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    description = models.TextField()
    salary      = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('assembly',            'Assembly'),
        ('mounting',            'Mounting'),
        ('cleaning',            'Cleaning'),
        ('outdoor-maintenance', 'Outdoor Maintenance'),
        ('repairs',             'Repairs'),
        ('moving',              'Moving'),
        ('cooking',             'Cooking'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    zip_code    = models.CharField(max_length=10)
    latitude    = models.FloatField(null=True, blank=True)
    longitude   = models.FloatField(null=True, blank=True)
    posted_by   = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.zip_code})"

class Booking(models.Model):
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.service.title}"

class Review(models.Model):
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.IntegerField()
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars for {self.service.title}"
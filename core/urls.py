from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("guidelines/", views.guidelines, name="guidelines"),
    path("offer/", views.offer, name="offer"),
    path("request/", views.request, name="request"),
    path("events/", views.events, name="events"),
    path('jobs/create/', views.offer, name='create_job'),
]

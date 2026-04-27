from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("results/", views.results, name="results"),
    path("guidelines/", views.guidelines, name="guidelines"),
    path("offer/", views.offer, name="offer"),
    path("request/", views.request_service, name="request"),
    path("events/", views.events, name="events"),
    path("category/<str:category_slug>/", views.category, name="category"),
    path('jobs/create/', views.offer, name='create_job'),
    path('create-service/', views.create_service, name='create_service'),
    path('signup/', views.signup, name='signup'),
]

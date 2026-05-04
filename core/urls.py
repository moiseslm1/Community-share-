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
    path("create-post/", views.create_post, name="create_post"),    
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("category/<str:category_slug>/", views.category, name="category"),
    path('jobs/create/', views.offer, name='create_job'),
    path('create-service/', views.create_service, name='create_service'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('job-history/', views.job_history, name='job_history'),
    path('requests/incoming/', views.incoming_requests, name='incoming_requests'),
    path('requests/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('requests/decline/<int:request_id>/', views.decline_request, name='decline_request'),
]

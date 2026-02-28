from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
<<<<<<< HEAD
]
=======
]
>>>>>>> bd3f32f61ee5cc00bb1938241b355da2a1405168

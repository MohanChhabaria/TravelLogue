from django.urls import path
from . import views

urlpatterns = [
    path('details/', views.UserDetails.as_view(), name="user-details"),
    path('connections/', views.UserFollowingDetails.as_view(), name='connections'),
]
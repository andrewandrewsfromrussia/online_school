from django.urls import path
from .views import UserProfileUpdateView

urlpatterns = [
    path("profile/int:pk/", UserProfileUpdateView.as_view(), name="profile-edit")
]
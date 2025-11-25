from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserProfileUpdateView, PaymentViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="profile-edit"),
    path("", include(router.urls)),
]
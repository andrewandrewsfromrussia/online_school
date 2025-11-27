from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserProfileUpdateView, PaymentViewSet, UserRegisterAPIView

app_name = "users"

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="profile-edit"),
    path("", include(router.urls)),
]
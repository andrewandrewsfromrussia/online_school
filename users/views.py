from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User, Payment
from .serializers import (
    UserSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    PublicUserSerializer,
)
from .permissions import IsSelfOrReadOnly


class UserRegisterAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    Просмотр любого профиля, редактирование только своего.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        return PublicUserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = [
        "paid_course",
        "paid_lesson",
        "payment_method",
    ]

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]

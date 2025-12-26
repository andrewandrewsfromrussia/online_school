from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView

from .models import User, Payment
from .serializers import (
    UserSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    PublicUserSerializer,
)
from .permissions import IsSelfOrReadOnly

from lms.services import create_stripe_product, create_stripe_price, create_stripe_session


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
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        return PublicUserSerializer


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product_name = "Donation"
        product_price = 0

        if payment.paid_course:
            product_name = payment.paid_course.title
            product_price = payment.paid_course.price
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.title
            product_price = payment.paid_lesson.price

        stripe_product_id = create_stripe_product(product_name)
        stripe_price_id = create_stripe_price(product_price, stripe_product_id)
        session_id, payment_link = create_stripe_session(stripe_price_id)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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

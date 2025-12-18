from rest_framework import serializers
from .models import User, Payment

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
            "session_id",
            "link",
        )
        read_only_fields = ("id", "user", "payment_date", "session_id", "link")

class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password")

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Урезанный профиль для чужих пользователей.
    """
    class Meta:
        model = User
        fields = ("id", "email", "city", "avatar")

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .models import Todo


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description"]


class TodoDetailSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "completed"]


class RegisterSerializer(serializers.Serializer):
    # password2 = serializers.CharField(
    #     write_only=True, required=True, style={"input_type": "password"}
    # )
    name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    # class Meta:
    #     model = User
    #     fields = [
    #         # "name",
    #         "email",
    #         "password",
    #         # "password2",
    #     ]
    #     extra_kwargs = {
    #         "password": {"write_only": True, "style": {"input_type": "password"}},
    #         "email": {"required": True},
    #         # "name": {"required": True},
    #     }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["name"],
        )
        return user

    def validate_email(self, value):
        email_lower = value.lower()
        if User.objects.filter(username=email_lower).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def to_representation(self, instance):
        return {
            "name": instance.first_name,
            "email": instance.email,
        }

    # def validate(self, attrs):
    #     password2 = attrs.pop("password2")
    #     if attrs["password"] != password2:
    #         raise serializers.ValidationError({"password": "Passwords do not match."})
    #     validate_password(attrs["password"], user=User(username=attrs["username"]))
    #     return attrs


# add email serializer to make user login with email and password
class EmailLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email and password are required.")

        user = authenticate(email=email, password=password)

        # Find the user by their email
        # try:
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     raise AuthenticationFailed(
        #         "No active account found with the given credentials"
        #     )

        # Authentication
        authenticated_user = authenticate(username=email, password=password)

        if not authenticated_user:
            raise AuthenticationFailed(
                "No active account found with the given credentials"
            )

        if not authenticated_user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        refresh = RefreshToken.for_user(authenticated_user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": authenticated_user,
        }

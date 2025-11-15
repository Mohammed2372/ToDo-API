from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Todo


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description"]


class TodoDetailSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class RegisterSerializer(ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "email": {"required": True},
            "username": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

    def validate(self, attrs):
        password2 = attrs.pop("password2")
        if attrs["password"] != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        validate_password(attrs["password"], user=User(username=attrs["username"]))
        return attrs

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # ensures password is hashed properly
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "message", "is_read", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "role",
                  "secret_link", "messages", "created_at"]
        read_only_fields = ["id", "role", "secret_link"]


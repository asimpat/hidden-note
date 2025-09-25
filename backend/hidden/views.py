from hidden.serializers import RegisterSerializer, UserSerializer, MessageSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Message


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])  
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # serialize user to return safe info
        user_data = UserSerializer(user).data
        return Response(
            {
                "message": "User registered successfully",
                "user": user_data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_message(request, secret_link):
    try:
        user = User.objects.get(secret_link=secret_link)
    except User.DoesNotExist:
        return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_messages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
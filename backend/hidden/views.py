from hidden.serializers import RegisterSerializer, UserSerializer, MessageSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Message
from .utils import error_response


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
        return error_response("Invalid link", code="invalid_link", status_code=status.HTTP_404_NOT_FOUND)
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_messages(request):
    messages = Message.objects.filter(user=request.user)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(request, id):
    try:
        message = Message.objects.get(id=id, user=request.user)
    except Message.DoesNotExist:
        return error_response("", code="invalid_link", status_code=status.HTTP_404_NOT_FOUND)
        # return Response({"error": "Message not found"}, status=status.HTTP_400_BAD_REQUEST)

    message.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

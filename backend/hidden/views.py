from hidden.serializers import RegisterSerializer, UserSerializer, MessageSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Message
from .utils import error_response
from rest_framework import generics
from hidden.filter import MessageFilter
from rest_framework import filters
from .throttles import MessageAnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
 
    
        user_data = UserSerializer(user).data

        return Response( 
            {
                "message": "User registered successfully",
                "user": user_data
            },
            status=status.HTTP_201_CREATED 
        )

 
# @api_view(["POST"])
# @permission_classes([AllowAny])  
# def register(request): 
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         # serialize user to return safe info
#         user_data = UserSerializer(user).data 
#         return Response(
#             {
#                 "message": "User registered successfully",
#                 "user": user_data
#             },
#             status=status.HTTP_201_CREATED
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def send_message(request, secret_link):
#     try:
#         user = User.objects.get(secret_link=secret_link)
#     except User.DoesNotExist:
#         return error_response("Invalid link", code="invalid_link", status_code=status.HTTP_404_NOT_FOUND)
#     serializer = MessageSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=user)
#         return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [MessageAnonRateThrottle]

    def perform_create(self, serializer):
        secret_link = self.kwargs.get("secret_link")
        user = get_object_or_404(User, secret_link=secret_link)
        serializer.save(user=user)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_messages(request):
#     messages = Message.objects.filter(user=request.user)
#     serializer = MessageSerializer(messages, many=True) 
#     return Response(serializer.data)
 
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = MessageFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['message']
    ordering_fields = ['created_at', 'is_read']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # only messages for the logged-in user
        return Message.objects.filter(user=self.request.user)

 
# @api_view(["DELETE"]) 
# @permission_classes([IsAuthenticated])
# def delete_message(request, id):
#     try:
#         message = Message.objects.get(id=id, user=request.user)
#     except Message.DoesNotExist:
#         return error_response("", code="invalid_link", status_code=status.HTTP_404_NOT_FOUND)
#         # return Response({"error": "Message not found"}, status=status.HTTP_400_BAD_REQUEST)

#     message.delete()
#     return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
 

# @api_view(["GET"])  
# @permission_classes([AllowAny])
# def get_users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data) 

class GetUpdateDeleteMessageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all().order_by('id')
    

class DashboardView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
 
    def get_object(self):
        # Return only the currently logged-in user 
        return self.request.user

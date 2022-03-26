from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import generics, permissions

from .serializers import MyTokenObtainPairSerializer, Userserializer


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom token view"""

    serializer_class = MyTokenObtainPairSerializer
    my_tags = ["User Authentication"]


class MyTokenRefreshView(TokenRefreshView):
    """Custom refresh token view"""

    my_tags = ["User Authentication"]


class CreateUserView(generics.CreateAPIView):
    """create a new user in the project"""

    serializer_class = Userserializer
    my_tags = ["User Authentication"]


class ProfileUserView(generics.RetrieveUpdateDestroyAPIView):
    """Retives and updates the authenticated user's profile"""

    queryset = User.objects.all()
    serializer_class = Userserializer
    permission_classes = (permissions.IsAuthenticated,)
    my_tags = ["Profile"]

    def get_object(self):
        """Retrieve authenticated user"""
        return self.request.user

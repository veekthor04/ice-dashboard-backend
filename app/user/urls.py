"""
User setup url config
"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from user.views import (
    MyTokenObtainPairView,
    CreateUserView,
    ProfileUserView,
    MyTokenRefreshView,
)


app_name = 'user'

router = SimpleRouter()

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("profile/", ProfileUserView.as_view(), name="profile"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls

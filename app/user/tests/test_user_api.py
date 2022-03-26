from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Reverse URLs
SIGNUP_USER_URL = reverse("user:signup")
LOGIN_URL = reverse("user:login")
PROFILE_URL = reverse("user:profile")
TOKEN_REFRESH_URL = reverse("user:token_refresh")


# Helper function to create user
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Unauthenticated user request
class PublicUserApiTests(TestCase):
    """Test the users public API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "Testpassword123",
        }
        response = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_exists(self):
        """Test creating user that already exist fails"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "Testpassword123",
        }
        create_user(**payload)

        response = self.client.post(SIGNUP_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 8 character"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "T123",
        }
        response = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_login_for_valid_user(self):
        """Test that access and refresh token is created for the user login"""
        payload = {"username": "testuser", "password": "Testpassword123"}
        create_user(**payload)
        response = self.client.post(LOGIN_URL, payload)

        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        """Test that access and refresh token is not created if login
        credentials are invalid"""
        create_user(
            username="testuser",
            email="test@test.com",
            password="Testpassword123",
        )
        payload = {"username": "testuser", "password": "invalid"}
        response = self.client.post(LOGIN_URL, payload)

        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_token_not_created_if_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {"username": "testuser", "password": "Testpassword123"}
        response = self.client.post(LOGIN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_field(self):
        """Test that username and password are required during login"""
        payload = {"username": "testuser", "password": ""}
        response = self.client.post(LOGIN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_refresh(self):
        """Test that token can be refreshed"""
        login_payload = {"username": "testuser", "password": "Testpassword123"}
        create_user(**login_payload)
        login_response = self.client.post(LOGIN_URL, login_payload)
        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            TOKEN_REFRESH_URL, {"refresh": refresh_token}
        )
        refresh_token = login_response.data["access"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


# Authenticated user request
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            username="testuser",
            email="test@test.com",
            password="Testpassword123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
            },
        )

    def test_post_profile_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        response = self.client.post(PROFILE_URL, {})

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {"password": "newpassword123"}

        response = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

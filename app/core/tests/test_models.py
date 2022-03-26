from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_successful(self):
        """ "Test creating a new user with an email is successful"""
        username = "testuser"
        email = "test@test.com"
        password = "Testpassword1234"
        user = get_user_model().objects.create_user(
            username=username, email=email, password=password
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_credentials(self):
        """Test creating with invalid credentials raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testuser")

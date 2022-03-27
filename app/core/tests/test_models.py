from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Customer, Payment


def sample_customer(
    name: str = "testname",
    email: str = "test@test.com",
    address: str = "123 test address",
) -> Customer:
    """Create a sample customer account"""
    return Customer.objects.create(name=name, email=email, address=address)


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

    def test_create_customer_successful(self):
        """Test creating a new customer is successful"""
        name = "test name"
        email = "test@test.com"
        address = "123 test address"

        customer = Customer.objects.create(
            name=name, email=email, address=address
        )

        self.assertEqual(
            str(customer),
            f"ID: {customer.customer_id} Balance: {customer.balance}",
        )

    def test_create_payment_successful(self):
        """Test creating a payment customer is successful"""
        test_customer = sample_customer()
        payment = Payment.objects.create(customer=test_customer, amount=2000)

        self.assertEqual(
            str(payment),
            f"Ref: {payment.payment_ref} Amount: {payment.amount}",
        )

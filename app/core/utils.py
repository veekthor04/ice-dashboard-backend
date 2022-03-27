from decimal import Decimal

from django.contrib.auth import get_user_model
from drf_yasg.inspectors import SwaggerAutoSchema

from core.models import Customer, Payment


class CustomAutoSchema(SwaggerAutoSchema):
    """Custom SwaggerAutoSchema to add tags to views"""

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get("tags", None) or getattr(
            self.view, "my_tags", []
        )
        if not tags:
            tags = [operation_keys[0]]

        return tags


def sample_user(
    username="testuser", email="test@test.com", password="Testpassword_123"
):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        username,
        email,
        password,
    )


def sample_customer(
    name: str = "test name",
    email: str = "test@test.com",
    address: str = "123 test address",
) -> Customer:
    """Create a sample customer"""
    return Customer.objects.create(name=name, email=email, address=address)


def sample_payment(customer: Customer, amount: Decimal = 100) -> Payment:
    """Create a sample payment"""
    return Payment.objects.create(customer=customer, amount=amount)

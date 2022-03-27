import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from shortuuid.django_fields import ShortUUIDField


class User(AbstractUser):
    """Custom User model"""

    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["username"]


class Customer(models.Model):
    """Customer model to keep customer's details"""

    customer_id = ShortUUIDField(
        length=10,
        max_length=40,
        prefix="CUS_",
        alphabet="0123456789ABCDEFGHJKLMNPQRSTUVWXYZ",
        editable=False,
        unique=True,
        db_index=True,
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    balance = models.DecimalField(
        decimal_places=2, max_digits=18, default=0.00
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"ID: {self.customer_id} Balance: {self.balance}"


class Payment(models.Model):
    """Payment Model to keep record of customers payment"""

    payment_ref = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="customer_payment",
        null=True,
        blank=False,
    )
    amount = models.DecimalField(decimal_places=2, max_digits=18, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"Ref: {self.payment_ref} Amount: {self.amount}"

    def update_customer_balance(self) -> None:
        """Updates the connected customer's balance"""
        self.customer.balance += self.amount
        self.customer.save()

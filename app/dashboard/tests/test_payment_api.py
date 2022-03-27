from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Payment
from core.utils import sample_user, sample_customer, sample_payment
from dashboard.serializers import PaymentSerializer, CreatePaymentSerializer


PAYMENT_LIST_URL = reverse("dashboard:payment-list")


def payment_detail_url(payment_ref: str):
    """Return the detail url for a payment"""
    return reverse("dashboard:payment-detail", args=[payment_ref])


def customer_payment_list_url(customer_id: str):
    """Return the list url for a customer's payment"""
    return reverse("dashboard:customer-payment-list", args=[customer_id])


class PublicCustomerAPITests(TestCase):
    """Test the unauthenticated payment api access"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required_for_payment(self):
        """Test login is required to access API"""
        res = self.client.get(PAYMENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_required_for_customer_payment_list(self):
        """Test login is required to access API"""

        url = customer_payment_list_url("test_customer_id")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCustomerAPITests(TestCase):
    """Test the authenticated payment api access"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    def test_create_payment_successful(self):
        """Test url to create payment for customer"""
        test_customer = sample_customer()
        test_customer_id = test_customer.customer_id

        payload = {
            "customer": test_customer_id,
            "amount": 1000,
        }

        res = self.client.post(PAYMENT_LIST_URL, payload)

        test_customer.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertAlmostEqual(test_customer.balance, 1000)

    def test_create_payment_invalid_data(self):
        """Test url to create payment for customer with invalid data"""
        payload = {
            "customer": "fake_id_123",
            "amount": 0,
        }

        res = self.client.post(PAYMENT_LIST_URL, payload)

        serializer = CreatePaymentSerializer(data=payload)
        serializer.is_valid()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json(), serializer.errors)

    def test_list_payment(self):
        """Test payment url to list created payments"""

        customer = sample_customer()

        sample_payment(customer=customer)
        sample_payment(customer=customer)
        sample_payment(customer=customer)

        res = self.client.get(PAYMENT_LIST_URL)

        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.json())
        self.assertEqual(res.json()["results"], serializer.data)

    def test_retrieve_payment_success(self):
        """Test payment url to retrieve a payment"""

        customer = sample_customer()
        payment = sample_payment(customer=customer)

        url = payment_detail_url(payment.payment_ref)
        res = self.client.get(url)

        payment = Payment.objects.get(payment_ref=payment.payment_ref)
        serializer = PaymentSerializer(payment, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), serializer.data)

    def test_retrieve_payment_not_found(self):
        """Test payment url to retrieve a payment that doesnot exist"""

        payment_ref = "test_id123"

        url = payment_detail_url(payment_ref)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_payment_not_allowed(self):
        """Test that PUT is not allowed on the payment url"""

        payment_ref = "test_id123"

        url = payment_detail_url(payment_ref)
        res = self.client.put(url, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_payment_not_allowed(self):
        """Test that PATCH is not allowed on the payment url"""

        payment_ref = "test_id123"

        url = payment_detail_url(payment_ref)
        res = self.client.patch(url, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_customer_payment(self):
        """Test customer payment url to list created customer's payments"""

        customer_1 = sample_customer()
        customer_2 = sample_customer()

        sample_payment(customer=customer_1)
        sample_payment(customer=customer_2)
        sample_payment(customer=customer_1)

        url = customer_payment_list_url(customer_id=customer_1.customer_id)
        res = self.client.get(url)

        payments = Payment.objects.filter(customer=customer_1)
        serializer = PaymentSerializer(payments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.json())
        self.assertEqual(res.json()["results"], serializer.data)
